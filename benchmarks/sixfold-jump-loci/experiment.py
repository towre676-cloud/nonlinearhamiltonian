"""Reproduce the baseline and evaluate frozen trajectory-only estimators."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np
import scipy
from scipy.special import ndtr

from evaluate import baseline, score
from identify import TERMS, classify_exact, distances, fit_field, rational_candidate, regularize

SPLITS = ('train', 'validation', 'test')
DEPTHS = np.array([1, 2, 6])
MAGNITUDES = ('1/10', '1/1000', '1/100000')
PREFIXES = (13, 25, 49)
METHODS = ('local-field-nearest', 'weak-field-nearest', 'weak-locus',
           'guarded-weak-locus', 'regularized-weak-locus', 'weak-locus-calibrated', 'raw-nearest')


def read_labels(path):
    labels = {split: {} for split in SPLITS[:2]}
    for line in path.read_text().splitlines():
        row = json.loads(line)
        if row['split'] in labels:
            labels[row['split']][row['id']] = row['least_depth']
    return labels


def split_summary(data):
    """Independent pair construction and benchmark-design audit."""
    groups = defaultdict(list)
    for line in (data/'exact.jsonl').read_text().splitlines():
        row = json.loads(line)
        groups[row['group']].append(row)
    pairs = {split: [] for split in SPLITS}
    axes = {split: Counter() for split in SPLITS}
    for members in groups.values():
        original, = [r for r in members if r['perturbation'] is None]
        split, family = original['split'], original['stratum']
        assert all(r['split'] == split and r['stratum'] == family for r in members)
        if family == 'depth-six':
            assert len(members) == 1 and original['least_depth'] == 6
            continue
        assert len(members) == 4 and original['least_depth'] == 2
        offsets = set()
        for off in members:
            change = off['perturbation']
            if change is None:
                continue
            eps = str(abs(Fraction(change['delta'])))
            assert off['least_depth'] == 1
            offsets.add(eps)
            axis = tuple(change['monomial'])
            h = {(i, j): Fraction(v) for i, j, v in original['coefficients']}
            k = {(i, j): Fraction(v) for i, j, v in off['coefficients']}
            assert {term for term in h.keys() | k.keys() if h.get(term,0) != k.get(term,0)} == {axis}
            assert k.get(axis, 0) - h.get(axis, 0) == Fraction(change['delta'])
            axes[split][f'{family}:q^{axis[0]}p^{axis[1]}'] += 1
            pairs[split].append((family, eps, original['id'], off['id']))
        assert offsets == set(MAGNITUDES)
    for split, n in zip(SPLITS, (90, 45, 45)):
        assert len(pairs[split]) == n
    return pairs, {split: dict(sorted(counts.items())) for split, counts in axes.items()}


def pair_summary(pairs, predictions, official):
    lookup = {(r['id'], r['noise_index']): r['depth'] for r in predictions}
    output = {}
    for noise in range(4):
        counts = defaultdict(Counter)
        for family, eps, on, off in pairs:
            a, b = lookup[on, noise], lookup[off, noise]
            for group in ((family, eps), ('all', eps), ('all', 'all')):
                count = counts[group]
                count['pairs'] += 1
                count['answered'] += a is not None and b is not None
                count['both_correct'] += (a, b) == (2, 1)
        for (family, eps), count in counts.items():
            if family == 'all':
                continue
            published = official[str(noise)][family]['pairs_by_abs_perturbation'][eps]
            assert count['pairs'] == published['pairs']
            assert count['answered']/count['pairs'] == published['coverage']
            assert count['both_correct']/count['pairs'] == published['both_correct_fraction']
            assert (count['both_correct']/count['answered'] if count['answered'] else None
                    ) == published['selective_pair_accuracy']
        output[str(noise)] = {
            eps: dict(counts['all', eps]) for eps in (*MAGNITUDES, 'all')
        }
    return output


def load_arrays(data):
    arrays = {}
    for split in SPLITS:
        with np.load(data/f'trajectories_{split}.npz', allow_pickle=False) as source:
            arrays[split] = dict(source)
    return arrays


def nearest(train, query, labels):
    error = ((query[:, None, :] - train[None, :, :])**2).mean(axis=-1)
    d = np.stack([error[:, labels == depth].min(axis=1) for depth in DEPTHS], axis=1)
    best, runner_up = np.sort(d, axis=1)[:, :2].T
    return DEPTHS[d.argmin(axis=1)], (runner_up-best)/np.maximum(runner_up, 1e-30)


def ridge_prediction(train, query, labels):
    """Balanced supervised linear scores on log numerical locus distances."""
    scale = np.maximum(train.std(axis=0), 1e-12)
    center = train.mean(axis=0)
    x = np.c_[np.ones(len(train)), (train-center)/scale]
    y = labels[:, None] == DEPTHS
    weights = np.sum(y/y.sum(axis=0), axis=1)*len(x)/len(DEPTHS)
    penalty = np.diag([0.] + [1.]*train.shape[1])
    beta = np.linalg.solve(x.T @ (weights[:, None]*x)+penalty, x.T @ (weights[:, None]*y))
    scores = np.c_[np.ones(len(query)), (query-center)/scale] @ beta
    best = np.sort(scores, axis=1)[:, -2:]
    return DEPTHS[scores.argmax(axis=1)], best[:, 1]-best[:, 0]


def tolerance(features, labels):
    """Choose physics-rule tolerance by three-class validation macro recall."""
    candidates = np.r_[1e-8, np.geomspace(1e-6, 1e6, 97)]
    return max(candidates, key=lambda t: np.mean([
        np.mean(locus_prediction(features, t)[0][labels == d] == d) for d in DEPTHS
    ]))


def locus_prediction(features, threshold):
    log_scores = np.log(np.maximum(features, 1e-30)/threshold)
    depth_two, depth_six = log_scores[:, :-1].min(axis=1), log_scores[:, -1]
    rank = np.stack([np.zeros(len(features)), -depth_two, -depth_six], axis=1)
    best = np.sort(rank, axis=1)[:, -2:]
    return DEPTHS[rank.argmax(axis=1)], best[:, 1]-best[:, 0]


def selection_threshold(confidence, good):
    for candidate in np.unique(np.r_[0., confidence]):
        keep = confidence >= candidate
        if keep.sum() >= 5 and good[keep].mean() >= .8:
            return float(candidate)
    return None


def select_records(ids, k, guess, confidence, threshold, force=False):
    return [dict(id=case_id, noise_index=k,
                 depth=int(depth) if force or (threshold is not None and conf >= threshold) else None)
            for case_id, depth, conf in zip(ids, guess, confidence)]


def featurize(arrays, sigma_index, n, certificates, prior):
    features = {}
    for split, array in arrays.items():
        t = array['t'][:n]
        sigma = float(array['noise_sigma'][sigma_index])
        states = array['qp'][:, sigma_index, :, :n]
        local = [fit_field(t, track, sigma, 'local') for track in states]
        weak = [fit_field(t, track, sigma, 'weak') for track in states]
        # Monomial units at a fixed reference scale, without consulting coefficients.
        units = np.array([.4**(sum(term)-1) for term in TERMS])
        raw = np.stack([chunk.mean(axis=2) for chunk in
                        np.array_split(states, 7, axis=2)], axis=2)
        guarded = np.stack([distances(fit, guard_branches=True) for fit in weak])
        regularized = np.stack([distances(regularize(fit, *prior), guard_branches=True)
                                for fit in weak]) if sigma else guarded
        features[split] = dict(local=np.stack([fit.coefficients*units for fit in local]),
                               weak=np.stack([fit.coefficients*units for fit in weak]),
                               locus=np.stack([distances(fit) for fit in weak]),
                               guarded=guarded, regularized=regularized,
                               condition=np.array([fit.condition for fit in weak]),
                               coefficients=np.stack([fit.coefficients for fit in weak]),
                               raw=raw.reshape(len(states), -1))
        if split == 'test' and sigma == 0 and n == 49:
            for case_id, fit, track in zip(array['ids'], weak, states):
                candidate = rational_candidate(fit, t, track)
                if candidate is not None:
                    certificates.append(dict(id=case_id, **candidate))
    return features


def evaluate_estimates(arrays, labels):
    certificates = []
    report = {}
    predictions = {}
    frozen_coefficients = {}
    training_array = arrays['train']
    for n in PREFIXES:
        # Train-only coefficient statistics estimated from clean training arrays.
        # No exact coefficients, labels, test clean tracks or group metadata enter.
        prior_sample = np.stack([fit_field(training_array['t'][:n], track, 0., 'weak').coefficients
                                 for track in training_array['qp'][:, 0, :, :n]])
        covariance = np.cov(prior_sample, rowvar=False)
        prior = (prior_sample.mean(axis=0), np.linalg.cholesky(
            covariance + .1*np.diag(np.diag(covariance)) + .05**2*np.eye(len(TERMS))
        ))
        report[str(n)] = {m: {} for m in METHODS}
        predictions[str(n)] = {m: {'forced': [], 'selective': []} for m in METHODS}
        for k in range(4):
            features = featurize(arrays, k, n, certificates, prior)
            if n == 49:
                frozen_coefficients[k] = (features['test']['coefficients'], features['test']['condition'])
            train, val, test = (features[split] for split in SPLITS)
            train_y, val_y = (np.array([labels[s][key] for key in arrays[s]['ids']])
                              for s in ('train', 'validation'))
            locus_keys = {'weak-locus': 'locus', 'guarded-weak-locus': 'guarded',
                          'regularized-weak-locus': 'regularized'}
            locus_thresholds = {m: tolerance(val[key], val_y) for m, key in locus_keys.items()}

            def fit_predict(method, query):
                if method in locus_keys:
                    return locus_prediction(query[locus_keys[method]], locus_thresholds[method])
                if method == 'weak-locus-calibrated':
                    return ridge_prediction(np.log1p(train['locus']), np.log1p(query['locus']), train_y)
                feature = {'raw-nearest': 'raw', 'weak-field-nearest': 'weak',
                           'local-field-nearest': 'local'}[method]
                return nearest(train[feature], query[feature], train_y)

            for method in METHODS:
                val_pred, val_conf = fit_predict(method, val)
                test_pred, test_conf = fit_predict(method, test)
                threshold = selection_threshold(val_conf, val_pred == val_y)
                settings = dict(selection_threshold=threshold)
                if method in locus_keys:
                    settings['locus_threshold'] = float(locus_thresholds[method])
                report[str(n)][method][str(k)] = settings
                output = predictions[str(n)][method]
                ids = arrays['test']['ids'].tolist()
                output['selective'].extend(select_records(ids,k,test_pred,test_conf,threshold))
                output['forced'].extend(select_records(ids,k,test_pred,test_conf,threshold,force=True))
    return report, predictions, certificates, frozen_coefficients


def exact_audit(data, arrays, certificates, estimates):
    """Post-prediction evaluation only. Exact coefficients never enter any fit."""
    truth = {r['id']: r for r in map(json.loads, (data/'exact.jsonl').read_text().splitlines())
             if r['split'] == 'test'}
    ids = arrays['test']['ids']
    def rational_map(rows):
        return {(i,j): Fraction(v) for i,j,v in rows}

    rows = [rational_map(truth[i]['coefficients']) for i in ids]
    exact = np.array([[float(h.get(m, 0)) for m in TERMS] for h in rows])
    error = {}
    for k, (coefficients, condition) in estimates.items():
        error[str(k)] = dict(
            median_max_coefficient_error=float(np.median(np.max(abs(coefficients-exact), axis=1))),
            median_column_scaled_condition=float(np.median(condition)),
        )
    control = Counter()
    for row in truth.values():
        assert classify_exact(rational_map(row['coefficients']))['depth'] == row['least_depth']
        control[str(row['least_depth'])] += 1
    candidate_counts = defaultdict(Counter)
    for candidate in certificates:
        row = truth[candidate['id']]
        count = candidate_counts[row['stratum']]
        count['replayed'] += 1
        count['exact_match'] += rational_map(candidate['coefficients']) == rational_map(row['coefficients'])
        count['right_depth'] += candidate['candidate_depth'] == row['least_depth']
    return dict(exact_input_control=dict(control), clean_candidate_audit=dict(candidate_counts),
                weak_coefficient_error=error)



def oracle_summary(array, pairs):
    """Post-hoc diagnostic for binary discrimination with known clean means.

    With equal priors and independent isotropic Gaussian noise, the optimal
    single-trajectory accuracy between two known candidate models is
    Phi(||mu_on - mu_off||/(2*sigma)). This is not a complete-pair score.
    """
    indexes = {key: i for i, key in enumerate(array['ids'])}
    output = {}
    for n in PREFIXES:
        items = defaultdict(list)
        for family, eps, on, off in pairs:
            a, b = (array['qp'][indexes[key], 0, :, :n] for key in (on, off))
            norm = np.linalg.norm(a-b)
            items[family, eps].append(norm)
            items['all', eps].append(norm)
        output[str(n)] = {}
        for (family, eps), norms in items.items():
            entry = output[str(n)].setdefault(family, {})
            accuracies = [float(np.mean(ndtr(np.asarray(norms)/(2*sigma)))) if sigma
                          else float(np.mean(np.where(np.asarray(norms) > 0, 1., .5)))
                          for sigma in array['noise_sigma']]
            entry[eps] = dict(n=len(norms), median_signal_l2=float(np.median(norms)),
                              mean_single_case_accuracy=accuracies)
    return output

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('data', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    data = args.data
    manifest = json.loads((data/'manifest.json').read_text())
    for filename, digest in manifest['sha256'].items():
        assert hashlib.sha256((data/filename).read_bytes()).hexdigest() == digest
    arrays = load_arrays(data)
    labels = read_labels(data/'exact.jsonl')
    # Fit and freeze trajectory predictions before opening test scoring metadata.
    report, predictions, certificates, coefficients = evaluate_estimates(arrays, labels)
    baseline_report, baseline_predictions = baseline(data)
    here = Path(__file__).resolve().parent
    expected = json.loads((here/'baseline_report.json').read_text())
    expected_predictions = list(map(json.loads, (here/'baseline_predictions.jsonl').read_text().splitlines()))
    assert baseline_report['test'] == expected['test']
    assert baseline_predictions == expected_predictions
    pairs, axes = split_summary(data)
    official = baseline_report['test']
    base_pairs = pair_summary(pairs['test'], baseline_predictions, official)
    assert all(row['all']['both_correct'] == 0 and row['all']['pairs'] == 45
               for row in base_pairs.values())
    metrics = {}
    for prefix, methods in predictions.items():
        metrics[prefix] = {}
        for method, policies in methods.items():
            metrics[prefix][method] = {}
            for policy, records in policies.items():
                official = score(data, 'test', records)
                metrics[prefix][method][policy] = dict(
                    score=official, aggregate_pairs=pair_summary(pairs['test'], records, official)
                )
    audit = exact_audit(data, arrays, certificates, coefficients)
    audit['known_pair_oracle'] = oracle_summary(arrays['test'], pairs['test'])
    args.output.mkdir(parents=True, exist_ok=True)
    results = dict(data_sha256=manifest['sha256'], numpy=np.__version__, scipy=scipy.__version__,
                   horizons={str(n): float(arrays['train']['t'][n-1]) for n in PREFIXES},
                   noise=arrays['train']['noise_sigma'].tolist(), settings=report,
                   baseline=dict(scores=baseline_report, pairs=base_pairs),
                   split_axis_counts=axes, exact_audit=audit, metrics=metrics)
    for filename, value in [('results.json',results), ('predictions.json',predictions),
                            ('candidate_certificates.json',certificates)]:
        (args.output/filename).write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')
    print('PASS: baseline reproduced, independent pair counts agree, exact control replayed')


if __name__ == '__main__':
    main()

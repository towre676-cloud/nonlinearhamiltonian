"""Freeze decision thresholds from the calibration phase only (train+validation on-locus fits)."""
import json, hashlib, numpy as np
from pathlib import Path
HERE = Path(__file__).resolve().parent; D = HERE/'out'/'estimator'
rows = [json.loads(l) for l in open(D/'calibration.jsonl')]
frozen = {'alpha': 0.05, 'interval_z': 1.959964, 'rule': {
  'constrained_forced': 'depth 1 if lam > lam_crit else depth 2',
  'constrained_selective': "depth 1 if lam > lam_crit; '|c|<eta' (scored as depth 2) if |c_hat|+z*se_c < eta; else abstain",
  'plugin_forced': 'depth 1 if |plug_z| > z_crit else depth 2'}, 'cells': {}}
for ds in ('A', 'B'):
    for sg in (1e-5, 1e-3):
        r = [x for x in rows if x['design'] == ds and x['sigma'] == sg]
        lam = np.array([x['lam'] for x in r]); pz = np.abs([x['plug_z'] for x in r])
        upper = np.array([abs(x['c_hat']) + 1.959964*x['se_c'] for x in r])
        frozen['cells'][f'{ds}|{sg:g}'] = dict(
            n=len(r), fit_failures=int(sum(x['fails'] > 0 for x in r)), inconsistent=int(sum(x['inconsistent'] for x in r)),
            false_pos_at_3p84=float((lam > 3.841459).mean()), plug_false_pos_at_1p96=float(np.nanmean(pz > 1.959964)),
            lam_crit=float(max(3.841459, np.quantile(lam, .95))), z_crit=float(max(1.959964, np.nanquantile(pz, .95))),
            eta=float(np.quantile(upper, .95)), median_se_c=float(np.median([x['se_c'] for x in r])),
            median_chi2_red=float(np.median([x['chi2_red'] for x in r])))
s = json.dumps(frozen, indent=1); (D/'frozen.json').write_text(s)
print(s); print('sha256', hashlib.sha256(s.encode()).hexdigest())

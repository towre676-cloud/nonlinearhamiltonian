"""Second domain for `exact_observation`: prime-valuation period fingerprints.

For a weighted projective space with weight multiset w and total weight L, the
m-th supported regularized quantum period coefficient is (mL)! / prod (m w_i)!.
Two spaces with equal L share that coefficient iff, for every prime p,
sum_i v_p((m w_i)!) agrees.  With u = (multiplicity vector of the left space)
- (that of the right space), agreement of the first K supported coefficients
is exactly: u lies in the kernel of the integer observation map with rows

    total:   a -> a                      (equal total weight)
    (m, p):  a -> v_p((m a)!),  m <= K, p prime <= m * max weight.

This is the matrix used in period-fingerprint-lab's fixed-prefix ambiguity
theorem.  The same exact kernel / minimum-cost panel / exchange certificate
code that handles Moyal gates handles it unchanged.
"""
from __future__ import annotations
from exact_observation import ObservationSystem


def primes_to(n):
    sieve = [True] * (n + 1)
    out = []
    for i in range(2, n + 1):
        if sieve[i]:
            out.append(i)
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return out


def factorial_valuation(n, p):
    v = 0
    while n:
        n //= p
        v += n
    return v


def valuation_system(max_weight, prefix):
    """Observations on Z^{1..max_weight}; cost of (m, p) is m, the degree multiple needed."""
    coords = list(range(1, max_weight + 1))
    obs = [("total", 0, coords)]
    for m in range(1, prefix + 1):
        for p in primes_to(m * max_weight):
            obs.append(((m, p), m, [factorial_valuation(m * a, p) for a in coords]))
    return ObservationSystem(coords, obs)


def difference_vector(left, right, max_weight):
    u = [0] * max_weight
    for a in left:
        u[a - 1] += 1
    for a in right:
        u[a - 1] -= 1
    return u


def collision_report(left, right, prefix):
    """Is the pair indistinguishable by the first `prefix` supported coefficients?"""
    mw = max(max(left), max(right))
    sys_ = valuation_system(mw, prefix)
    u = difference_vector(left, right, mw)
    hits = sys_.separating_observations(u)
    return {"indistinguishable": not hits,
            "cheapest_separator": None if not hits else sys_.labels[hits[0]],
            "separator_count": len(hits)}

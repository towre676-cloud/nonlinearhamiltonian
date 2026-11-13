"""Exact observation design over the rationals.

A model class is a finite-dimensional rational vector space with labelled
coordinates; an observation is a labelled rational linear functional with a
nonnegative cost.  The engine answers, exactly:

* the rank of the observation map and a basis of its kernel (each kernel
  vector is an indistinguishability witness: two models differing by it give
  identical observations);
* a minimum-cost identifying panel (a set of observations of the same rank as
  the whole family).  Rows of a matrix form a linear matroid, so the greedy
  choice by increasing cost is optimal; the certificate records the single
  exchange test that characterises minimum-weight bases;
* the worst-case error amplification of a square identifying panel,
  `max_i sum_j |(A^-1)_ij|`, for adversarial errors bounded by 1 per sensor.

Nothing here is specific to a mathematical domain.  `weighted_cubic_form.py`
uses it for Moyal gate matrices and `period_valuation_transfer.py` for
prime-valuation fingerprints of weighted projective spaces.
Only the standard library is used.
"""
from __future__ import annotations
from fractions import Fraction as Fr


def _F(v):
    if isinstance(v, Fr):
        return v
    if isinstance(v, int):
        return Fr(v)
    if isinstance(v, str):
        return Fr(v)
    raise TypeError("inexact or unsupported coefficient: %r" % (v,))


def rref(rows, ncols):
    """Reduced row echelon form; returns (reduced rows, pivot columns)."""
    m = [[_F(v) for v in r] for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if pr is None:
            continue
        m[r], m[pr] = m[pr], m[r]
        inv = 1 / m[r][c]
        m[r] = [v * inv for v in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c)
        r += 1
        if r == len(m):
            break
    return m[:r], piv


def rank(rows, ncols):
    return len(rref(rows, ncols)[1])


def kernel(rows, ncols):
    """Basis of {v : rows . v = 0}, one vector per free column."""
    red, piv = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    out = []
    for f in free:
        v = [Fr(0)] * ncols
        v[f] = Fr(1)
        for i, pc in enumerate(piv):
            v[pc] = -red[i][f]
        out.append(v)
    return out


def det(square):
    """Fraction-free (Bareiss) determinant of a rational square matrix."""
    n = len(square)
    a = [[_F(v) for v in r] for r in square]
    sign, prev = 1, Fr(1)
    for k in range(n - 1):
        if a[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if a[i][k] != 0), None)
            if sw is None:
                return Fr(0)
            a[k], a[sw] = a[sw], a[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) / prev
        prev = a[k][k]
    return sign * a[n - 1][n - 1] if n else Fr(1)


def inverse(square):
    n = len(square)
    aug = [[_F(v) for v in r] + [Fr(int(i == j)) for j in range(n)] for i, r in enumerate(square)]
    red, piv = rref(aug, n)
    if piv != list(range(n)):
        raise ValueError("singular panel")
    return [r[n:] for r in red]


class ObservationSystem:
    """Labelled rational observations of a labelled coordinate space."""

    def __init__(self, coordinates, observations):
        self.coordinates = list(coordinates)
        self.labels, self.costs, self.rows = [], [], []
        n = len(self.coordinates)
        for label, cost, row in observations:
            if len(row) != n:
                raise ValueError("row length mismatch at %r" % (label,))
            if _F(cost) < 0:
                raise ValueError("negative cost")
            self.labels.append(label)
            self.costs.append(_F(cost))
            self.rows.append([_F(v) for v in row])

    @property
    def n(self):
        return len(self.coordinates)

    def rank(self, panel=None):
        rows = self.rows if panel is None else [self.rows[i] for i in panel]
        return rank(rows, self.n) if rows else 0

    def witnesses(self, panel=None):
        rows = self.rows if panel is None else [self.rows[i] for i in panel]
        return kernel(rows, self.n) if rows else [[Fr(int(i == j)) for j in range(self.n)] for i in range(self.n)]

    def minimum_cost_panel(self):
        """Indices of a minimum-total-cost panel with the rank of the full system."""
        order = sorted(range(len(self.rows)), key=lambda i: (self.costs[i], i))
        chosen, basis = [], []
        for i in order:
            if rank(basis + [self.rows[i]], self.n) > len(basis):
                basis.append(self.rows[i])
                chosen.append(i)
        return chosen

    def separating_observations(self, vector):
        """Observations with nonzero value on a candidate ambiguity, cheapest first."""
        vec = [_F(v) for v in vector]
        hits = [i for i, r in enumerate(self.rows) if sum(a * b for a, b in zip(r, vec)) != 0]
        return sorted(hits, key=lambda i: (self.costs[i], i))

    def amplification(self, panel):
        """Exact sup-norm amplification of a square full-rank panel on its pivot columns."""
        rows = [self.rows[i] for i in panel]
        _, piv = rref(rows, self.n)
        if len(piv) != len(panel):
            raise ValueError("panel is not independent")
        inv = inverse([[r[c] for c in piv] for r in rows])
        return max(sum(abs(v) for v in r) for r in inv)

    def certificate(self):
        panel = self.minimum_cost_panel()
        rows = [self.rows[i] for i in panel]
        _, piv = rref(rows, self.n) if rows else ([], [])
        minor = [[r[c] for c in piv] for r in rows]
        return {
            "schema": "exact-observation-certificate/1",
            "coordinates": [str(c) for c in self.coordinates],
            "observations": [{"label": str(l), "cost": str(c), "row": [str(v) for v in r]}
                             for l, c, r in zip(self.labels, self.costs, self.rows)],
            "rank": len(panel),
            "panel": panel,
            "panel_cost": str(sum((self.costs[i] for i in panel), Fr(0))),
            "pivot_columns": piv,
            "pivot_minor_determinant": str(det(minor)) if panel else "1",
            "kernel_witnesses": [[str(v) for v in w] for w in self.witnesses()],
        }


def verify_certificate(cert):
    """Replay a certificate with independent code paths; returns a list of checked facts.

    Rank is established as a sandwich: the panel minor is nonzero (rank >= r) and
    the listed witnesses are independent kernel vectors, n - r of them (rank <= r).
    Optimality is the matroid exchange test for a minimum-weight basis.
    """
    if cert.get("schema") != "exact-observation-certificate/1":
        raise ValueError("unknown schema")
    n = len(cert["coordinates"])
    rows = [[Fr(v) for v in o["row"]] for o in cert["observations"]]
    costs = [Fr(o["cost"]) for o in cert["observations"]]
    panel, piv, r = cert["panel"], cert["pivot_columns"], cert["rank"]
    facts = []
    if len(panel) != r or len(piv) != r or len(set(panel)) != r:
        raise AssertionError("panel shape")
    minor = [[rows[i][c] for c in piv] for i in panel]
    d = det(minor)
    if d == 0 or str(d) != cert["pivot_minor_determinant"]:
        raise AssertionError("pivot minor")
    facts.append("rank >= %d (nonzero %dx%d minor)" % (r, r, r))
    wit = [[Fr(v) for v in w] for w in cert["kernel_witnesses"]]
    for w in wit:
        for row in rows:
            if sum(a * b for a, b in zip(row, w)) != 0:
                raise AssertionError("witness is observable")
    if len(wit) != n - r or (wit and rank(wit, n) != len(wit)):
        raise AssertionError("witness count or independence")
    facts.append("rank <= %d (%d independent unobservable witnesses)" % (r, n - r))
    total = sum((costs[i] for i in panel), Fr(0))
    if str(total) != cert["panel_cost"]:
        raise AssertionError("panel cost")
    inside = set(panel)
    for out in range(len(rows)):
        if out in inside:
            continue
        for s in panel:
            if costs[out] < costs[s]:
                trial = [rows[i] for i in panel if i != s] + [rows[out]]
                if rank(trial, n) == r:
                    raise AssertionError("cheaper exchange exists")
    facts.append("panel cost %s is minimal (no improving single exchange)" % total)
    return facts

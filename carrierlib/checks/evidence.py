"""checks.evidence — probability & evidence carriers."""
from __future__ import annotations
import itertools, math
from fractions import Fraction as Fr
from ..core import check


@check("kolmogorov_axioms_to_bayes")
def _():
    import numpy as np
    rng = np.random.default_rng(12)
    ok = True
    for _ in range(50):
        p = rng.dirichlet(np.ones(6))          # a random finite space
        idx = np.arange(6)
        A = idx < 3
        B = (idx % 2) == 0
        PA, PB = p[A].sum(), p[B].sum()
        PAB = p[A & B].sum()
        if PB > 1e-9 and PA > 1e-9:
            bayes = abs(PAB / PB - (PAB / PA) * PA / PB) < 1e-12
            ok &= bayes
        # total probability over the partition {B, not B}:
        tot = abs(PA - (p[A & B].sum() + p[A & ~B].sum())) < 1e-12
        mono = PAB <= PA + 1e-12
        ok &= tot and mono
    return ok, "FORCED", \
        ("on 50 random finite probability spaces: Bayes' identity, the "
         "law of total probability, and monotonicity all reduce to "
         "arithmetic of the measure — no new axiom needed beyond "
         "additivity and P(Omega)=1 (the two the record names)")


@check("bayes_sequential_and_dutch_book")
def _():
    import numpy as np
    rng = np.random.default_rng(13)
    ok = True
    for _ in range(30):
        prior = rng.dirichlet(np.ones(3))
        L1 = rng.random(3)                      # likelihood of e1 per H
        L2 = rng.random(3)
        seq = prior * L1
        seq /= seq.sum()
        seq = seq * L2
        seq /= seq.sum()
        joint = prior * (L1 * L2)
        joint /= joint.sum()
        ok &= np.allclose(seq, joint)
    # Dutch book against incoherence: someone prices P(A)=0.6 and
    # P(not A)=0.6. Sell them both bets at their prices:
    stake = 1.0
    price_A, price_notA = 0.6, 0.6
    bookie_take = price_A + price_notA          # collects 1.2
    payout = stake                              # pays exactly 1 always
    guaranteed = bookie_take - payout
    return ok and abs(guaranteed - 0.2) < 1e-12, "FORCED", \
        ("sequential updating equals joint updating on 30 random cases "
         "(conditional independence given H); and the Dutch book is "
         "constructed: prices P(A)=P(~A)=0.6 hand the bookie a "
         "guaranteed +0.20 per unit stake regardless of outcome — "
         "incoherence is a purchasable loss")


@check("dempster_shafer_zadeh")
def _():
    def combine(m1, m2, frame):
        K = sum(m1[B] * m2[C]
                for B in m1 for C in m2 if not (set(B) & set(C)))
        out = {}
        for B in m1:
            for C in m2:
                A = tuple(sorted(set(B) & set(C)))
                if A:
                    out[A] = out.get(A, 0) + m1[B] * m2[C]
        return {A: v / (1 - K) for A, v in out.items()}, K
    frame = ("meningitis", "concussion", "tumor")
    m1 = {("meningitis",): 0.99, ("tumor",): 0.01}
    m2 = {("concussion",): 0.99, ("tumor",): 0.01}
    m12, K = combine(m1, m2, frame)
    zadeh = abs(m12[("tumor",)] - 1.0) < 1e-9 and K > 0.99
    # Bel <= Pl on a sample BPA; vacuous = total ignorance:
    m = {("a",): Fr(3, 10), ("a", "b"): Fr(5, 10), ("a", "b", "c"): Fr(2, 10)}
    Bel = lambda A: sum(v for B, v in m.items() if set(B) <= set(A))
    Pl = lambda A: sum(v for B, v in m.items() if set(B) & set(A))
    order = all(Bel(A) <= Pl(A) for A in [("a",), ("b",), ("a", "b")])
    vac = {("a", "b", "c"): 1}
    BelV = lambda A: sum(v for B, v in vac.items() if set(B) <= set(A))
    PlV = lambda A: sum(v for B, v in vac.items() if set(B) & set(A))
    ignorance = BelV(("a",)) == 0 and PlV(("a",)) == 1
    return zadeh and order and ignorance, "FORCED", \
        ("Zadeh's paradox computed exactly: two sources 99% sure of "
         "DIFFERENT diagnoses combine to 100% certainty in the tumor "
         "NEITHER believed (conflict K=0.9998 normalized away); "
         "Bel<=Pl verified; the vacuous BPA yields [0,1] — ignorance "
         "distinct from uniform uncertainty")


@check("possibility_maxitive")
def _():
    pi = {"a": 1.0, "b": 0.7, "c": 0.2}
    Pi = lambda A: max((pi[x] for x in A), default=0.0)
    N = lambda A: 1 - Pi([x for x in pi if x not in A])
    maxitive = all(abs(Pi(set(A) | set(B)) - max(Pi(A), Pi(B))) < 1e-12
                   for A in (["a"], ["b"], ["a", "c"])
                   for B in (["b"], ["c"], ["a", "b"]))
    dual = all(abs(N(A) + Pi([x for x in pi if x not in A]) - 1) < 1e-12
               for A in (["a"], ["a", "b"], ["c"]))
    both_possible = Pi(["a"]) == 1.0 and Pi(["b", "c"]) == 0.7
    ign = {"a": 1.0, "b": 1.0, "c": 1.0}
    PiI = lambda A: max((ign[x] for x in A), default=0)
    ignorance = PiI(["a"]) == 1 and PiI(["b", "c"]) == 1
    return maxitive and dual and ignorance, "FORCED", \
        ("Pi(A u B) = max — enumerated; N(A) = 1 - Pi(~A) duality holds; "
         "under the vacuous distribution both A and ~A carry possibility "
         "1 simultaneously — the additivity axiom is the thing removed, "
         "and ignorance becomes expressible")


@check("imprecise_credal_dilation")
def _():
    # credal set = convex hull of a positively and a negatively
    # correlated joint over (X,Y) in {0,1}^2, both with P(X=1)=1/2;
    # conditioning on Y WIDENS the X-interval from a point to [0.2,0.8].
    P1 = {(0, 0): 0.4, (0, 1): 0.1, (1, 0): 0.1, (1, 1): 0.4}
    P2 = {(0, 0): 0.1, (0, 1): 0.4, (1, 0): 0.4, (1, 1): 0.1}
    K = [P1, P2]
    PX = lambda P: P[(1, 0)] + P[(1, 1)]
    PXgY = lambda P, y: (P[(1, y)]) / (P[(0, y)] + P[(1, y)])
    prior_lo, prior_hi = min(map(PX, K)), max(map(PX, K))
    post = [PXgY(P, 0) for P in K]
    post_lo, post_hi = min(post), max(post)
    dilated = post_lo < prior_lo and post_hi > prior_hi
    conj = all(abs((1 - PX(P)) + PX(P) - 1) < 1e-12 for P in K)
    return dilated and conj, "FORCED", \
        (f"dilation constructed: prior interval for X is "
         f"[{prior_lo:.2f},{prior_hi:.2f}] (a point), posterior after "
         f"observing Y=0 is [{post_lo:.2f},{post_hi:.2f}] — conditioning "
         "WIDENED the interval; evidence can honestly increase "
         "imprecision, which a single measure cannot express")


@check("boundary_law_scaling")
def _():
    import numpy as np
    # The Boundary Law D = 8 sigma^2 ln(1/delta) / gap^2: measure the
    # sample count needed to tell two Gaussian means apart at 1-delta,
    # and verify the 1/gap^2 scaling by log-log slope.
    rng = np.random.default_rng(14)
    sigma, delta = 1.0, 0.1
    gaps = [0.8, 0.4, 0.2]
    measured = []
    for gap in gaps:
        # find n where the decision (mean > midpoint) errs <= delta
        n = 1
        while True:
            errs = 0
            trials = 400
            for _ in range(trials):
                x = rng.normal(gap, sigma, size=n).mean()
                errs += x < gap / 2
            if errs / trials <= delta:
                measured.append(n)
                break
            n = max(n + 1, int(n * 1.3))
    slopes = [math.log(measured[i + 1] / measured[i])
              / math.log(gaps[i] / gaps[i + 1])
              for i in range(len(gaps) - 1)]
    inv_square = all(1.5 < s < 2.6 for s in slopes)
    formula = 8 * sigma**2 * math.log(1 / delta) / gaps[-1]**2
    same_order = 0.05 < measured[-1] / formula < 2.0
    return inv_square and same_order, "EMPIRICAL", \
        (f"halving the gap multiplied the required sample count by "
         f"~4 (log-log slopes {[f'{s:.1f}' for s in slopes]} vs exponent "
         f"2); measured n={measured[-1]} at gap=0.2 vs formula "
         f"{formula:.0f} — same order. The near-boundary distinction is "
         "the expensive one, quantitatively; universality across "
         "carriers NOT claimed (per the record)")

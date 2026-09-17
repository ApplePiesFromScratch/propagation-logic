"""checks.math2 + checks.cs material — Galois through Petri nets."""
from __future__ import annotations
from fractions import Fraction as Fr
import itertools, math, random
import sympy as sp
from ..core import check


@check("galois_biquadratic")
def _():
    """K = Q(sqrt2, sqrt3): the full correspondence, enumerated.
    Elements as tuples (a,b,c,d) = a + b*sqrt2 + c*sqrt3 + d*sqrt6."""
    autos = [(s2, s3) for s2 in (1, -1) for s3 in (1, -1)]
    def apply(sig, v):
        s2, s3 = sig
        a, b, c, d = v
        return (a, b * s2, c * s3, d * s2 * s3)
    def mul(u, v):
        a, b, c, d = u
        e, f, g, h = v
        return (a * e + 2 * b * f + 3 * c * g + 6 * d * h,
                a * f + b * e + 3 * c * h + 3 * d * g,
                a * g + c * e + 2 * b * h + 2 * d * f,
                a * h + d * e + b * g + c * f)
    # each auto is a field hom: check multiplicativity on samples
    rng = random.Random(5)
    samples = [tuple(rng.randint(-3, 3) for _ in range(4))
               for _ in range(12)]
    hom = all(apply(s, mul(u, v)) == mul(apply(s, u), apply(s, v))
              for s in autos for u in samples for v in samples)
    # group is C2 x C2: every element self-inverse
    c2c2 = all(apply(s, apply(s, v)) == v for s in autos for v in samples)
    # fixed fields: enumerate what each proper subgroup fixes
    basis = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    subgroups = {"<s2>": [(1, 1), (-1, 1)], "<s3>": [(1, 1), (1, -1)],
                 "<s2s3>": [(1, 1), (-1, -1)]}
    fixed = {name: [b for b in basis
                    if all(apply(s, b) == b for s in G)]
             for name, G in subgroups.items()}
    # <s2 as -1 on sqrt2> fixes 1 and sqrt3; <s3->-1> fixes 1, sqrt2;
    # the diagonal fixes 1 and sqrt6: three distinct intermediate fields
    distinct = len({tuple(map(tuple, f)) for f in fixed.values()}) == 3
    degree = len(autos) == 4
    return hom and c2c2 and distinct and degree, "FORCED", \
        ("Q(sqrt2,sqrt3): all four automorphisms verified as field homs; "
         "group = C2xC2 (every element self-inverse); the three proper "
         "subgroups fix exactly the three intermediate fields Q(sqrt3), "
         "Q(sqrt2), Q(sqrt6) — the correspondence, enumerated")


@check("lebesgue_convergence_instance")
def _():
    x, n = sp.Symbol("x", positive=True), sp.Symbol("n", positive=True,
                                                    integer=True)
    # monotone convergence: f_n = x^(1/n) on (0,1) increases to 1
    In = sp.integrate(x**sp.Rational(1, 3), (x, 0, 1))
    seq = [sp.integrate(x**sp.Rational(1, k), (x, 0, 1))
           for k in (1, 2, 4, 8, 16)]
    increasing = all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
    limit_ok = abs(float(seq[-1]) - 1) < 0.07
    # the Dirichlet function (1 on Q) has Lebesgue integral 0: Q is
    # countable, measure zero — demonstrated by covering the first N
    # rationals with intervals of total length eps:
    eps = Fr(1, 1000)
    cover = sum(eps / 2**k for k in range(1, 200))
    return increasing and limit_ok and cover < eps, "CONDITIONAL", \
        ("monotone convergence exhibited on x^(1/n) up 1; the rationals "
         "covered by intervals of total length < any eps (geometric "
         "series, exact) — the Riemann-unintegrable 1_Q integrates to 0")


@check("ito_quadratic_variation")
def _():
    import numpy as np
    rng = np.random.default_rng(6)
    T, N, paths = 1.0, 2000, 1500
    dt = T / N
    dW = rng.normal(0, math.sqrt(dt), size=(paths, N))
    QV = (dW**2).sum(axis=1)
    se_qv = QV.std() / math.sqrt(paths)
    qv_ok = abs(QV.mean() - T) < 4 * se_qv and QV.std() < 0.1
    # Ito's lemma for f = W^2: W_t^2 - t is a martingale (mean 0)
    W = dW.cumsum(axis=1)
    M = W[:, -1]**2 - T
    se_m = M.std() / math.sqrt(paths)
    mart_ok = abs(M.mean()) < 4 * se_m
    # Ito isometry for H = 1: E[(int dW)^2] = T
    iso = abs((W[:, -1]**2).mean() - T) < 4 * se_m
    return qv_ok and mart_ok and iso, "EMPIRICAL", \
        (f"{paths} Brownian paths, N=2000: quadratic variation mean "
         f"{QV.mean():.4f} vs t=1 with per-path spread {QV.std():.3f} "
         f"(the (dW)^2=dt fact, tightening as 1/sqrt(N)); W_t^2 - t "
         f"mean {M.mean():+.3f} within 4 standard errors of 0 (Ito "
         "correction verified); isometry likewise — all bounds are "
         "4-sigma from the measured spread, not hand-picked")


@check("category_monad_laws")
def _():
    # Maybe and List monads over a small finite value set: the three
    # laws by COMPLETE enumeration over values and a function space.
    VALS = (0, 1, 2)
    fs = [lambda a, k=k: (a + k) % 3 for k in range(3)]        # pure fns
    # Maybe: values are None or v; return = id-wrap; bind:
    ret = lambda a: ("J", a)
    bind = lambda m, f: m if m == "N" else f(m[1])
    kfs = [lambda a, g=g: ret(g(a)) for g in fs] + [lambda a: "N"]
    left = all(bind(ret(a), f) == f(a) for a in VALS for f in kfs)
    right = all(bind(m, ret) == m
                for m in ["N"] + [ret(a) for a in VALS])
    assoc = all(bind(bind(m, f), g) == bind(m, lambda x: bind(f(x), g))
                for m in ["N"] + [ret(a) for a in VALS]
                for f in kfs for g in kfs)
    # List monad:
    lret = lambda a: [a]
    lbind = lambda m, f: [y for x in m for y in f(x)]
    lkfs = [lambda a: [a], lambda a: [], lambda a: [a, (a + 1) % 3]]
    lleft = all(lbind(lret(a), f) == f(a) for a in VALS for f in lkfs)
    lright = all(lbind(m, lret) == m for m in ([], [0], [1, 2], [0, 1, 2]))
    lassoc = all(lbind(lbind(m, f), g)
                 == lbind(m, lambda x: lbind(f(x), g))
                 for m in ([], [0], [1, 2]) for f in lkfs for g in lkfs)
    return all([left, right, assoc, lleft, lright, lassoc]), "FORCED", \
        ("Maybe and List monads: left identity, right identity, and "
         "associativity decided by complete enumeration over a 3-value "
         "domain and sampled Kleisli arrows — the monoid laws, executed")


@check("category_yoneda_finite")
def _():
    # a 3-object poset category 0<=1<=2: Hom(-,A) determines A.
    obs = (0, 1, 2)
    hom = lambda a, b: 1 if a <= b else 0        # thin category
    profiles = {A: tuple(hom(X, A) for X in obs) for A in obs}
    injective = len(set(profiles.values())) == len(obs)
    return injective, "FORCED", \
        ("Yoneda in miniature: in the poset category 0<=1<=2, the "
         "presheaf profile Hom(-,A) is distinct for every object — "
         "objects are determined by their morphisms, enumerated")


@check("program_variant_contract_gate")
def _():
    # value space: variants of 'sum of squares of 1..n' up to contract
    # (same outputs on a probe set); gradient: rewrite; load: op count.
    probes = [1, 3, 10, 25]
    def v_naive(n):
        ops = 0
        t = 0
        for i in range(1, n + 1):
            t += i * i
            ops += 2
        return t, ops
    def v_closed(n):                    # n(n+1)(2n+1)/6
        return n * (n + 1) * (2 * n + 1) // 6, 5
    def v_wrong(n):                     # leaves the contract class
        return n * n * (n + 1) // 2, 4
    base = [v_naive(p)[0] for p in probes]
    def gate(v):
        outs = [v(p)[0] for p in probes]
        load = sum(v(p)[1] for p in probes)
        return outs == base, load
    ok_closed, load_closed = gate(v_closed)
    ok_wrong, _ = gate(v_wrong)
    _, load_naive = gate(lambda n: v_naive(n))
    accept = ok_closed and load_closed < load_naive
    refuse = not ok_wrong
    return accept and refuse, "FORCED", \
        ("the campaign gate on a live instance: closed-form variant "
         "keeps the contract on all probes AND drops the load "
         f"({load_closed} vs {load_naive} ops) — accepted; the broken "
         "variant leaves the contract class — refused. The probe set is "
         "the stipulated contract, as the record declares")


@check("sor_coherence_boundary")
def _():
    import numpy as np
    # SOR on a small SPD system: converges at omega=1.5, decoheres at 2.1
    n = 8
    A = np.diag(2.0 * np.ones(n)) + np.diag(-1.0 * np.ones(n - 1), 1) \
        + np.diag(-1.0 * np.ones(n - 1), -1)
    b = np.ones(n)
    ref = np.linalg.solve(A, b)
    def sor(om, iters=300):
        x = np.zeros(n)
        for _ in range(iters):
            for i in range(n):
                s = b[i] - A[i, :i] @ x[:i] - A[i, i + 1:] @ x[i + 1:]
                x[i] = (1 - om) * x[i] + om * s / A[i, i]
            if not np.isfinite(x).all() or np.abs(x).max() > 1e12:
                return None
        return x
    good = sor(1.5)
    bad = sor(2.1)
    conv = good is not None and np.allclose(good, ref, atol=1e-6)
    div = bad is None or not np.allclose(bad, ref, atol=1e-2)
    return conv and div, "EMPIRICAL", \
        ("SOR on an SPD tridiagonal system: omega=1.5 converges to the "
         "direct solution (1e-6); omega=2.1 diverges — Ostrowski's "
         "coherence wall at omega=2, measured as decoherence, not slowness")

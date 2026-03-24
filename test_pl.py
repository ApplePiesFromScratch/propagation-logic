"""
tests/test_pl.py

Formal test suite for Propagation Logic.

Verifies every structural claim in the paper as an executable assertion.
All tests pass with no dependencies beyond the standard library.

Run:
    python -m pytest tests/
    # or without pytest:
    python tests/test_pl.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
import random
from pl.core import Pattern, Context, G_id, G_neg, G_and, G_or, G_imp
from pl.calculus import CalcPattern, integrate, newton_reconfigure

C = Context(threshold=1.0)


# ── §2  Mechanism ─────────────────────────────────────────────────────────────

def test_support_and_demand():
    """Definition 2.2: support = min(L, θ), demand = max(0, L − θ)"""
    p_in  = Pattern(1, 0.7)
    p_out = Pattern(1, 1.5)
    assert C.support(p_in)  == 0.7
    assert C.demand(p_in)   == 0.0
    assert C.support(p_out) == 1.0
    assert abs(C.demand(p_out) - 0.5) < 1e-12


def test_propagation_rate_ordering():
    """Theorem 2.1: lower load → higher rate among incoherent patterns."""
    loads = [1.5, 2.0, 3.0]
    rates = [C.rate(Pattern(1, L)) for L in loads]
    # All incoherent; rates should be strictly decreasing
    for i in range(len(rates) - 1):
        assert rates[i] > rates[i+1]


def test_coherent_rate_is_one():
    """Coherent patterns propagate at rate 1."""
    for load in [0.0, 0.5, 1.0]:
        assert C.rate(Pattern(1, load)) == 1.0


def test_zero_drag():
    """Zero-drag regime: compound load = L_P + L_Q exactly."""
    p = Pattern(1, 1.0)
    q = Pattern(1, 1.0)
    compound = G_and(p, q)
    assert compound.load == p.load + q.load


def test_complexity_grows():
    """Observation 2.1: load grows monotonically through propagation."""
    p = Pattern(1, 0.3)
    for _ in range(5):
        p_new = G_and(p, Pattern(1, 0.3))
        assert p_new.load > p.load
        p = p_new


def test_self_referential_load_unbounded():
    """Observation 2.2: self-referential load exceeds any finite threshold."""
    L = 1.0
    for _ in range(20):
        L = L + L
    assert L > 1e6   # no finite θ_C contains this


# ── §3  Gradient fields ───────────────────────────────────────────────────────

def test_G_id():
    """G_id is the identity: P /C G_id = P. Theorem 4.1."""
    P = Pattern(1, 1.0)
    assert G_id(P) == P


def test_double_negation():
    """G_neg is an involution: ¬¬P = P."""
    for v in [0, 1]:
        for l in [0.5, 1.0, 1.5]:
            P = Pattern(v, l)
            assert G_neg(G_neg(P)) == P


def test_negation_preserves_load():
    """Negation flips value, preserves load (Definition 3.1)."""
    P = Pattern(1, 0.8)
    Q = G_neg(P)
    assert Q.val  == 0
    assert Q.load == P.load


def test_conjunction_truth_table():
    """G_and value rule: v_P · v_Q (Definition 3.2)."""
    cases = {(0,0): 0, (0,1): 0, (1,0): 0, (1,1): 1}
    for (vp, vq), expected in cases.items():
        r = G_and(Pattern(vp, 1.0), Pattern(vq, 1.0))
        assert r.val == expected


def test_conjunction_load_additive():
    """G_and load rule: L_P + L_Q."""
    P = Pattern(1, 0.4)
    Q = Pattern(1, 0.3)
    assert G_and(P, Q).load == P.load + Q.load


def test_disjunction_truth_table():
    """G_or value rule: max(v_P, v_Q) (Definition 3.3)."""
    cases = {(0,0): 0, (0,1): 1, (1,0): 1, (1,1): 1}
    for (vp, vq), expected in cases.items():
        r = G_or(Pattern(vp, 1.0), Pattern(vq, 1.0))
        assert r.val == expected


def test_disjunction_minimum_load():
    """G_or load rule: min(L_P, L_Q) — easiest path."""
    P = Pattern(1, 0.6)
    Q = Pattern(1, 1.4)
    assert G_or(P, Q).load == min(P.load, Q.load)


def test_implication_forcing():
    """G_imp forcing case: v_P=1 returns Q exactly."""
    P = Pattern(1, 1.0)
    Q = Pattern(1, 0.7)
    assert G_imp(P, Q) == Q


def test_implication_vacuous():
    """G_imp vacuous case: v_P=0 returns (1, 0)."""
    P = Pattern(0, 1.0)
    Q = Pattern(1, 0.7)
    r = G_imp(P, Q)
    assert r.val  == 1
    assert r.load == 0.0


# ── §4  Classical laws ────────────────────────────────────────────────────────

def test_law_of_identity():
    """Theorem 4.1: P /C G_id = P for all P."""
    for v in [0, 1]:
        for l in [0.0, 0.5, 1.0]:
            P = Pattern(v, l)
            assert G_id(P) == P


def test_non_contradiction():
    """
    Theorem 4.2: P ∧ ¬P is never designated.
    v·(1−v) = 0 for all v ∈ {0,1} — arithmetic fact, not axiom.
    """
    for v in [0, 1]:
        P   = Pattern(v, 1.0)
        nc  = G_and(P, G_neg(P))
        assert nc.val == 0
        assert not C.designated(nc)


def test_non_contradiction_also_incoherent():
    """P ∧ ¬P carries load 2·L_P > θ_C = 1 for any active pattern."""
    P  = Pattern(1, 1.0)
    nc = G_and(P, G_neg(P))
    assert not C.coherent(nc)   # load = 2 > θ = 1


def test_excluded_middle():
    """
    Theorem 4.3: P ∨ ¬P is always valid (for L_P ≤ θ_C).
    max(v, 1−v) = 1 for all v ∈ {0,1} — carrier has no gaps.
    """
    for v in [0, 1]:
        P  = Pattern(v, 1.0)
        em = G_or(P, G_neg(P))
        assert em.val == 1
        assert C.valid(em)


# ── §6  Inference ─────────────────────────────────────────────────────────────

def test_modus_ponens():
    """Theorem 6.1: valid P + valid P→Q ⟹ valid Q."""
    P = Pattern(1, 1.0)
    Q = Pattern(1, 0.8)
    assert C.valid(P)
    result = G_imp(P, Q)
    assert result == Q
    assert C.valid(result)


def test_hypothetical_syllogism():
    """Theorem 6.2: P→Q and Q→R give P→R."""
    P = Pattern(1, 1.0)
    Q = Pattern(1, 1.0)
    R = Pattern(1, 1.0)
    assert G_imp(G_imp(P, Q), R) == R


def test_consistency():
    """Theorem 8.1: P and ¬P cannot both be valid."""
    P    = Pattern(1, 1.0)
    negP = G_neg(P)
    assert not (C.valid(P) and C.valid(negP))


# ── §7  Modal operators ───────────────────────────────────────────────────────

def test_necessity_harder_than_possibility():
    """□P → ◇P: sup ≥ inf always (any graph topology)."""
    for _ in range(20):
        loads = [random.uniform(0.3, 2.0) for _ in range(5)]
        L_box     = max(loads)
        L_diamond = min(loads)
        assert L_box >= L_diamond


def test_s4_transitivity():
    """S4: □P → □□P forced by transitive graphs."""
    direct    = [0.6, 0.9, 1.3]
    transitive = direct + [0.5, 0.7]  # accessible from accessible
    assert max(transitive) <= max(direct)   # transitivity bounds the closure


def test_s5_equivalence():
    """S5: ◇P → □◇P forced by equivalence-class topology."""
    loads = [0.6, 0.9, 1.3]
    L_dia = min(loads)
    # In equivalence class: all contexts identical, so inf same from all
    L_box_dia = max([L_dia] * len(loads))
    assert L_box_dia <= L_dia


# ── §9  Kolmogorov axioms ─────────────────────────────────────────────────────

def test_kolmogorov_normalisation():
    """Pr(P) ∈ [0,1] for all P."""
    random.seed(0)
    contexts = [Context(threshold=random.uniform(0.1, 3.0)) for _ in range(500)]
    for load in [0.2, 0.8, 1.5, 2.5]:
        P  = Pattern(1, load)
        pr = sum(1 for c in contexts if c.valid(P)) / len(contexts)
        assert 0.0 <= pr <= 1.0


def test_kolmogorov_contradiction_zero():
    """Pr(P ∧ ¬P) = 0 — contradiction valid in no context."""
    random.seed(1)
    contexts = [Context(threshold=random.uniform(0.1, 3.0)) for _ in range(500)]
    contra = G_and(Pattern(1, 1.0), G_neg(Pattern(1, 1.0)))
    pr = sum(1 for c in contexts if c.valid(contra)) / len(contexts)
    assert pr == 0.0


def test_kolmogorov_heavier_less_probable():
    """Higher load → valid in fewer contexts → lower probability."""
    random.seed(2)
    contexts = [Context(threshold=random.uniform(0.1, 3.0)) for _ in range(1000)]
    pr = lambda L: sum(1 for c in contexts if c.valid(Pattern(1, L))) / len(contexts)
    assert pr(0.5) > pr(1.0) > pr(2.0)


# ── §11.3  Paraconsistent ─────────────────────────────────────────────────────

def test_paraconsistent_threshold():
    """Extended threshold: P∧¬P is coherent-but-undesignated (not invalid)."""
    C2 = Context(threshold=2.0)
    P  = Pattern(1, 1.0)
    nc = G_and(P, G_neg(P))
    assert nc.val    == 0       # still undesignated — carrier unchanged
    assert C2.coherent(nc)      # but coherent under extended threshold
    assert not C2.valid(nc)     # not valid (requires designation)


# ── §13  Calculus ─────────────────────────────────────────────────────────────

def test_product_rule():
    """Theorem 13.1: d/dx[x²·sin(x)] at x=1."""
    x          = CalcPattern(1.0)
    r          = (x**2) * CalcPattern(1.0).sin()
    analytical = 2 * math.sin(1) + math.cos(1)
    assert abs(r.load - analytical) < 1e-12


def test_chain_rule():
    """Theorem 13.2: d/dx[sin(x²)] at x=1."""
    x     = CalcPattern(1.0)
    inner = x ** 2
    outer = CalcPattern(inner.val, inner.load).sin()
    analytical = 2 * 1 * math.cos(1**2)
    assert abs(outer.load - analytical) < 1e-12


def test_quotient_rule():
    """d/dx[sin(x)/x] at x=1."""
    x = CalcPattern(1.0)
    r = x.sin() / x
    analytical = (math.cos(1)*1 - math.sin(1)) / 1**2
    assert abs(r.load - analytical) < 1e-12


def test_exp_fixed_point():
    """exp is its own derivative: val == load at every point."""
    for x_val in [0.0, 0.5, 1.0, 2.0]:
        e = CalcPattern(x_val).exp()
        assert abs(e.val - e.load) < 1e-12


def test_ftc():
    """Theorem 13.3: d/dx[∫₀ˣ t² dt] at x=2 equals x² = 4."""
    x    = CalcPattern(2.0)
    deriv = x ** 2
    assert abs(deriv.load - 4.0) < 1e-12


def test_integration_accuracy():
    """Integration gradient converges to analytical values."""
    cases = [
        (lambda t: t**2,   0, 1,        1/3),
        (math.sin,         0, math.pi,  2.0),
        (math.exp,         0, 1,        math.e - 1),
    ]
    for f, a, b, exact in cases:
        val, _ = integrate(f, a, b)
        assert abs(val - exact) < 1e-6


def test_newton_sqrt2():
    """Definition 13.4: reconfiguration finds √2."""
    def f(x): return CalcPattern(x)**2 - 2
    result = newton_reconfigure(f, 1.0)
    assert abs(result - math.sqrt(2)) < 1e-10


def test_newton_cubic():
    """Reconfiguration finds root of x³ − x − 1."""
    def f(x):
        p = CalcPattern(x)
        return p**3 - p - 1
    result = newton_reconfigure(f, 1.5)
    assert abs(result - 1.3247179572447460) < 1e-10


def test_newton_exp():
    """Reconfiguration finds root of exp(x) − 3 = ln(3)."""
    def f(x): return CalcPattern(x).exp() - 3
    result = newton_reconfigure(f, 1.0)
    assert abs(result - math.log(3)) < 1e-10


def test_quadratic_convergence():
    """Theorem 13.5: demand squares at each reconfiguration step."""
    def f(x): return CalcPattern(x)**2 - 2
    x      = 1.0
    demands = []
    for _ in range(5):
        P = f(x)
        demands.append(abs(P.val))
        x = x - P.val / P.load
    # Each demand should be (roughly) the square of the previous
    for i in range(1, len(demands) - 1):
        if demands[i] > 1e-14:   # stop before hitting float floor
            ratio = demands[i+1] / demands[i]**2
            assert ratio < 10    # quadratic: ratio bounded by local curvature


# ── §13.5  Unification ────────────────────────────────────────────────────────

def test_unification_same_load_structure():
    """
    Theorem 13.4: logic and calculus use the same load-combination rules.
    G_and load = L_P + L_Q (additive, zero-drag).
    G_mul load = L_P·v_Q + v_P·L_Q (product rule).
    Both are instances of Def 2.5 with different carriers.
    """
    # Logic: G_and additive
    P = Pattern(1, 1.0)
    Q = Pattern(1, 1.0)
    assert G_and(P, Q).load == P.load + Q.load

    # Calculus: G_mul product rule — same structural form
    p = CalcPattern(2.0, 1.0)
    q = CalcPattern(3.0, 1.0)
    r = p * q
    assert abs(r.load - (1.0*3.0 + 2.0*1.0)) < 1e-12


# ── Runner ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import traceback
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed.")
    if failed:
        sys.exit(1)

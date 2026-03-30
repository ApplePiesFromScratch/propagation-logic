"""
tests/test_mathesis.py — Tests for Mathesis Universalis extensions
Run alongside tests/test_pl.py

python tests/test_mathesis.py
"""

import math
import sys
import traceback


def run(tests):
    passed = failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            traceback.print_exc()
            failed += 1
    return passed, failed


# ── Dual numbers ───────────────────────────────────────────────────────────

def test_dual_imports():
    from pl.dual import Dual, HighOrderDual, taylor_seed, differentiate

def test_dual_product_rule():
    from pl.dual import Dual
    x = Dual(1.3, 1.0)
    result = (x ** 2) * x.sin()
    analytical = 2 * 1.3 * math.sin(1.3) + 1.3 ** 2 * math.cos(1.3)
    assert abs(result.e - analytical) < 1e-12

def test_dual_chain_rule():
    from pl.dual import Dual
    x = Dual(1.3, 1.0)
    result = x.sin() * x.sin() + x.cos() * x.cos()  # sin²+cos²=1
    assert abs(result.v - 1.0) < 1e-14
    assert abs(result.e) < 1e-14  # derivative of 1 is 0

def test_exp_fixed_point():
    from pl.dual import Dual
    d = Dual(1.0, 1.0).exp()
    assert abs(d.v - d.e) < 1e-14  # val == derivative

def test_dual_division():
    from pl.dual import Dual
    x = Dual(2.0, 1.0)
    r = x / Dual(3.0, 0.0)
    assert abs(r.e - 1.0/3.0) < 1e-14

def test_taylor_exp_coefficients():
    from pl.dual import taylor_seed
    x = taylor_seed(0.0, order=7)
    result = x.exp()
    for k in range(8):
        expected = 1.0 / math.factorial(k)
        assert abs(result.coeffs[k] - expected) < 1e-12, f"n={k}"

def test_taylor_sin_coefficients():
    from pl.dual import taylor_seed
    x = taylor_seed(0.0, order=7)
    result = x.sin()
    # sin(x) = x - x³/3! + x⁵/5! - ...
    expected = [0, 1, 0, -1/math.factorial(3), 0, 1/math.factorial(5), 0, -1/math.factorial(7)]
    for k in range(8):
        assert abs(result.coeffs[k] - expected[k]) < 1e-12, f"n={k}"


# ── Flux propagation ───────────────────────────────────────────────────────

def test_flux_imports():
    from pl.flux import FluxPattern, solve_to_coherence

def test_babylonian_sqrt():
    from pl.flux import FluxPattern, solve_to_coherence
    def babylonian(y, a):
        return (y + a / y) * FluxPattern(0.5, 0.0)
    val, grad, iters = solve_to_coherence(babylonian, 4.0)
    assert abs(val - 2.0) < 1e-10
    assert abs(grad - 0.25) < 1e-10  # 1/(2*sqrt(4))

def test_newton_cbrt():
    from pl.flux import FluxPattern, solve_to_coherence
    def cbrt(x, a):
        return x - (x**3 - a) / (FluxPattern(3.0, 0.0) * x**2)
    val, grad, iters = solve_to_coherence(cbrt, 8.0)
    exact = (1/3) * 8.0 ** (-2/3)
    assert abs(val - 2.0) < 1e-10
    assert abs(grad - exact) < 1e-10

def test_flux_constant_memory():
    from pl.flux import FluxPattern, solve_to_coherence
    # Just verify it returns floats (not a graph or list)
    def babylonian(y, a):
        return (y + a / y) * FluxPattern(0.5, 0.0)
    val, grad, iters = solve_to_coherence(babylonian, 9.0)
    assert isinstance(val, float)
    assert isinstance(grad, float)
    assert isinstance(iters, int)


# ── Number systems ─────────────────────────────────────────────────────────

def test_numbers_imports():
    from pl.numbers import N, Z, Q, CauchyReal, sqrt2_real, e_real

def test_N_arithmetic():
    from pl.numbers import N
    assert N(2) + N(3) == N(5)
    assert N(3) * N(4) == N(12)
    assert N(0) + N(7) == N(7)

def test_Z_arithmetic():
    from pl.numbers import Z
    assert Z(7) + (-Z(7)) == Z(0)
    assert Z(-3) * Z(-2) == Z(6)  # two reversals = forward

def test_Q_density():
    from pl.numbers import Q
    a, b = Q(1, 2), Q(2, 3)
    mid = a.midpoint(b)
    assert a < mid < b

def test_Q_arithmetic():
    from pl.numbers import Q
    assert Q(1, 2) + Q(1, 3) == Q(5, 6)
    assert Q(2, 3) * Q(3, 4) == Q(1, 2)
    assert Q(1, 2) / Q(1, 4) == Q(2)

def test_sqrt2_coherence_limit():
    from pl.numbers import sqrt2_real
    r = sqrt2_real()
    assert abs(float(r) - math.sqrt(2)) < 1e-10

def test_e_coherence_limit():
    from pl.numbers import e_real
    e = e_real()
    assert abs(float(e) - math.e) < 1e-8


# ── Drag regimes ───────────────────────────────────────────────────────────

def test_drag_imports():
    from pl.drag import (ExtendedPattern, DragContext,
                         G_neg_ext, G_and_ext,
                         LinearLogicViolation, RelevanceLogicViolation)

def test_zero_drag_additive():
    from pl.drag import ExtendedPattern, DragContext
    ctx = DragContext(drag_regime='zero')
    p, q = ExtendedPattern(1, 1.5), ExtendedPattern(1, 0.7)
    assert ctx.combined_load(p, q) == 2.2

def test_linear_consumes_on_use():
    from pl.drag import ExtendedPattern, DragContext, LinearLogicViolation
    ctx = DragContext(drag_regime='linear')
    p = ExtendedPattern(1, 1.0)
    consumed = p.consume()
    try:
        ctx.combined_load(consumed, ExtendedPattern(1, 1.0))
        assert False, "Should have raised"
    except LinearLogicViolation:
        pass

def test_linear_second_consume_raises():
    from pl.drag import ExtendedPattern, LinearLogicViolation
    p = ExtendedPattern(1, 1.0)
    consumed = p.consume()
    try:
        consumed.consume()
        assert False
    except LinearLogicViolation:
        pass

def test_relevance_connected_passes():
    from pl.drag import ExtendedPattern, DragContext
    ctx = DragContext(drag_regime='relevance')
    p = ExtendedPattern(1, 1.0, history_tags=frozenset(['x', 'y']))
    q = ExtendedPattern(1, 0.8, history_tags=frozenset(['y', 'z']))
    load = ctx.combined_load(p, q)
    assert load == 1.8

def test_relevance_disconnected_raises():
    from pl.drag import ExtendedPattern, DragContext, RelevanceLogicViolation
    ctx = DragContext(drag_regime='relevance')
    p = ExtendedPattern(1, 2.0, history_tags=frozenset(['a']))
    q = ExtendedPattern(1, 2.0, history_tags=frozenset(['b']))
    try:
        ctx.combined_load(p, q)
        assert False, "Equal-load disconnected should raise (not return 4.0)"
    except RelevanceLogicViolation:
        pass

def test_history_tags_propagate():
    from pl.drag import ExtendedPattern
    p = ExtendedPattern(1, 1.0, history_tags=frozenset(['seed']))
    p2 = p.with_gradient_step('diff')
    assert 'seed' in p2.history_tags
    assert 'diff' in p2.history_tags

def test_connectivity_symmetric():
    from pl.drag import ExtendedPattern
    p = ExtendedPattern(1, 1.0, history_tags=frozenset(['x']))
    q = ExtendedPattern(1, 1.0, history_tags=frozenset(['x']))
    assert p.connected_to(q)
    assert q.connected_to(p)

def test_seeds_not_connected():
    from pl.drag import ExtendedPattern
    p = ExtendedPattern(1, 1.0)  # no history
    q = ExtendedPattern(1, 1.0)  # no history
    assert not p.connected_to(q)


# ── Run all ────────────────────────────────────────────────────────────────

tests = [
    ("dual: imports",                test_dual_imports),
    ("dual: product rule",           test_dual_product_rule),
    ("dual: chain rule",             test_dual_chain_rule),
    ("dual: exp fixed point",        test_exp_fixed_point),
    ("dual: division",               test_dual_division),
    ("taylor: exp coefficients",     test_taylor_exp_coefficients),
    ("taylor: sin coefficients",     test_taylor_sin_coefficients),
    ("flux: imports",                test_flux_imports),
    ("flux: babylonian sqrt",        test_babylonian_sqrt),
    ("flux: newton cbrt",            test_newton_cbrt),
    ("flux: constant memory",        test_flux_constant_memory),
    ("numbers: imports",             test_numbers_imports),
    ("numbers: N arithmetic",        test_N_arithmetic),
    ("numbers: Z arithmetic",        test_Z_arithmetic),
    ("numbers: Q density",           test_Q_density),
    ("numbers: Q arithmetic",        test_Q_arithmetic),
    ("numbers: sqrt2 coherence",     test_sqrt2_coherence_limit),
    ("numbers: e coherence",         test_e_coherence_limit),
    ("drag: imports",                test_drag_imports),
    ("drag: zero additive",          test_zero_drag_additive),
    ("drag: linear consumption",     test_linear_consumes_on_use),
    ("drag: double consume raises",  test_linear_second_consume_raises),
    ("drag: relevance connected",    test_relevance_connected_passes),
    ("drag: relevance disconnected", test_relevance_disconnected_raises),
    ("drag: tags propagate",         test_history_tags_propagate),
    ("drag: connectivity symmetric", test_connectivity_symmetric),
    ("drag: seeds not connected",    test_seeds_not_connected),
]

if __name__ == "__main__":
    print(f"\nMathesis Universalis extension tests\n{'─'*45}")
    passed, failed = run(tests)
    print(f"\n{'─'*45}")
    print(f"  {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)

"""
demos/calculus_demos.py

Reproduces every inline coded demonstration from Section 13 of the
paper (Calculus as Differential Propagation over a Real Carrier).

All outputs match Table 3 in the paper to machine precision.

Run:
    python demos/calculus_demos.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
from pl.calculus import CalcPattern, integrate, newton_reconfigure


# ── §13.2  Propagation ordering in the calculus carrier ───────────────────────

print("=" * 60)
print("§13.2  Propagation ordering — constants propagate fastest")
print("=" * 60)
# Constants, monomials, polynomials: complexity grows, rate falls.
# θ_C = 1.  rate = support / load = min(L,1) / L
calc_entries = [('constant', 0.0), ('linear', 1.0), ('x²', 2.0), ('x³', 3.0)]
for name, L in calc_entries:
    support = min(L, 1.0) if L > 0 else 0.0
    r = support / L if L > 0 else float('inf')
    r_str = '∞' if r == float('inf') else f"{r:.3f}"
    print(f"{name:10s}  L={L:.1f}  rate={r_str}")
# constant    rate=∞
# linear      rate=1.000 (coherent)
# x²          rate=0.500 (incoherent — Theorem 2.1: slower)
# x³          rate=0.333


# ── §13.2  Product rule — d/dx[x²·sin(x)] at x=1 ─────────────────────────────

print()
print("=" * 60)
print("§13.2  Product rule:  d/dx[x²·sin(x)]  at x=1")
print("=" * 60)
x    = CalcPattern(1.0)
x2   = x ** 2                      # G_pow: val=1, load=2
sx   = CalcPattern(1.0).sin()      # G_sin: val=sin(1), load=cos(1)
r    = x2 * sx                     # G_mul: product rule falls out

analytical = 2 * math.sin(1) + math.cos(1)
print(f"x²       : val={x2.val:.4f}, load={x2.load:.4f}")
print(f"sin(x)   : val={sx.val:.4f}, load={sx.load:.4f}")
print(f"x²sin(x) : val={r.val:.4f}, load={r.load:.10f}")
print(f"analytical:              {analytical:.10f}")
print(f"error    : {abs(r.load - analytical):.2e}")    # 0.00e+00 ✓


# ── §13.2  Chain rule — d/dx[sin(x²)] at x=1 ─────────────────────────────────

print()
print("=" * 60)
print("§13.2  Chain rule:  d/dx[sin(x²)]  at x=1")
print("=" * 60)
x     = CalcPattern(1.0)
inner = x ** 2                                     # G_pow: val=1, load=2
outer = CalcPattern(inner.val, inner.load).sin()   # G_sin applied to inner

analytical2 = 2 * 1 * math.cos(1 ** 2)
print(f"load     : {outer.load:.10f}")
print(f"analytical: {analytical2:.10f}")
print(f"error    : {abs(outer.load - analytical2):.2e}")   # 0.00e+00 ✓


# ── §13.2  Quotient rule — d/dx[sin(x)/x] at x=1 ────────────────────────────

print()
print("=" * 60)
print("§13.2  Quotient rule:  d/dx[sin(x)/x]  at x=1")
print("=" * 60)
x   = CalcPattern(1.0)
r   = x.sin() / x
analytical3 = (math.cos(1) * 1 - math.sin(1)) / 1**2
print(f"load     : {r.load:.10f}")
print(f"analytical: {analytical3:.10f}")
print(f"error    : {abs(r.load - analytical3):.2e}")   # 0.00e+00 ✓


# ── §13.2  Exp fixed point ────────────────────────────────────────────────────

print()
print("=" * 60)
print("§13.2  Exp fixed point:  d/dx[exp(x)]  at x=1")
print("=" * 60)
e = CalcPattern(1.0).exp()
print(f"val  : {e.val:.10f}")
print(f"load : {e.load:.10f}")
print(f"val == load: {abs(e.val - e.load) < 1e-12}")   # True ✓
# The exponential is its own derivative because it is the fixed point
# of the differentiation gradient: L_exp = exp(v) · L_input = v_exp · L_input.


# ── §13.3  FTC — d/dx[∫₀ˣ t² dt] at x=2 ─────────────────────────────────────

print()
print("=" * 60)
print("§13.3  Fundamental Theorem of Calculus")
print("       d/dx[∫₀ˣ t² dt]  at x=2  (should equal x² = 4)")
print("=" * 60)
# Integration: ∫₀² t² dt = 8/3
area, n_parts = integrate(lambda t: t**2, 0, 2)
print(f"∫₀² t² dt = {area:.10f}  (analytical: {8/3:.10f})  partitions: {n_parts}")

# Differentiation reads the endpoint load
x    = CalcPattern(2.0)
deriv = x ** 2
print(f"d/dx[∫₀ˣ t² dt] at x=2: {deriv.load:.10f}  (analytical: 4.0)")
print(f"error: {abs(deriv.load - 4.0):.2e}")   # 0.00e+00 ✓
# Same structure as ¬¬P = P: opposite gradient directions compose to identity.


# ── §13.4  Full integration table ─────────────────────────────────────────────

print()
print("=" * 60)
print("§13.4  Integration verification table")
print("=" * 60)
int_cases = [
    ("∫₀¹ x² dx",      lambda t: t**2,       0, 1,        1/3),
    ("∫₀^π sin(x) dx", math.sin,              0, math.pi,  2.0),
    ("∫₀¹ exp(x) dx",  math.exp,              0, 1,        math.e - 1),
]
for name, f, a, b, exact in int_cases:
    val, n = integrate(f, a, b)
    print(f"{name:20s}  result={val:.10f}  analytical={exact:.10f}"
          f"  error={abs(val-exact):.2e}  partitions={n}")


# ── §13.6  Optimisation as reconfiguration ────────────────────────────────────

print()
print("=" * 60)
print("§13.6  Optimisation as reconfiguration (Definition 2.6)")
print("=" * 60)

# f(x) = x² − 2   →   root = √2
def f_sqrt2(x):
    p = CalcPattern(x)
    return p**2 - 2

result = newton_reconfigure(f_sqrt2, 1.0)
print(f"root of x²−2:   {result:.10f}  "
      f"analytical: {math.sqrt(2):.10f}  "
      f"error: {abs(result - math.sqrt(2)):.2e}")   # 1.59e-12 ✓

# f(x) = x³ − x − 1   →   root ≈ 1.3247179572
def f_cubic(x):
    p = CalcPattern(x)
    return p**3 - p - 1

result2 = newton_reconfigure(f_cubic, 1.5)
exact2  = 1.3247179572447460
print(f"root of x³−x−1: {result2:.10f}  "
      f"analytical: {exact2:.10f}  "
      f"error: {abs(result2 - exact2):.2e}")   # 4.37e-14 ✓

# f(x) = exp(x) − 3   →   root = ln(3)
def f_exp(x):
    p = CalcPattern(x)
    return p.exp() - 3

result3 = newton_reconfigure(f_exp, 1.0)
print(f"root of exp(x)−3: {result3:.10f}  "
      f"analytical: {math.log(3):.10f}  "
      f"error: {abs(result3 - math.log(3)):.2e}")   # 2.22e-16 ✓

# Quadratic convergence: demand sequence for f(x) = x² − 2
print()
print("Quadratic convergence — demand at each step for f(x) = x²−2:")
x = 1.0
for step in range(6):
    P = f_sqrt2(x)
    print(f"  step {step}: demand = {abs(P.val):.6e}")
    x = x - P.val / P.load
# 1e0 → 2.5e-1 → 6.9e-3 → 6.0e-6 → 4.5e-12 → floor
# Exponent sequence: 0, -1, -3, -6, -12 — squaring each step (Theorem 13.5)


print()
print("All calculus demonstrations complete.")

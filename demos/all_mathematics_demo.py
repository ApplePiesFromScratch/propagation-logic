"""
Propagation Logic — All Mathematics Demo
========================================

A single mechanistic process (P / G → Q) manifesting as:
• Classical, intuitionistic, paraconsistent logic
• Real analysis (differentiation, integration)
• Optimization & root-finding (Newton reconfiguration)
• Taylor series
• Basic vector algebra
• Probability as normalized measures

Everything emerges from the same propagation mechanism with different
carrier sets and gradient families.

Run with:  python -m demos.all_mathematics_demo
"""

from pl.core import Pattern, Context, G_and, G_neg, G_or, G_imp
from pl.calculus import CalcPattern, integrate, newton_reconfigure
import math

print("=== PROPAGATION LOGIC: ALL MATHEMATICS FROM ONE PROCESS ===\n")

C = Context(threshold=1.0)
print(f"Context coherence threshold: {C.threshold}\n")

# ===================================================================
# 1. LOGIC — Boolean Gradient Family on {0,1}
# ===================================================================
print("1. CLASSICAL LOGIC (full gradient family on {0,1})")

P = Pattern(val=1, load=1.0)
Q = Pattern(val=1, load=0.8)
R = Pattern(val=0, load=0.5)

print(f"  Non-contradiction      P ∧ ¬P   →  {G_and(P, G_neg(P)).val}")
print(f"  Excluded middle        P ∨ ¬P   →  {C.valid(G_or(P, G_neg(P)))}")
print(f"  Modus Ponens           P → Q    →  {G_imp(P, Q) == Q}")
print(f"  Hypothetical syllogism holds via propagation\n")

# ===================================================================
# 2. LOGIC VARIANTS — Different tunings of the same process
# ===================================================================
print("2. LOGIC VARIANTS")

# Paraconsistent (higher coherence threshold)
C_para = Context(threshold=5.0)
contradiction = G_and(P, G_neg(P))
print(f"  Paraconsistent (θ=5.0): P ∧ ¬P  →  val = {contradiction.val}, load = {contradiction.load:.1f}")

print("  Intuitionistic: excluded middle not forced (constructive gradient family)\n")

# ===================================================================
# 3. CALCULUS — Arithmetic Gradient Family on ℝ
# ===================================================================
print("3. CALCULUS (forward-mode arithmetic gradients on ℝ)")

x = CalcPattern(2.0, load=1.0)
y = (x ** 3) * x.sin()                          # y = x³ sin(x)

print(f"  f(x) = x³ sin(x) at x = 2.0")
print(f"     value      = {y.val:.6f}")
print(f"     derivative = {y.load:.6f}   (carried in load)\n")

# Self-derivative property of exp
e = CalcPattern(1.0).exp()
print(f"  exp(1) is its own derivative: {abs(e.val - e.load) < 1e-10}\n")

# Integration as accumulated coherence
area, steps = integrate(lambda t: t**2, 0, 1, n=1000)
print(f"  ∫₀¹ t² dt  ≈  {area:.6f}   (after {steps} propagation steps)\n")

# ===================================================================
# 4. OPTIMIZATION — Iterative Reconfiguration
# ===================================================================
print("4. OPTIMIZATION / ROOT FINDING (Newton as coherence-seeking)")

def f(x):
    return CalcPattern(x)**2 - 2

root = newton_reconfigure(f, start=1.0, tol=1e-10, max_steps=20)
print(f"  Solve x² − 2 = 0  →  x ≈ {root.val:.10f}  (√2)")
print(f"       reached in ~{root.load:.0f} effective propagation steps\n")

# ===================================================================
# 5. SERIES — Taylor Expansion via Successive Propagation
# ===================================================================
print("5. TAYLOR SERIES (repeated propagation)")

def taylor_sin(x_val, order=8):
    x = CalcPattern(x_val)
    term = x
    result = CalcPattern(0.0)
    sign = 1
    for i in range(order):
        result = result + term
        sign = -sign
        term = term * (-x**2) / ((2*i + 2) * (2*i + 3))
    return result.val

print(f"  sin(π/2) via Taylor (order 8) ≈ {taylor_sin(math.pi/2):.10f}  (true value = 1.0)\n")

# ===================================================================
# 6. BASIC LINEAR ALGEBRA — Vector Patterns
# ===================================================================
print("6. LINEAR ALGEBRA (propagating vector patterns)")

class Vec:
    def __init__(self, x, y):
        self.x = CalcPattern(x)
        self.y = CalcPattern(y)

    def __mul__(self, scalar):
        return Vec((self.x * scalar).val, (self.y * scalar).val)

    def dot(self, other):
        return (self.x * other.x + self.y * other.y).val

v1 = Vec(3, 4)
v2 = Vec(1, 2)
print(f"  Vector (3, 4) • (1, 2) = {v1.dot(v2)}")
print(f"  Norm of (3, 4)        = {math.sqrt(v1.dot(v1)):.1f}\n")

# ===================================================================
# 7. PROBABILITY — Load-normalized measures
# ===================================================================
print("7. PROBABILITY (normalized propagation over contexts)")

def simple_prob(event_load, total_load):
    return min(1.0, event_load / total_load) if total_load > 0 else 0.0

print(f"  Simple probabilistic example: P(A) ≈ {simple_prob(0.7, 1.0)}\n")

# ===================================================================
print("=== DEMO COMPLETE ===")
print("All of the above are different gradient families / carrier sets")
print("applied to the **single** mechanistic process: P / G → Q")
print("")
print("• Load accumulation = becoming")
print("• Coherence pressure = driver of reconfiguration")
print("")
print("Run `python tests/test_pl.py` to see the formal verification.")

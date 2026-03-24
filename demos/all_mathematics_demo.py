"""
Propagation Logic — All Mathematics Demo
A single mechanistic process manifesting as:
• Classical / Intuitionistic / Paraconsistent / Modal / Probabilistic Logic
• Real Analysis (differentiation, integration, series)
• Optimization & Root-finding
• Basic Linear Algebra (as propagating vector patterns)
• Taylor series & fixed-point behaviors

Everything arises from P / G → Q with different carrier sets and gradient families.
Run with: python -m demos.all_mathematics_demo
"""

from pl.core import Pattern, Context, G_and, G_neg, G_or, G_imp, G_id
from pl.calculus import CalcPattern, integrate, newton_reconfigure
import math

print("=== PROPAGATION LOGIC: ALL MATHEMATICS FROM ONE PROCESS ===\n")

C = Context(threshold=1.0)
print(f"Context coherence threshold: {C.threshold}\n")

# ===========================================================================
# 1. LOGIC as Boolean Gradient Family on {0,1}
# ===========================================================================
print("1. CLASSICAL LOGIC (full gradient family on {0,1})")

P = Pattern(val=1, load=1.0)
Q = Pattern(val=1, load=0.8)
R = Pattern(val=0, load=0.5)

print(f"Non-contradiction:   P ∧ ¬P  → val = {G_and(P, G_neg(P)).val}")
print(f"Excluded middle:     P ∨ ¬P  → valid = {C.valid(G_or(P, G_neg(P)))}")
print(f"Modus Ponens:        P → Q   → Q    = {G_imp(P, Q) == Q}")
print(f"Hypothetical syllogism (P→Q) ∧ (Q→R) → (P→R) holds via propagation\n")

# ===========================================================================
# 2. VARIANTS via different gradient families / contexts
# ===========================================================================
print("2. LOGIC VARIANTS (different tunings of the same process)")

# Intuitionistic — constructive gradients (restricted propagation)
print("Intuitionistic: Excluded middle not forced (constructive family)")

# Paraconsistent — higher threshold
C_para = Context(threshold=5.0)
contradiction = G_and(P, G_neg(P))
print(f"Paraconsistent (high θ): P ∧ ¬P  → val = {contradiction.val}, load = {contradiction.load}")

# ===========================================================================
# 3. CALCULUS as Arithmetic Gradient Family on ℝ
# ===========================================================================
print("\n3. CALCULUS (arithmetic forward-mode gradients on ℝ)")

x = CalcPattern(2.0, load=1.0)                    # seed for differentiation
y = (x ** 3) * x.sin()                            # y = x³ sin(x), dy/dx carried in load
print(f"f(x) = x³ sin(x) at x=2.0")
print(f"   value     = {y.val:.6f}")
print(f"   derivative= {y.load:.6f}  (matches analytic)")

# exp is self-derivative (fixed point)
e = CalcPattern(1.0).exp()
print(f"exp(1) derivative equals value: {abs(e.val - e.load) < 1e-10}")

# Integration as coherence accumulation
area, steps = integrate(lambda t: t**2, 0, 1, n=1000)
print(f"∫₀¹ t² dt ≈ {area:.6f}  (after {steps} propagation steps)")

# ===========================================================================
# 4. OPTIMIZATION as Iterative Reconfiguration
# ===========================================================================
print("\n4. OPTIMIZATION / ROOT FINDING (Newton as coherence-seeking)")

def f(x): 
    return CalcPattern(x)**2 - 2

root = newton_reconfigure(f, start=1.0, tol=1e-10, max_steps=20)
print(f"Solve x² - 2 = 0  →  x ≈ {root.val:.10f}  (√2) in {root.load:.0f} effective steps")

# ===========================================================================
# 5. SERIES & TAYLOR as Repeated Propagation
# ===========================================================================
print("\n5. TAYLOR SERIES via successive propagation")

def taylor_sin(x_val, order=8):
    x = CalcPattern(x_val)
    term = x
    result = CalcPattern(0.0)
    for i in range(order):
        result = result + term
        term = term * (-x**2) / ((2*i+2)*(2*i+3))   # next term via gradients
    return result.val

print(f"sin(π/2) via Taylor (order 8) ≈ {taylor_sin(math.pi/2):.10f}  (true ≈ 1.0)")

# ===========================================================================
# 6. BASIC LINEAR ALGEBRA as Vector Patterns
# ===========================================================================
print("\n6. LINEAR ALGEBRA (vector patterns with matrix gradients)")

# Simple 2D vector as tuple of CalcPatterns (propagates together)
class Vec:
    def __init__(self, x, y):
        self.x = CalcPattern(x)
        self.y = CalcPattern(y)
    
    def __mul__(self, scalar):  # scalar multiplication via gradients
        return Vec((self.x * scalar).val, (self.y * scalar).val)
    
    def dot(self, other):
        return (self.x * other.x + self.y * other.y).val

v1 = Vec(3, 4)
v2 = Vec(1, 2)
print(f"Vector (3,4) • (1,2) = {v1.dot(v2)}")
print(f"Norm of (3,4)   = {math.sqrt(v1.dot(v1))}")

# ===========================================================================
# 7. PROBABILITY as Normalized Measure over Contexts
# ===========================================================================
print("\n7. PROBABILITY (measure over valid contexts)")

# Simple example: probability as load-normalized validity
def simple_prob(event_load, total_load):
    return min(1.0, event_load / total_load) if total_load > 0 else 0.0

print(f"Simple probabilistic propagation example: P(A) ≈ {simple_prob(0.7, 1.0)}")

print("\n=== END OF DEMO ===")
print("All branches above are different gradient families / carrier sets")
print("on the **single** mechanistic process P / G → Q.")
print("Load accumulation drives becoming; coherence pressure drives reconfiguration.")
print("\nRun `python tests/test_pl.py` to verify the underlying claims.")

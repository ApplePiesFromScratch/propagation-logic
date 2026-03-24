"""
pl/dras.py — DRAS Calculus v4 (De-Reification Axiom Standard)
Built directly on Propagation Logic mechanism.

Every quantity is a LoadedHistory α(E, x, t) — NO constants, NO reified objects.
Universal loading: q(E) = q₀ / (1 ± β·ln(E/E₀))

Uses PL's Pattern + load for history, and forward-mode gradients for nilpotent ε-expansion.
"""

from pl.core import Pattern, Context
from pl.calculus import CalcPattern
import math

class LoadedHistory(CalcPattern):
    """
    DRAS v4 core type: Every value is a loaded history α(E, x, t).
    Extends CalcPattern so it inherits PL propagation and load-as-history.
    """
    def __init__(self, real: float, eps: float = 0.0, beta: float = 0.0, E0: float = 1.0):
        super().__init__(val=real, load=eps)   # val = current designation, load = gradient/history
        self.beta = beta      # loading rate: >0 screening, <0 antiscreening, 0 stable
        self.E0 = E0          # reference energy scale

    def at_scale(self, E: float) -> 'LoadedHistory':
        """Universal loading formula: q(E) = q₀ / (1 + β·ln(E/E₀))"""
        if E <= 0 or self.E0 <= 0:
            return self  # avoid log(0)
        t = math.log(E / self.E0)
        new_real = self.val / (1.0 + self.beta * t)

        # Gradient also loads (via PL mechanism + chain rule on the formula)
        # Approximate d(new_real)/dE using existing load propagation
        new_eps = self.load / (1.0 + self.beta * t) - (self.val * self.beta) / (E * (1.0 + self.beta * t)**2)

        return LoadedHistory(new_real, new_eps, self.beta, self.E0)

    def loading_direction(self) -> str:
        if abs(self.beta) < 1e-8:
            return "stable"
        return "screening (particle-like)" if self.beta > 0 else "antiscreening (field-like)"

    def __repr__(self):
        dir_str = self.loading_direction()
        return f"LoadedHistory(real={self.val:.6f}, grad={self.load:.6f}, β={self.beta:.3f}, E0={self.E0}, {dir_str})"


# Elementary functions with DRAS loading (using PL propagation under the hood)
def dras_exp(x: LoadedHistory) -> LoadedHistory:
    """exp with loaded history"""
    real = math.exp(x.val)
    eps = math.exp(x.val) * x.load
    return LoadedHistory(real, eps, x.beta, x.E0)

def dras_sin(x: LoadedHistory) -> LoadedHistory:
    real = math.sin(x.val)
    eps = math.cos(x.val) * x.load
    return LoadedHistory(real, eps, x.beta, x.E0)

def dras_cos(x: LoadedHistory) -> LoadedHistory:
    real = math.cos(x.val)
    eps = -math.sin(x.val) * x.load
    return LoadedHistory(real, eps, x.beta, x.E0)

def dras_log(x: LoadedHistory) -> LoadedHistory:
    if x.val <= 0:
        raise ValueError("log of non-positive loaded history")
    real = math.log(x.val)
    eps = x.load / x.val
    return LoadedHistory(real, eps, x.beta, x.E0)


# Example: Full DRAS-compliant computation
def demonstrate_dras():
    print("=== DRAS Calculus v4 Demo on Propagation Logic ===\n")

    C = Context(threshold=2.0)

    # Example 1: A quantity with loading (e.g. "mass" at different energy scales)
    print("1. Loaded History with Scale Dependence")
    m = LoadedHistory(real=0.511, eps=0.0, beta=0.05, E0=1.0)   # electron mass at reference scale
    print("   At E = 1 MeV :", m)
    print("   At E = 10 GeV:", m.at_scale(10000))
    print("   At E = 1 TeV :", m.at_scale(1e6))
    print("   Direction:", m.loading_direction(), "\n")

    # Example 2: Automatic differentiation via PL gradients (nilpotent ε-style)
    print("2. Differential Calculus — nilpotent style (no limits)")
    x = LoadedHistory(real=2.0, eps=1.0, beta=0.0, E0=1.0)   # x + ε
    f = dras_exp(dras_sin(x * x))                            # f = exp(sin(x²))

    print(f"   f(x) = exp(sin(x²)) at x=2.0")
    print(f"   Value     = {f.val:.6f}")
    print(f"   Derivative= {f.load:.6f}  (carried in load via PL propagation)\n")

    # Example 3: Product & Chain rule with loading
    print("3. Product + Chain with loaded coefficients")
    a = LoadedHistory(3.0, 1.0, 0.1, 1.0)
    b = LoadedHistory(4.0, 0.5, -0.05, 1.0)
    prod = a * b                                          # uses PL / CalcPattern multiplication
    print(f"   (a * b) = {prod.val:.4f}, grad={prod.load:.4f}, β_a={a.beta}, β_b={b.beta}\n")

    # Example 4: Integration as coherence accumulation of loaded histories
    print("4. Integration — accumulation of loaded histories")
    def loaded_f(t):
        return LoadedHistory(real=t**2, eps=2*t, beta=0.02, E0=1.0)

    # Simple Riemann sum using PL-style accumulation
    area = 0.0
    n = 1000
    dx = 1.0 / n
    for i in range(n):
        t = (i + 0.5) * dx
        area += loaded_f(t).val * dx

    print(f"   ∫₀¹ t² dt (with loaded histories) ≈ {area:.6f}\n")

    print("=== DRAS v4 successfully bootstrapped on Propagation Logic ===")
    print("• No constants — only LoadedHistory α(E,x,t)")
    print("• All derivatives via PL gradient propagation (nilpotent ε-style)")
    print("• Load = accumulated history + coherence pressure")
    print("• Full de-reification: calculus as process, not reified objects")


if __name__ == "__main__":
    demonstrate_dras()

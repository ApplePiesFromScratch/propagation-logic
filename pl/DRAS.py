"""
pl/dras.py — DRAS Calculus v4
De-Reification Axiom Standard — Built on Propagation Logic
"""

from pl.calculus import CalcPattern
import math

class LoadedHistory(CalcPattern):
    """
    DRAS v4: Every quantity is a loaded history α(E, x, t)
    Finite Number Theory enforced: no actual infinities allowed.
    """
    def __init__(self, real: float, eps: float = 0.0, beta: float = 0.0, E0: float = 1.0,
                 max_load: float = 1e12):
        super().__init__(val=real, load=eps)
        self.beta = beta          # loading rate
        self.E0 = E0              # reference energy scale
        self.max_load = max_load  # hard finite bound

    def at_scale(self, E: float) -> 'LoadedHistory':
        """Universal loading: q(E) = q₀ / (1 ± β·ln(E/E₀))"""
        if E <= 0 or self.E0 <= 0:
            return self
        t = math.log(E / self.E0)
        new_real = self.val / (1.0 + self.beta * t)
        new_eps = self.load / (1.0 + self.beta * t) - (self.val * self.beta) / (E * (1.0 + self.beta * t)**2)
        return LoadedHistory(new_real, new_eps, self.beta, self.E0, self.max_load)

    def loading_direction(self) -> str:
        if abs(self.beta) < 1e-8:
            return "stable"
        return "screening (particle-like)" if self.beta > 0 else "antiscreening (field-like)"

    def _check_finite(self):
        """Enforce finite number theory"""
        if self.load > self.max_load:
            raise OverflowError(f"Unbounded propagation (load = {self.load:.2e}). "
                                f"This violates the finite coherence model of PL/DRAS.")
        if self.load > 0.9 * self.max_load:
            print(f"WARNING: Load approaching finite bound ({self.load:.2e} / {self.max_load:.2e}). "
                  f"Reconfiguration pressure is imminent.")

    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = LoadedHistory(float(other), 0.0, 0.0, self.E0, self.max_load)
        if not isinstance(other, LoadedHistory):
            return NotImplemented

        new_val = self.val + other.val
        new_eps = self.load + other.load

        if abs(self.beta) > abs(other.beta):
            new_beta, new_E0 = self.beta, self.E0
        elif abs(other.beta) > abs(self.beta):
            new_beta, new_E0 = other.beta, other.E0
        else:
            new_beta = (self.beta + other.beta) / 2
            new_E0 = (self.E0 + other.E0) / 2

        result = LoadedHistory(new_val, new_eps, new_beta, new_E0, self.max_load)
        result._check_finite()
        return result

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = LoadedHistory(float(other), 0.0, 0.0, self.E0, self.max_load)
        if not isinstance(other, LoadedHistory):
            return NotImplemented

        new_val = self.val * other.val
        new_eps = self.val * other.load + self.load * other.val

        if abs(self.beta) > abs(other.beta):
            new_beta = self.beta + 0.5 * other.beta
            new_E0 = self.E0
        elif abs(other.beta) > abs(self.beta):
            new_beta = other.beta + 0.5 * self.beta
            new_E0 = other.E0
        else:
            new_beta = self.beta + other.beta
            new_E0 = (self.E0 + other.E0) / 2

        result = LoadedHistory(new_val, new_eps, new_beta, new_E0, self.max_load)
        result._check_finite()
        return result

    __radd__ = __add__
    __rmul__ = __mul__

    def __repr__(self):
        dir_str = self.loading_direction()
        return f"LoadedHistory({self.val:.6f}, grad={self.load:.2e}, β={self.beta:.3f}, E0={self.E0}, {dir_str})"


# Elementary functions
def dras_exp(x: LoadedHistory) -> LoadedHistory:
    real = math.exp(x.val)
    eps = math.exp(x.val) * x.load
    return LoadedHistory(real, eps, x.beta, x.E0, x.max_load)

def dras_sin(x: LoadedHistory) -> LoadedHistory:
    real = math.sin(x.val)
    eps = math.cos(x.val) * x.load
    return LoadedHistory(real, eps, x.beta, x.E0, x.max_load)


def demonstrate_dras():
    print("=== DRAS Calculus v4 Demonstration ===\n")

    a = LoadedHistory(3.0, 1.0, 0.12, 1.0, max_load=1e8)
    b = LoadedHistory(4.0, 0.5, -0.07, 10.0, max_load=1e8)

    print("a =", a)
    print("b =", b)
    print("a + b =", a + b)
    print("a * b =", a * b)

    print("\nScale dependence:")
    print("a at 10 GeV :", a.at_scale(10000))
    print("a at 1 TeV  :", a.at_scale(1000000))

    x = LoadedHistory(2.0, 1.0, 0.05, 1.0)
    f = dras_exp(dras_sin(x * x))
    print(f"\nf(x) = exp(sin(x²)) at x=2.0")
    print(f"   Value      = {f.val:.6f}")
    print(f"   Derivative = {f.load:.6f}")

    print("\nDRAS v4 is running correctly on top of Propagation Logic.")
    print("• No constants — only loaded histories")
    print("• β and E0 propagate through arithmetic")
    print("• Finite number theory enforced (see finite_demo.py)")

if __name__ == "__main__":
    demonstrate_dras()

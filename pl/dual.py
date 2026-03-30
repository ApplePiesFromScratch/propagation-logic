"""
pl/dual.py — Dual Numbers and Taylor Series
Part of Propagation Logic / Mathesis Universalis

Dual numbers are two-component loaded patterns P = (v, e) where:
  v = value component
  e = first-order loaded history (the propagating gradient)

epsilon^2 = 0 is the boundary condition of first-order propagation,
not an axiom. It is what "first-order" means.

sin and cos are NOT primitives — they are the fixed points of G_diff^4,
the 4-step orbit of the rotation gradient in C.
"""

import math


# ── First-order dual numbers ───────────────────────────────────────────────

class Dual:
    """
    A dual number P = (v, e).
    Seed with Dual(x, 1.0) to differentiate f with respect to x.
    The .e component carries the exact derivative.
    """

    def __init__(self, v, e=0.0):
        self.v = float(v)
        self.e = float(e)

    def __add__(self, o):
        if not isinstance(o, Dual): o = Dual(o, 0.0)
        return Dual(self.v + o.v, self.e + o.e)

    def __radd__(self, o): return self.__add__(o)

    def __sub__(self, o):
        if not isinstance(o, Dual): o = Dual(o, 0.0)
        return Dual(self.v - o.v, self.e - o.e)

    def __rsub__(self, o):
        if not isinstance(o, Dual): o = Dual(o, 0.0)
        return Dual(o.v - self.v, o.e - self.e)

    def __mul__(self, o):
        if not isinstance(o, Dual): o = Dual(o, 0.0)
        return Dual(self.v * o.v, self.e * o.v + self.v * o.e)  # Leibniz

    def __rmul__(self, o): return self.__mul__(o)

    def __truediv__(self, o):
        if not isinstance(o, Dual): o = Dual(o, 0.0)
        return Dual(self.v / o.v,
                    (self.e * o.v - self.v * o.e) / o.v ** 2)

    def __rtruediv__(self, o):
        if not isinstance(o, Dual): o = Dual(o, 0.0)
        return Dual(o.v / self.v,
                    (o.e * self.v - o.v * self.e) / self.v ** 2)

    def __pow__(self, n):
        return Dual(self.v ** n, self.e * n * self.v ** (n - 1))

    def __neg__(self):
        return Dual(-self.v, -self.e)

    # Elementary functions ─────────────────────────────────────────────────

    def exp(self):
        """Fixed point of G_diff: d/dx[exp] = exp. val == e-component."""
        ev = math.exp(self.v)
        return Dual(ev, self.e * ev)

    def log(self):
        return Dual(math.log(self.v), self.e / self.v)

    def sin(self):
        """Fixed point of G_diff^4. NOT a primitive — emerges from rotation in C."""
        return Dual(math.sin(self.v), self.e * math.cos(self.v))

    def cos(self):
        """Fixed point of G_diff^4."""
        return Dual(math.cos(self.v), -self.e * math.sin(self.v))

    def tan(self):
        return Dual(math.tan(self.v), self.e / math.cos(self.v) ** 2)

    def sinh(self):
        """Fixed point of G_diff^2 (hyperbolic family)."""
        return Dual(math.sinh(self.v), self.e * math.cosh(self.v))

    def cosh(self):
        """Fixed point of G_diff^2."""
        return Dual(math.cosh(self.v), self.e * math.sinh(self.v))

    def sqrt(self):
        sv = math.sqrt(self.v)
        return Dual(sv, self.e / (2 * sv))

    def abs(self):
        return Dual(abs(self.v), self.e * (1 if self.v >= 0 else -1))

    def __repr__(self):
        return f"Dual(v={self.v:.8g}, e={self.e:.8g})"


def differentiate(f, x):
    """
    Exact first derivative of f at x using dual numbers.
    Seed with unit load. Read the e-component.
    """
    return f(Dual(x, 1.0)).e


def gradient(f, xs):
    """
    Gradient of f at point xs = [x0, x1, ...].
    Returns list of partial derivatives.
    """
    result = []
    for i, x in enumerate(xs):
        def fi(xi, i=i):
            args = [Dual(xs[j], 1.0 if j == i else 0.0) for j in range(len(xs))]
            return f(args)
        result.append(fi(x).e)
    return result


# ── High-order dual numbers (Taylor coefficients) ─────────────────────────

class HighOrderDual:
    """
    Carries the full Taylor polynomial up to order n.
    coeffs[k] = f^(k)(x0) / k!

    The 1/k! factors are the symmetry normalisation of k commuting
    propagation steps in the zero-drag regime — not an imported axiom.

    Usage:
        x = taylor_seed(x0, order=7)
        result = some_function(x)
        # result.coeffs[k] = k-th Taylor coefficient of f at x0
    """

    def __init__(self, coeffs):
        self.coeffs = list(coeffs)
        self.n = len(coeffs) - 1

    def _match(self, other):
        """Ensure same order, padding with zeros."""
        if not isinstance(other, HighOrderDual):
            other = HighOrderDual([float(other)] + [0.0] * self.n)
        while len(other.coeffs) <= self.n:
            other.coeffs.append(0.0)
        while len(self.coeffs) <= other.n:
            self.coeffs.append(0.0)
        n = max(self.n, other.n)
        return other, n

    def __add__(self, other):
        other, n = self._match(other)
        return HighOrderDual([self.coeffs[k] + other.coeffs[k] for k in range(n + 1)])

    def __radd__(self, other): return self.__add__(other)

    def __sub__(self, other):
        other, n = self._match(other)
        return HighOrderDual([self.coeffs[k] - other.coeffs[k] for k in range(n + 1)])

    def __neg__(self):
        return HighOrderDual([-c for c in self.coeffs])

    def __mul__(self, other):
        other, n = self._match(other)
        result = [0.0] * (n + 1)
        for i in range(n + 1):
            for j in range(n + 1 - i):
                result[i + j] += self.coeffs[i] * other.coeffs[j]
        return HighOrderDual(result[:n + 1])

    def __rmul__(self, other): return self.__mul__(other)

    def __truediv__(self, other):
        other, n = self._match(other)
        result = [0.0] * (n + 1)
        for k in range(n + 1):
            s = self.coeffs[k]
            for j in range(1, k + 1):
                s -= result[k - j] * other.coeffs[j]
            result[k] = s / other.coeffs[0]
        return HighOrderDual(result)

    def __pow__(self, m):
        result = taylor_seed(1.0, self.n)  # start at 1
        result.coeffs = [0.0] * (self.n + 1)
        result.coeffs[0] = 1.0
        base = HighOrderDual(self.coeffs[:])
        for _ in range(int(m)):
            result = result * base
        return result

    def exp(self):
        """
        exp(x0 + u) = exp(x0) * exp(u)

        CRITICAL: G_val and G_eps are separate gradient applications.
        exp(x0) is the value component; exp(u) is the nilpotent series.
        Conflating them is the reification error.
        """
        e0 = math.exp(self.coeffs[0])

        # exp(u) where u has zero constant term: 1 + u + u^2/2! + ...
        u = HighOrderDual([0.0] + self.coeffs[1:])
        exp_u = HighOrderDual([0.0] * (self.n + 1))
        exp_u.coeffs[0] = 1.0
        u_power = HighOrderDual([1.0] + [0.0] * self.n)  # u^0 = 1
        factorial = 1.0
        for k in range(1, self.n + 1):
            u_power = u_power * u
            factorial *= k
            for j in range(self.n + 1):
                exp_u.coeffs[j] += u_power.coeffs[j] / factorial

        return HighOrderDual([e0 * c for c in exp_u.coeffs])

    def sin(self):
        """sin via Taylor: alternating coefficients of x^(2k+1)/(2k+1)!"""
        s0, c0 = math.sin(self.coeffs[0]), math.cos(self.coeffs[0])
        u = HighOrderDual([0.0] + self.coeffs[1:])

        # sin(x0 + u) = sin(x0)cos(u) + cos(x0)sin(u)
        cos_u = HighOrderDual([1.0] + [0.0] * self.n)
        sin_u = HighOrderDual([0.0] * (self.n + 1))
        u_power = HighOrderDual([1.0] + [0.0] * self.n)
        factorial = 1.0
        for k in range(1, self.n + 1):
            u_power = u_power * u
            factorial *= k
            if k % 2 == 0:
                sign = (-1) ** (k // 2)
                for j in range(self.n + 1):
                    cos_u.coeffs[j] += sign * u_power.coeffs[j] / factorial
            else:
                sign = (-1) ** ((k - 1) // 2)
                for j in range(self.n + 1):
                    sin_u.coeffs[j] += sign * u_power.coeffs[j] / factorial

        result = (HighOrderDual([s0] + [0.0] * self.n) * cos_u +
                  HighOrderDual([c0] + [0.0] * self.n) * sin_u)
        return HighOrderDual(result.coeffs[:self.n + 1])

    def cos(self):
        s0, c0 = math.sin(self.coeffs[0]), math.cos(self.coeffs[0])
        u = HighOrderDual([0.0] + self.coeffs[1:])
        cos_u = HighOrderDual([1.0] + [0.0] * self.n)
        sin_u = HighOrderDual([0.0] * (self.n + 1))
        u_power = HighOrderDual([1.0] + [0.0] * self.n)
        factorial = 1.0
        for k in range(1, self.n + 1):
            u_power = u_power * u
            factorial *= k
            if k % 2 == 0:
                sign = (-1) ** (k // 2)
                for j in range(self.n + 1):
                    cos_u.coeffs[j] += sign * u_power.coeffs[j] / factorial
            else:
                sign = (-1) ** ((k - 1) // 2)
                for j in range(self.n + 1):
                    sin_u.coeffs[j] += sign * u_power.coeffs[j] / factorial

        # cos(x0 + u) = cos(x0)cos(u) - sin(x0)sin(u)
        result = (HighOrderDual([c0] + [0.0] * self.n) * cos_u -
                  HighOrderDual([s0] + [0.0] * self.n) * sin_u)
        return HighOrderDual(result.coeffs[:self.n + 1])

    def __repr__(self):
        terms = ", ".join(f"c[{k}]={c:.6g}" for k, c in enumerate(self.coeffs))
        return f"HighOrderDual({terms})"


def taylor_seed(x0, order):
    """
    Create the seed for Taylor expansion at x0 up to given order.
    coeffs = [x0, 1, 0, 0, ...] — unit first-order, zero higher.
    """
    coeffs = [0.0] * (order + 1)
    coeffs[0] = float(x0)
    if order >= 1:
        coeffs[1] = 1.0
    return HighOrderDual(coeffs)

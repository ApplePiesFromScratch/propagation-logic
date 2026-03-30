"""
pl/numbers.py — Constructive Number Systems
Part of Propagation Logic / Mathesis Universalis

Each number system is the natural structure forced by the demands
of the previous level. Not axiomatic constructions — propagation outputs.

N: counts of propagation steps
Z: bidirectional reconfiguration
Q: load ratios (propagation rates)
R: coherence completion of Q (CauchyReal)
"""

import math
from math import gcd


# ── Natural Numbers ──────────────────────────────────────────────────────

class N:
    """
    Natural numbers as propagation step counts.
    The successor relation IS a propagation step.
    Zero IS the empty loaded history.
    """

    def __init__(self, steps: int):
        assert isinstance(steps, int) and steps >= 0
        self.steps = steps

    def successor(self) -> 'N':
        return N(self.steps + 1)

    def __add__(self, other: 'N') -> 'N':
        return N(self.steps + other.steps)

    def __mul__(self, other: 'N') -> 'N':
        return N(self.steps * other.steps)

    def __eq__(self, other):
        if isinstance(other, N): return self.steps == other.steps
        if isinstance(other, int): return self.steps == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, N): return self.steps < other.steps
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, N): return self.steps <= other.steps
        return NotImplemented

    def __int__(self): return self.steps
    def __repr__(self): return f"N({self.steps})"


# ── Integers ──────────────────────────────────────────────────────────────

class Z:
    """
    Integers as bidirectional reconfiguration.
    Negative integers are signed reconfiguration directions,
    not constructed from pairs.
    """

    def __init__(self, n: int):
        self.n = int(n)

    def __add__(self, other: 'Z') -> 'Z':
        return Z(self.n + other.n)

    def __sub__(self, other: 'Z') -> 'Z':
        return Z(self.n - other.n)

    def __mul__(self, other: 'Z') -> 'Z':
        return Z(self.n * other.n)

    def __neg__(self) -> 'Z':
        return Z(-self.n)

    def __eq__(self, other):
        if isinstance(other, Z): return self.n == other.n
        if isinstance(other, int): return self.n == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Z): return self.n < other.n
        return NotImplemented

    def __int__(self): return self.n
    def __repr__(self): return f"Z({self.n})"


# ── Rationals ─────────────────────────────────────────────────────────────

class Q:
    """
    Rationals as load ratios — the ratios arising as propagation rates.
    Exact arithmetic. Density: between any two, the mediant lies strictly between.
    """

    def __init__(self, p: int, q: int = 1):
        if q == 0:
            raise ZeroDivisionError("Rational denominator cannot be zero.")
        g = gcd(abs(p), abs(q))
        sign = -1 if q < 0 else 1
        self.p = sign * p // g
        self.q = sign * q // g

    def __add__(self, other: 'Q') -> 'Q':
        if isinstance(other, int): other = Q(other)
        return Q(self.p * other.q + other.p * self.q,
                 self.q * other.q)

    def __radd__(self, other): return self.__add__(Q(other) if isinstance(other, int) else other)

    def __sub__(self, other: 'Q') -> 'Q':
        if isinstance(other, int): other = Q(other)
        return Q(self.p * other.q - other.p * self.q,
                 self.q * other.q)

    def __rsub__(self, other):
        return Q(other).__sub__(self) if isinstance(other, int) else other.__sub__(self)

    def __mul__(self, other: 'Q') -> 'Q':
        if isinstance(other, int): other = Q(other)
        return Q(self.p * other.p, self.q * other.q)

    def __rmul__(self, other): return self.__mul__(Q(other) if isinstance(other, int) else other)

    def __truediv__(self, other: 'Q') -> 'Q':
        if isinstance(other, int): other = Q(other)
        return Q(self.p * other.q, self.q * other.p)

    def __rtruediv__(self, other):
        return Q(other).__truediv__(self) if isinstance(other, int) else other.__truediv__(self)

    def __neg__(self) -> 'Q':
        return Q(-self.p, self.q)

    def __eq__(self, other) -> bool:
        if isinstance(other, Q): return self.p == other.p and self.q == other.q
        if isinstance(other, int): return self.p == other and self.q == 1
        return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, Q): return self.p * other.q < other.p * self.q
        if isinstance(other, int): return self.p < other * self.q
        return NotImplemented

    def __le__(self, other) -> bool:
        return self == other or self < other

    def __gt__(self, other) -> bool:
        if isinstance(other, Q): return other < self
        return NotImplemented

    def midpoint(self, other: 'Q') -> 'Q':
        """The mediant — minimum-load fraction between self and other."""
        return (self + other) / Q(2)

    def __float__(self) -> float:
        return self.p / self.q

    def __repr__(self) -> str:
        if self.q == 1: return f"Q({self.p})"
        return f"Q({self.p}/{self.q})"


# ── Real Numbers: Coherence Completion of Q ───────────────────────────────

class CauchyReal:
    """
    A real number as a coherence limit: a Cauchy sequence of rationals
    that demand(P_n, C_theta) -> 0 for any threshold theta > 0.

    The sequence IS the propagation history.
    The limit IS the coherence state it approaches.

    This is Type B: the mechanism motivates and constructs.
    The resulting structure is standard Cauchy completion.
    """

    def __init__(self, sequence_fn, name=""):
        """
        sequence_fn(n) -> Q: the n-th rational approximation.
        """
        self._seq = sequence_fn
        self.name = name

    def approx(self, n: int) -> Q:
        """Return the n-th rational approximation."""
        return self._seq(n)

    def __float__(self) -> float:
        return float(self._seq(50))

    def __repr__(self):
        approx = float(self)
        return f"CauchyReal({self.name or '?'} ≈ {approx:.10f})"


def sqrt2_real() -> CauchyReal:
    """
    sqrt(2) as coherence limit of Newton reconfiguration in Q.
    Each step: x -> (x + 2/x) / 2
    All steps in Q. Limit is irrational — forcing R.
    """
    def gen(n: int) -> Q:
        x = Q(1)
        for _ in range(n):
            x = (x + Q(2) / x) / Q(2)
        return x
    return CauchyReal(gen, "sqrt(2)")


def e_real() -> CauchyReal:
    """e as coherence limit of sum(1/n!) in Q."""
    def gen(n: int) -> Q:
        total = Q(0)
        factorial = Q(1)
        for k in range(n + 1):
            if k > 0:
                factorial = factorial * Q(k)
            total = total + Q(1) / factorial
        return total
    return CauchyReal(gen, "e")


def pi_real() -> CauchyReal:
    """pi via Leibniz series: 4*(1 - 1/3 + 1/5 - 1/7 + ...)"""
    def gen(n: int) -> Q:
        total = Q(0)
        for k in range(n + 1):
            term = Q((-1) ** k, 2 * k + 1)
            total = total + term
        return total * Q(4)
    return CauchyReal(gen, "pi")

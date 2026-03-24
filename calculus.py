"""
pl/calculus.py — Propagation Logic: calculus regime (V = ℝ)

The same mechanism — loaded patterns, gradient fields, propagation
operator — instantiated over a real carrier V = ℝ instead of {0,1}.

    P = (v_P, L_P)  with  v_P ∈ ℝ
    v_P : current value of the expression
    L_P : differential load — magnitude of accumulated propagation history

The load-combination rules for arithmetic operations are exactly the
rules of forward-mode automatic differentiation. The derivative of
f(x) is read off as the load of the output pattern when the seed is
(val=x, load=1).

Sections 13.1–13.6, paper.
"""

import math


# ── CalcPattern ────────────────────────────────────────────────────────────────

class CalcPattern:
    """
    A loaded pattern over the real carrier V = ℝ.

    val  : current value of the expression
    load : differential load (= derivative when seed load = 1)

    Seed initialisation: CalcPattern(x) sets val=x, load=1, meaning
    "differentiate with respect to this variable."
    To treat a constant: CalcPattern(c, 0.0).

    Definition 13.1 (paper §13.1).
    """

    def __init__(self, val: float, load: float = 1.0):
        self.val = float(val)
        self.load = float(load)

    def __repr__(self):
        return f"CalcPattern(val={self.val}, load={self.load})"

    # ── Arithmetic gradient fields ─────────────────────────────────────────

    def __add__(self, other):
        """G_add: v = v_P + v_Q,  L = L_P + L_Q"""
        if not isinstance(other, CalcPattern):
            other = CalcPattern(other, 0.0)
        return CalcPattern(self.val + other.val, self.load + other.load)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """G_sub: v = v_P − v_Q,  L = L_P − L_Q"""
        if not isinstance(other, CalcPattern):
            other = CalcPattern(other, 0.0)
        return CalcPattern(self.val - other.val, self.load - other.load)

    def __rsub__(self, other):
        if not isinstance(other, CalcPattern):
            other = CalcPattern(other, 0.0)
        return CalcPattern(other.val - self.val, other.load - self.load)

    def __mul__(self, other):
        """
        G_mul (product rule): v = v_P · v_Q,  L = L_P · v_Q + v_P · L_Q
        Theorem 13.1.
        """
        if not isinstance(other, CalcPattern):
            other = CalcPattern(other, 0.0)
        return CalcPattern(
            self.val * other.val,
            self.load * other.val + other.load * self.val
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        G_div (quotient rule):
        v = v_P / v_Q,  L = (L_P · v_Q − v_P · L_Q) / v_Q²
        """
        if not isinstance(other, CalcPattern):
            other = CalcPattern(other, 0.0)
        return CalcPattern(
            self.val / other.val,
            (self.load * other.val - self.val * other.load) / other.val ** 2
        )

    def __rtruediv__(self, other):
        if not isinstance(other, CalcPattern):
            other = CalcPattern(other, 0.0)
        return other.__truediv__(self)

    def __pow__(self, n):
        """
        G_pow (power rule): v = v_P^n,  L = L_P · n · v_P^(n−1)
        """
        return CalcPattern(
            self.val ** n,
            self.load * n * self.val ** (n - 1)
        )

    def __neg__(self):
        return CalcPattern(-self.val, -self.load)

    # ── Transcendental gradient fields ─────────────────────────────────────

    def sin(self):
        """G_sin (chain rule): v = sin(v_P),  L = L_P · cos(v_P)"""
        return CalcPattern(math.sin(self.val), self.load * math.cos(self.val))

    def cos(self):
        """G_cos (chain rule): v = cos(v_P),  L = −L_P · sin(v_P)"""
        return CalcPattern(math.cos(self.val), -self.load * math.sin(self.val))

    def exp(self):
        """
        G_exp (fixed point): v = exp(v_P),  L = L_P · exp(v_P)
        The exponential is the fixed point of the differentiation gradient:
        load = value at every step. This is why d/dx[exp(x)] = exp(x).
        """
        e = math.exp(self.val)
        return CalcPattern(e, self.load * e)

    def log(self):
        """G_log (chain rule): v = log(v_P),  L = L_P / v_P"""
        return CalcPattern(math.log(self.val), self.load / self.val)

    def tan(self):
        """G_tan: v = tan(v_P),  L = L_P / cos²(v_P)"""
        c = math.cos(self.val)
        return CalcPattern(math.tan(self.val), self.load / (c * c))

    def sqrt(self):
        """G_sqrt: v = sqrt(v_P),  L = L_P / (2 · sqrt(v_P))"""
        s = math.sqrt(self.val)
        return CalcPattern(s, self.load / (2 * s))


# ── Integration gradient ───────────────────────────────────────────────────────

def integrate(f, a: float, b: float, threshold: float = 1e-8):
    """
    G_int: accumulate load across [a, b] using adaptive Simpson's rule.

    Accumulation halts when successive refinements add less than
    threshold (the coherence threshold θ_C for this operation).

    Returns (value, n_partitions).

    Definition 13.3, Theorem 13.3 (FTC): the load accumulated by
    G_int, read by the differentiation gradient at the upper limit,
    returns f(x). Integration and differentiation are inverse gradient
    directions — the same structural relationship as ¬¬P = P.

    Paper §13.3.
    """
    n, prev = 4, None
    while True:
        h = (b - a) / n
        acc = f(a) + f(b)
        for i in range(1, n):
            acc += (4 if i % 2 else 2) * f(a + i * h)
        current = acc * h / 3
        if prev is not None and abs(current - prev) < threshold:
            return current, n
        prev, n = current, n * 2


# ── Optimisation as reconfiguration ───────────────────────────────────────────

def newton_reconfigure(f_pattern, x0: float, threshold: float = 1e-10,
                       max_steps: int = 50):
    """
    Reconfiguration toward coherence in the root-finding regime.

    P = (f(x), f'(x)). Coherence: v_P = 0, i.e. f(x) = 0.
    Demand = |f(x)| — the reconfiguration pressure.

    Reconfiguration step (Definition 2.6, calculus regime):
        x ← x − v_P / L_P = x − f(x) / f'(x)

    This is the unique step that minimises demand(P', C) to first order
    along the gradient direction available in Γ_C.

    Convergence is quadratic (Theorem 13.5): each step squares the
    residual demand, so four steps reduce demand from 10⁻¹ to below
    10⁻¹².

    Parameters
    ----------
    f_pattern : callable(x) → CalcPattern
        Function returning (f(x), f'(x)) as a CalcPattern.
        Construct using CalcPattern arithmetic; seed with CalcPattern(x).
    x0        : initial value
    threshold : coherence threshold θ_C (halt when |f(x)| < threshold)
    max_steps : safety limit

    Returns
    -------
    x : float — the coherent root

    Paper §13.6, Definition 13.4, Theorem 13.5.
    """
    x = float(x0)
    for _ in range(max_steps):
        P = f_pattern(x)
        if abs(P.val) < threshold:
            break
        x = x - P.val / P.load
    return x

"""
pl/flux.py — Flux Propagation Through Iterative Solvers
Part of Propagation Logic / Mathesis Universalis [Pugmire, 2026b]

In the calculus regime, loaded history IS the flux — the propagating gradient.
A flux pattern P = (val, flux) carries both simultaneously.

At convergence (fixed-point), BOTH fields stabilise.
The gradient arrives WITH the solution — not extracted after.
Memory: 48 bytes (two floats), constant regardless of iteration depth.
No computation graph. No Jacobian inversion.
"""

import math


class FluxPattern:
    """
    P = (val, flux): value and gradient co-propagating.
    The flux field is not metadata — it is a second propagating
    quantity governed by the same arithmetic as val.
    """

    def __init__(self, val, flux=0.0):
        self.val  = float(val)
        self.flux = float(flux)

    def __add__(self, o):
        if not isinstance(o, FluxPattern): o = FluxPattern(o, 0.0)
        return FluxPattern(self.val + o.val, self.flux + o.flux)

    def __radd__(self, o): return self.__add__(o)

    def __sub__(self, o):
        if not isinstance(o, FluxPattern): o = FluxPattern(o, 0.0)
        return FluxPattern(self.val - o.val, self.flux - o.flux)

    def __rsub__(self, o):
        if not isinstance(o, FluxPattern): o = FluxPattern(o, 0.0)
        return FluxPattern(o.val - self.val, o.flux - self.flux)

    def __mul__(self, o):
        if not isinstance(o, FluxPattern): o = FluxPattern(o, 0.0)
        return FluxPattern(self.val * o.val,
                           self.val * o.flux + o.val * self.flux)   # Leibniz

    def __rmul__(self, o): return self.__mul__(o)

    def __truediv__(self, o):
        if not isinstance(o, FluxPattern): o = FluxPattern(o, 0.0)
        return FluxPattern(self.val / o.val,
                           (self.flux * o.val - self.val * o.flux) / o.val ** 2)

    def __rtruediv__(self, o):
        if not isinstance(o, FluxPattern): o = FluxPattern(o, 0.0)
        return FluxPattern(o.val / self.val,
                           (o.flux * self.val - o.val * self.flux) / self.val ** 2)

    def __pow__(self, n):
        return FluxPattern(self.val ** n,
                           self.flux * n * self.val ** (n - 1))

    def __neg__(self):
        return FluxPattern(-self.val, -self.flux)

    # Elementary functions ─────────────────────────────────────────────────

    def sqrt(self):
        sv = math.sqrt(self.val)
        return FluxPattern(sv, self.flux / (2 * sv))

    def exp(self):
        ev = math.exp(self.val)
        return FluxPattern(ev, self.flux * ev)

    def log(self):
        return FluxPattern(math.log(self.val), self.flux / self.val)

    def sin(self):
        return FluxPattern(math.sin(self.val), self.flux * math.cos(self.val))

    def cos(self):
        return FluxPattern(math.cos(self.val), -self.flux * math.sin(self.val))

    def __repr__(self):
        return f"FluxPattern(val={self.val:.10g}, flux={self.flux:.10g})"


def solve_to_coherence(solver_step, input_val, tol=1e-12, max_iter=500):
    """
    Differentiate through any convergent iterative solver. [Pugmire, 2026b]

    Usage:
        def my_solver_step(state, a):
            return (state + a / state) * FluxPattern(0.5, 0.0)  # Babylonian sqrt

        val, gradient, iters = solve_to_coherence(my_solver_step, input_value=4.0)
        # val=2.0, gradient=0.25 (= 1/(2*sqrt(4))), iters=6

    The input parameter is seeded with unit flux → gradient w.r.t. that input.
    The solver state starts with zero flux → no gradient history yet.

    Returns: (value, gradient, iterations_to_coherence)

    Memory: constant — one FluxPattern (48 bytes) regardless of depth.
    No computation graph. No Jacobian inversion.
    The gradient arrives with the solution because it propagated throughout.

    Flux convergence proof [Pugmire 2026b, Appendix A]:
    At fixed point x* = f(x*, a) with |df/dx| < 1, the flux converges to
    g* = (df/da) / (1 - df/dx)  — the IFT gradient, without matrix inversion.
    """
    a     = FluxPattern(input_val, 1.0)   # unit flux seeds d/da
    state = FluxPattern(1.0, 0.0)         # initial guess, zero flux

    for i in range(max_iter):
        prev  = state
        state = solver_step(state, a)
        if abs(state.val - prev.val) < tol:
            return state.val, state.flux, i + 1

    return state.val, state.flux, max_iter   # coherence not reached


def diff_through_solver(solver_step, input_val, **kwargs):
    """Convenience wrapper — returns just (value, gradient)."""
    val, grad, _ = solve_to_coherence(solver_step, input_val, **kwargs)
    return val, grad

#!/usr/bin/env python3
"""
flux_gradient.py  —  Flux Propagation: O(1) Memory Gradients
Propagation Logic Project · James Alexander Pugmire · 2026

Demonstrates exact gradient computation through iterative fixed-point
solvers with constant memory — independent of iteration depth.

Contrast with backpropagation, which stores O(N) states for N iterations.
Flux propagation always uses exactly 2 floats per variable: 32 bytes total.

The mechanism: the gradient field propagates concurrently with the value.
No backward pass. No stored computation graph. No Jacobian inversion.

This is §9 of pl_unified.py demonstrated in isolation.
See also: core/pl_unified.py §9 for the full derivation.
"""

import math

kB             = 1.380649e-23
LANDAUER_300K  = kB * 300.0 * math.log(2)

SEP = "═" * 68


# ── Flux Pattern ─────────────────────────────────────────────────────────────

class FP:
    """
    Flux Pattern: P = (val, flux).

    val  : current iterative value.
    flux : gradient — propagates concurrently with val.
    Memory: 2 floats = 16 bytes. Constant regardless of iteration depth.

    At convergence x* = f(x*, a), the flux carries ∂x*/∂a exactly.
    This is the implicit function theorem gradient, reached iteratively.
    """
    def __init__(self, val: float, flux: float = 0.0):
        self.val  = float(val)
        self.flux = float(flux)

    def __add__(self, o):
        o = o if isinstance(o, FP) else FP(o)
        return FP(self.val + o.val, self.flux + o.flux)
    __radd__ = __add__

    def __sub__(self, o):
        o = o if isinstance(o, FP) else FP(o)
        return FP(self.val - o.val, self.flux - o.flux)

    def __mul__(self, o):
        o = o if isinstance(o, FP) else FP(o)
        return FP(self.val * o.val,
                  self.val * o.flux + o.val * self.flux)
    __rmul__ = __mul__

    def __truediv__(self, o):
        o = o if isinstance(o, FP) else FP(o)
        return FP(self.val / o.val,
                  (self.flux * o.val - self.val * o.flux) / o.val**2)
    def __rtruediv__(self, o): return FP(o).__truediv__(self)

    def __pow__(self, n):
        return FP(self.val**n, self.flux * n * self.val**(n-1))

    def exp(self):
        ev = math.exp(self.val)
        return FP(ev, self.flux * ev)

    def sin(self):
        return FP(math.sin(self.val), self.flux * math.cos(self.val))

    def cos(self):
        return FP(math.cos(self.val), -self.flux * math.sin(self.val))

    def sqrt(self):
        s = math.sqrt(self.val)
        return FP(s, self.flux / (2 * s))


# ── Flux solver ───────────────────────────────────────────────────────────────

def flux_solve(step_fn, a_val: float, x0: float = 1.0,
               tol: float = 1e-12) -> tuple:
    """
    Solve x = step_fn(x, a) to fixed point.
    Gradient ∂x*/∂a arrives with the solution — no extra work.
    Memory: 2 FP objects = 4 floats = 32 bytes. Constant.

    Returns: (value, gradient, iterations)
    """
    a     = FP(a_val, 1.0)    # unit flux seeds ∂/∂a
    state = FP(x0,   0.0)    # zero flux: no gradient history yet
    for iters in range(500):
        prev  = state
        state = step_fn(state, a)
        if abs(state.val - prev.val) < tol:
            return state.val, state.flux, iters + 1
    return state.val, state.flux, 500


# ── Benchmarks ────────────────────────────────────────────────────────────────

benchmarks = [
    ("√a  (Babylonian)",
     lambda s, a: (s + a / s) * FP(0.5),
     2.0,   math.sqrt(2),       0.5 / math.sqrt(2),    1.5),
    ("√a  (Babylonian)",
     lambda s, a: (s + a / s) * FP(0.5),
     7.0,   math.sqrt(7),       0.5 / math.sqrt(7),    3.0),
    ("√a  (Babylonian)",
     lambda s, a: (s + a / s) * FP(0.5),
     100.0, math.sqrt(100.0),   0.5 / math.sqrt(100.0), 10.5),
    ("∛a  (Newton)",
     lambda s, a: s - (s**3 - a) / (FP(3) * s**2),
     8.0,   2.0,                1.0 / (3 * 8**(2/3)),  2.0),
]


def main():
    print(SEP)
    print("FLUX PROPAGATION — O(1) Memory Gradients")
    print(f"Landauer cost per erased state at 300K: {LANDAUER_300K:.3e} J")
    print(SEP)
    print()
    print(f"  {'Problem':<22} {'a':>6}  {'value':>14}  {'grad ∂x*/∂a':>14}  "
          f"{'exact grad':>14}  {'iters':>6}")
    print("  " + "─" * 82)

    for name, step, a, exact_val, exact_grad, x0 in benchmarks:
        val, grad, iters = flux_solve(step, a_val=a, x0=x0)

        val_err  = abs(val  - exact_val)
        grad_err = abs(grad - exact_grad)
        assert val_err  < 1e-9, f"Value error for {name}(a={a}): {val_err}"
        assert grad_err < 1e-9, f"Grad error for {name}(a={a}): {grad_err}"

        backprop_states  = iters * 2        # (x, a) per step
        flux_states      = 2                # always 2 floats
        erased_bp        = backprop_states * LANDAUER_300K
        erased_flux      = flux_states      * LANDAUER_300K
        savings          = erased_bp / erased_flux

        print(f"  {name:<22} {a:>6.1f}  {val:>14.8f}  {grad:>14.8f}  "
              f"{exact_grad:>14.8f}  {iters:>6d}")
        print(f"  {'':22}        "
              f"backprop: {backprop_states} states ({erased_bp:.2e} J)  "
              f"flux: {flux_states} states ({erased_flux:.2e} J)  "
              f"savings: {savings:.0f}×")

    print()
    print(SEP)
    print("All assertions passed.")
    print()
    print("Flux propagation: exact gradients with constant memory.")
    print("Backpropagation through N iterations: O(N) memory.")
    print("Flux: always O(1) — gradient carried in the load component.")
    print("Thermodynamically optimal: minimum history, maximum gradient.")
    print(SEP)


if __name__ == "__main__":
    main()

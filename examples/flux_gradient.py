#!/usr/bin/env python3
"""
Flux propagation demo: O(1) memory gradient through iterative convergence.
Compare memory cost vs standard backpropagation.
"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
from pl_unified import Dual, flux_solve

kB = 1.380649e-23
landauer_300 = kB * 300 * math.log(2)

print("FLUX PROPAGATION — O(1) memory gradients")
print(f"Landauer cost per erased state: {landauer_300:.2e} J
")

# Babylonian √a: x_{n+1} = (x + a/x)/2
def babylonian(xd, ad):
    return (xd + ad/xd) * 0.5

print("Babylonian √a — gradient d√a/da = 1/(2√a)")
for a in [2.0, 7.0, 100.0]:
    root, grad, iters = flux_solve(babylonian, x0=a/2+0.5, a_val=a)
    exact_grad = 0.5/math.sqrt(a)
    backprop_states = iters * 2   # (x, a) per step
    flux_states = 2               # always 2 floats
    erased = (backprop_states - flux_states) * landauer_300
    print(f"  √{a:6.1f}: root={root:.8f}  grad={grad:.8f}  (exact:{exact_grad:.8f})")
    print(f"         Backprop stores {backprop_states} floats → erases {erased:.2e} J")
    print(f"         Flux stores     {flux_states} floats  → erases {flux_states*landauer_300:.2e} J")
    print(f"         Savings: {erased/(flux_states*landauer_300):.0f}× less heat  ✓")
    print()

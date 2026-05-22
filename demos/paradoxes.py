"""
demos/paradoxes.py — Propagation Logic: Paradoxes as Thermodynamic Debt

In the unified framework, paradoxes are not caused by self-reference.
They occur when the propagation load creates a thermodynamic debt
that the current carrier + gradient family cannot pay.

The system demands reconfiguration, but the carrier cannot satisfy it.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pl.core import Pattern, Context

C = Context(threshold=1.0)

print("=" * 70)
print("Propagation Logic — Paradoxes as Unpayable Thermodynamic Debt")
print("=" * 70)
print()

# ── Liar Paradox ─────────────────────────────────────────────────────
print("§10.1  The Liar Paradox")
print("       'This proposition is not designated'")
print()

print("In binary carrier {0,1}:")
print("   Requires v = 1 - v")
print("   No solution exists → infinite load accumulation")
print("   → Thermodynamic debt grows without bound")
print()

# Simple simulation of debt accumulation
print("Load accumulation (thermodynamic pressure):")
L = 1.0
for step in range(1, 6):
    L = L * 2
    print(f"  Step {step}: debt = {L:.0f} units")
print("   ... debt exceeds any finite coherence threshold (θ=1.0)")
print()

print("Resolution in unified view:")
print("   Not a self-reference problem.")
print("   It is the carrier being unable to pay the demanded propagation debt.")
print("   Extend carrier (e.g. to [0,1]) → debt becomes payable at v=0.5")
print("\n" + "="*70)
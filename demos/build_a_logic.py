#!/usr/bin/env python3
"""
Build a logic from scratch using Propagation Logic.
This example builds a deontic logic (logic of obligations and permissions).

A deontic logic needs:
  V = {forbidden, permitted, obligatory}  — three values
  Γ = {obligation, permission, prohibition, norm_negation}
  θ = 1.0

We derive: what laws are forced by this carrier?
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

# Step 1: Identify your value carrier
V = {"forbidden": 0, "permitted": 0.5, "obligatory": 1}
print("Step 1: Carrier V = {forbidden=0, permitted=0.5, obligatory=1}")

# Step 2: Define gradient family
def norm_neg(v):
    """Deontic negation: forbidden ↔ obligatory, permitted ↔ permitted"""
    return {0: 1, 0.5: 0.5, 1: 0}[v]

def permission(v):
    """Something is permitted if not forbidden"""
    return 0 if v == 0 else 0.5

print("Step 2: Gradients defined — norm_neg, permission")

# Step 3: Derive forced laws
print("
Step 3: Derive what the carrier forces")

# Does deontic non-contradiction hold?
for name, v in V.items():
    nc = min(v, norm_neg(v))
    print(f"  {name}: v AND norm_neg(v) = min({v}, {norm_neg(v)}) = {nc}")

# Is there an excluded middle?
for name, v in V.items():
    em = max(v, norm_neg(v))
    print(f"  {name}: v OR norm_neg(v) = max({v}, {norm_neg(v)}) = {em}")

print("
Step 4: Document the carrier")
print("""  V     = {forbidden, permitted, obligatory}
  Γ     = {norm_neg, permission, obligation}
  θ     = 1.0
  Forced: obligation + permission partition (not both obligatory and forbidden)
  Not forced: classical LNC (permitted is its own norm-negation)
  Explicit failure: cannot represent supererogation (beyond obligation)
""")
print("Step 5: Write carriers/deontic.json and submit a PR.")

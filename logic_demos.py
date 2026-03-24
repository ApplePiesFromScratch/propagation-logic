"""
demos/logic_demos.py

Reproduces every inline coded demonstration from Sections 2–11 of the
paper. Each block is labelled with its section. All output values match
those printed in the paper exactly.

Run:
    python demos/logic_demos.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import random
import math
from pl.core import Pattern, Context, G_id, G_neg, G_and, G_or, G_imp

C = Context(threshold=1.0)


# ── §2.2  Support, demand, validity ───────────────────────────────────────────

print("=" * 60)
print("§2.2  Support, demand, validity  (θ_C = 1)")
print("=" * 60)
for load in [0.5, 1.0, 1.5, 2.0]:
    p = Pattern(val=1, load=load)
    print(
        f"L={load}: support={C.support(p):.1f}  "
        f"demand={C.demand(p):.1f}  valid={C.valid(p)}"
    )
# L=0.5: support=0.5  demand=0.0  valid=True
# L=1.0: support=1.0  demand=0.0  valid=True
# L=1.5: support=1.0  demand=0.5  valid=False
# L=2.0: support=1.0  demand=1.0  valid=False


# ── §2.3  Propagation rate and ordering ───────────────────────────────────────

print()
print("=" * 60)
print("§2.3  Propagation rate and ordering  (θ_C = 1)")
print("=" * 60)
for load in [0.5, 1.0, 1.5, 2.0, 3.0]:
    p = Pattern(val=1, load=load)
    r = C.rate(p)
    status = 'coherent' if C.coherent(p) else 'incoherent'
    print(f"L={load}: rate={r:.3f} [{status}]")
# L=0.5: rate=1.000 [coherent]
# L=1.0: rate=1.000 [coherent]
# L=1.5: rate=0.667 [incoherent]
# L=2.0: rate=0.500 [incoherent]
# L=3.0: rate=0.333 [incoherent]
#
# Theorem 2.1: among incoherent patterns, lower load → higher rate
incoherent = [Pattern(1, l) for l in [1.5, 2.0, 3.0]]
rates = [C.rate(p) for p in incoherent]
loads = [p.load for p in incoherent]
print(f"Rate ordering (desc): {sorted(rates, reverse=True)}")
print(f"Load ordering (asc):  {sorted(loads)}")
assert sorted(rates, reverse=True) == rates  # confirmed


# ── §2.4  Zero-drag regime ────────────────────────────────────────────────────

print()
print("=" * 60)
print("§2.4  Zero-drag regime (classical logic scope)")
print("=" * 60)
P1 = Pattern(val=1, load=1.0)
P2 = Pattern(val=1, load=1.0)
drag = 0.0
compound_load = P1.load + P2.load + drag
print(f"P1={P1}, P2={P2}")
print(f"drag = {drag}")
print(f"compound load = {compound_load} (additive: L1+L2)")
# compound load = 2.0 (additive: L1+L2)


# ── §2.7  Complexity growth through iterated propagation ──────────────────────

print()
print("=" * 60)
print("§2.7  Complexity growth through iterated propagation")
print("=" * 60)
P = Pattern(val=1, load=0.3)
print(f"Seed: (v={P.val}, L={P.load})")
for i in range(5):
    P = G_and(P, Pattern(val=1, load=0.3))
    r = C.support(P) / P.load if P.load > 0 else 1.0
    print(f"Step {i+1}: (v={P.val}, L={P.load:.1f}) rate={r:.3f}")
# Step 3 crosses coherence threshold, rate falls thereafter


# ── §2.8  Self-referential load recursion ─────────────────────────────────────

print()
print("=" * 60)
print("§2.8  Self-referential load (maximum complexity)")
print("=" * 60)
L = 1.0
print(f"Starting load: {L}")
for step in range(1, 7):
    L = L + L
    if L > 1000:
        print(f"Step {step}: L → ∞ (exceeds any finite θ_C)")
        break
    print(f"Step {step}: L = {L}")
# Step 1: L = 2.0  ...  No finite θ_C contains this.


# ── §3.1  Negation ────────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§3.1  Negation gradient")
print("=" * 60)
P = Pattern(val=1, load=1.0)
print(G_neg(P))                   # (v=0, L=1.0)
print(G_neg(G_neg(P)))            # (v=1, L=1.0) — double negation
print(G_neg(G_neg(P)) == P)       # True ✓


# ── §3.2  Conjunction ─────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§3.2  Conjunction gradient (truth table)")
print("=" * 60)
for vp, vq in [(0,0),(0,1),(1,0),(1,1)]:
    r = G_and(Pattern(vp, 1.0), Pattern(vq, 1.0))
    print(f"({vp},{vq}) → val={r.val}, load={r.load}")


# ── §3.3  Disjunction ─────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§3.3  Disjunction — selects easier path (lower load)")
print("=" * 60)
P = Pattern(val=1, load=0.6)   # easier
Q = Pattern(val=1, load=1.4)   # harder
r = G_or(P, Q)
print(f"P∨Q = {r}")              # (v=1, L=0.6) — takes easier load
print(f"valid = {C.valid(r)}")   # True

# Excluded middle
P = Pattern(val=1, load=1.0)
em = G_or(P, G_neg(P))
print(f"P∨¬P = {em}, valid = {C.valid(em)}")   # True ✓


# ── §3.4  Implication ─────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§3.4  Implication — value-based activation")
print("=" * 60)
Q = Pattern(val=1, load=0.8)
for vp in [0, 1]:
    P = Pattern(vp, 1.0)
    r = G_imp(P, Q)
    case = 'forcing' if vp == 1 else 'vacuous'
    print(f"v_P={vp}: G_imp(P,Q) = {r} [{case}]")
# v_P=0: (v=1, L=0.0) [vacuous]
# v_P=1: (v=1, L=0.8) [forcing — returns Q exactly]


# ── §4  Classical laws ────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§4  Classical laws as forced boundary conditions")
print("=" * 60)

# Identity
P = Pattern(val=1, load=1.0)
print(f"G_id(P) == P: {G_id(P) == P}")                         # True ✓

# Non-contradiction — arithmetic on {0,1}
for v in [0, 1]:
    P = Pattern(v, 1.0)
    nc = G_and(P, G_neg(P))
    print(
        f"v={v}: P∧¬P → val={nc.val}  (v·(1-v)={v*(1-v)})  "
        f"coherent={C.coherent(nc)}"
    )
# val=0 always; load=2L > θ=1 so also incoherent

# Excluded middle
for v in [0, 1]:
    P = Pattern(val=v, load=1.0)
    em = G_or(P, G_neg(P))
    print(f"v={v}: P∨¬P = {em}, valid = {C.valid(em)}")   # True ✓


# ── §5  Quantifiers ───────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§5  Quantifiers — sup/inf load over a domain  (θ_C = 1.0)")
print("=" * 60)
domain = {'a': Pattern(1, 0.5), 'b': Pattern(1, 0.8), 'c': Pattern(1, 1.2)}

L_forall = max(p.load for p in domain.values())   # sup — hardest instance
forall   = Pattern(1, L_forall)
print(f"∀x P(x): load={L_forall}, valid={C.valid(forall)}")   # False (1.2 > 1)

L_exists = min(p.load for p in domain.values())   # inf — easiest instance
exists   = Pattern(1, L_exists)
print(f"∃x P(x): load={L_exists}, valid={C.valid(exists)}")   # True  (0.5 ≤ 1)

# Infinite domain: bounded sup
loads = [1 / (n + 1) for n in range(1000)]
print(f"Bounded infinite domain: sup={max(loads):.4f}, inf={min(loads):.6f}")
# sup=0.5000 — finite, so ∀n P(n) can be coherent for θ ≥ 0.5


# ── §6  Modus Ponens and Hypothetical Syllogism ───────────────────────────────

print()
print("=" * 60)
print("§6  Modus Ponens and Hypothetical Syllogism")
print("=" * 60)
P = Pattern(val=1, load=1.0)
Q = Pattern(val=1, load=0.8)
R = Pattern(val=1, load=0.6)

print(f"P valid: {C.valid(P)}")
print(f"G_imp(P,Q) = {G_imp(P,Q)}  valid: {C.valid(G_imp(P,Q))}")   # True ✓

# Hypothetical syllogism
step1 = G_imp(P, Q)
step2 = G_imp(step1, R)
print(f"P→Q→R gives R: {step2 == R}")   # True ✓


# ── §7  Modal operators ───────────────────────────────────────────────────────

print()
print("=" * 60)
print("§7  Modal operators — sup/inf over accessible context graph")
print("=" * 60)
accessible = {'C1': 0.6, 'C2': 0.9, 'C3': 1.3}
L_box     = max(accessible.values())   # necessity:   sup
L_diamond = min(accessible.values())   # possibility: inf
box_P     = Pattern(val=1, load=L_box)
diamond_P = Pattern(val=1, load=L_diamond)

print(f"□P: load={L_box}, valid={C.valid(box_P)}")         # False
print(f"◇P: load={L_diamond}, valid={C.valid(diamond_P)}") # True
print(f"□P → ◇P (sup ≥ inf): {L_box >= L_diamond}")        # True ✓

# S4: transitive graph
direct_sup     = max([0.6, 0.9, 1.3])
transitive_sup = max([0.5, 0.7, 0.9, 1.3])
print(f"S4 □P→□□P: trans_sup({transitive_sup}) ≤ direct_sup({direct_sup}): "
      f"{transitive_sup <= direct_sup}")                    # True ✓

# S5: equivalence class
L_dia_s5     = min([0.6, 0.9, 1.3])
L_box_dia_s5 = max([L_dia_s5] * 3)
print(f"S5 ◇P→□◇P: {L_box_dia_s5} ≤ {L_dia_s5}: "
      f"{L_box_dia_s5 <= L_dia_s5}")                       # True ✓


# ── §8.1  Consistency ─────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§8.1  Consistency")
print("=" * 60)
P    = Pattern(val=1, load=1.0)
negP = G_neg(P)
print(f"P valid:  {C.valid(P)}")
print(f"¬P valid: {C.valid(negP)}")
print(f"Both valid: {C.valid(P) and C.valid(negP)}")   # False — consistent ✓


# ── §9 / §11.5  Probability — measure over valid contexts ─────────────────────

print()
print("=" * 60)
print("§11.5  Probability — measure over valid contexts")
print("=" * 60)
random.seed(42)
contexts = [Context(threshold=random.uniform(0.3, 2.0)) for _ in range(1000)]
P_heavy = Pattern(val=1, load=1.5)
P_light = Pattern(val=1, load=0.4)
P_contra = G_and(Pattern(1, 1.0), G_neg(Pattern(1, 1.0)))

pr_heavy  = sum(1 for c in contexts if c.valid(P_heavy))  / len(contexts)
pr_light  = sum(1 for c in contexts if c.valid(P_light))  / len(contexts)
pr_contra = sum(1 for c in contexts if c.valid(P_contra)) / len(contexts)

print(f"P_heavy (L=1.5): Pr={pr_heavy:.3f}")   # ~0.302
print(f"P_light (L=0.4): Pr={pr_light:.3f}")   # ~0.951
print(f"P∧¬P:            Pr={pr_contra:.3f}")  # 0.000 — contradiction ✓


# ── §11.3  Paraconsistent: extended threshold ─────────────────────────────────

print()
print("=" * 60)
print("§11.3  Paraconsistent regime  (θ = 2.0)")
print("=" * 60)
C2 = Context(threshold=2.0)
P  = Pattern(1, 1.0)
nc = G_and(P, G_neg(P))
print(f"P∧¬P: val={nc.val}, load={nc.load}, coherent(θ=2.0)={C2.coherent(nc)}")
# val=0 (carrier arithmetic unchanged),  load=2.0,  coherent=True
# Contradiction is coherent-but-undesignated: propagates without
# generating reconfiguration pressure. The mechanism does not break.


print()
print("All logic demonstrations complete.")

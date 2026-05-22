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

incoherent = [Pattern(1, l) for l in [1.5, 2.0, 3.0]]
rates = [C.rate(p) for p in incoherent]
loads = [p.load for p in incoherent]
print(f"Rate ordering (desc): {sorted(rates, reverse=True)}")
print(f"Load ordering (asc):  {sorted(loads)}")
assert sorted(rates, reverse=True) == rates


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


# ── §3.1  Negation ────────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§3.1  Negation gradient")
print("=" * 60)
P = Pattern(val=1, load=1.0)
print(G_neg(P))
print(G_neg(G_neg(P)))
print(G_neg(G_neg(P)) == P)


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
P = Pattern(val=1, load=0.6)
Q = Pattern(val=1, load=1.4)
r = G_or(P, Q)
print(f"P∨Q = {r}")
print(f"valid = {C.valid(r)}")

P = Pattern(val=1, load=1.0)
em = G_or(P, G_neg(P))
print(f"P∨¬P = {em}, valid = {C.valid(em)}")


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


# ── §4  Classical laws ────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§4  Classical laws as forced boundary conditions")
print("=" * 60)

P = Pattern(val=1, load=1.0)
print(f"G_id(P) == P: {G_id(P) == P}")

for v in [0, 1]:
    P = Pattern(v, 1.0)
    nc = G_and(P, G_neg(P))
    print(
        f"v={v}: P∧¬P → val={nc.val}  (v·(1-v)={v*(1-v)})  "
        f"coherent={C.coherent(nc)}"
    )

for v in [0, 1]:
    P  = Pattern(val=v, load=1.0)
    em = G_or(P, G_neg(P))
    print(f"v={v}: P∨¬P = {em}, valid = {C.valid(em)}")


# ── §5  Quantifiers ───────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§5  Quantifiers — sup/inf load over a domain  (θ_C = 1.0)")
print("=" * 60)
domain = {'a': Pattern(1, 0.5), 'b': Pattern(1, 0.8), 'c': Pattern(1, 1.2)}

L_forall = max(p.load for p in domain.values())
forall   = Pattern(1, L_forall)
print(f"∀x P(x): load={L_forall}, valid={C.valid(forall)}")

L_exists = min(p.load for p in domain.values())
exists   = Pattern(1, L_exists)
print(f"∃x P(x): load={L_exists}, valid={C.valid(exists)}")

loads = [1 / (n + 1) for n in range(1000)]
print(f"Bounded infinite domain: sup={max(loads):.4f}, inf={min(loads):.6f}")


# ── §6  Modus Ponens and Hypothetical Syllogism ───────────────────────────────

print()
print("=" * 60)
print("§6  Modus Ponens and Hypothetical Syllogism")
print("=" * 60)
P = Pattern(val=1, load=1.0)
Q = Pattern(val=1, load=0.8)
R = Pattern(val=1, load=0.6)

print(f"P valid: {C.valid(P)}")
print(f"G_imp(P,Q) = {G_imp(P,Q)}  valid: {C.valid(G_imp(P,Q))}")

step1 = G_imp(P, Q)
step2 = G_imp(step1, R)
print(f"P→Q→R gives R: {step2 == R}")


# ── §7  Modal operators ───────────────────────────────────────────────────────

print()
print("=" * 60)
print("§7  Modal operators — sup/inf over accessible context graph")
print("=" * 60)
accessible = {'C1': 0.6, 'C2': 0.9, 'C3': 1.3}
L_box     = max(accessible.values())
L_diamond = min(accessible.values())
box_P     = Pattern(val=1, load=L_box)
diamond_P = Pattern(val=1, load=L_diamond)

print(f"□P: load={L_box}, valid={C.valid(box_P)}")
print(f"◇P: load={L_diamond}, valid={C.valid(diamond_P)}")
print(f"□P → ◇P (sup ≥ inf): {L_box >= L_diamond}")

direct_sup     = max([0.6, 0.9, 1.3])
transitive_sup = max([0.5, 0.7, 0.9, 1.3])
print(f"S4 □P→□□P: trans_sup({transitive_sup}) ≤ direct_sup({direct_sup}): "
      f"{transitive_sup <= direct_sup}")

L_dia_s5     = min([0.6, 0.9, 1.3])
L_box_dia_s5 = max([L_dia_s5] * 3)
print(f"S5 ◇P→□◇P: {L_box_dia_s5} ≤ {L_dia_s5}: "
      f"{L_box_dia_s5 <= L_dia_s5}")


# ── §8.1  Consistency ─────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§8.1  Consistency")
print("=" * 60)
P    = Pattern(val=1, load=1.0)
negP = G_neg(P)
print(f"P valid:  {C.valid(P)}")
print(f"¬P valid: {C.valid(negP)}")
print(f"Both valid: {C.valid(P) and C.valid(negP)}")


# ── §11.5  Probability ────────────────────────────────────────────────────────

print()
print("=" * 60)
print("§11.5  Probability — measure over valid contexts")
print("=" * 60)
random.seed(42)
contexts = [Context(threshold=random.uniform(0.3, 2.0)) for _ in range(1000)]
P_heavy  = Pattern(val=1, load=1.5)
P_light  = Pattern(val=1, load=0.4)
P_contra = G_and(Pattern(1, 1.0), G_neg(Pattern(1, 1.0)))

pr_heavy  = sum(1 for c in contexts if c.valid(P_heavy))  / len(contexts)
pr_light  = sum(1 for c in contexts if c.valid(P_light))  / len(contexts)
pr_contra = sum(1 for c in contexts if c.valid(P_contra)) / len(contexts)

print(f"P_heavy (L=1.5): Pr={pr_heavy:.3f}")
print(f"P_light (L=0.4): Pr={pr_light:.3f}")
print(f"P∧¬P:            Pr={pr_contra:.3f}")


# ── §11.3  Paraconsistent ─────────────────────────────────────────────────────

print()
print("=" * 60)
print("§11.3  Paraconsistent regime  (θ = 2.0)")
print("=" * 60)
C2 = Context(threshold=2.0)
P  = Pattern(1, 1.0)
nc = G_and(P, G_neg(P))
print(f"P∧¬P: val={nc.val}, load={nc.load}, coherent(θ=2.0)={C2.coherent(nc)}")


print()
print("All logic demonstrations complete.")

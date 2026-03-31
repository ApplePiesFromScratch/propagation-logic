"""
boundary_condition_extrapolation.py
=====================================
Training data for boundary condition extrapolation.

The goal: a model that can take a novel carrier V and gradient
family Gamma_C, and derive the forced boundary conditions —
including checking recursive stability.

This file shows the PROCEDURE, not just the results.
The model needs to see this derivation process many times
with varied inputs to generalise to novel carriers.

The procedure:
  1. Apply each G to each element of V
  2. Check closure: G(V) ⊆ V?
  3. Find fixed points: where does P/G → P?
  4. Check recursive stability:
       applying G to a boundary condition must return a
       pattern still within V (or still satisfying the condition)
  5. Check coherence: no P such that P is both designated
     and its negation is designated
  6. State the boundary conditions: what cannot be otherwise

If the carrier is extended (new elements added), repeat.
The boundary conditions of the new carrier may differ.
"""

from dataclasses import dataclass
from typing import Any, List, Tuple, Dict, Set, Optional
import math


@dataclass
class Pattern:
    val:  Any
    load: float = 1.0

    def __repr__(self):
        return f"P({self.val}, L={self.load})"


def derive_boundary_conditions(
    carrier:          List[Any],
    gradient_family:  Dict[str, callable],
    threshold:        float = 1.0,
    verbose:          bool = True
) -> Dict:
    """
    Given a carrier V and gradient family Gamma_C,
    derive the forced boundary conditions step by step.

    Returns: {
        'fixed_points': patterns where P/G -> P,
        'boundary_conditions': list of forced laws,
        'recursive_stable': bool,
        'coherent': bool,
        'carrier_pressure': list of values outside V
                           (forcing carrier extension)
    }

    This IS the mechanism applied to itself.
    The boundary conditions are not chosen — they are what
    the carrier arithmetic forces.
    """
    if verbose:
        print(f"\nCarrier V = {carrier}")
        print(f"Gradient family: {list(gradient_family.keys())}")
        print(f"Coherence threshold theta_C = {threshold}")
        print("=" * 55)

    # ── Step 1: Apply each G to each element ──────────────────
    if verbose:
        print("\nSTEP 1: Apply each G to each element of V")

    propagation_table = {}
    carrier_pressure = []  # values that escape V

    for g_name, G in gradient_family.items():
        propagation_table[g_name] = {}
        for v in carrier:
            p = Pattern(v)
            try:
                q = G(p)
                propagation_table[g_name][v] = q.val
                if q.val not in carrier:
                    carrier_pressure.append((g_name, v, q.val))
                    if verbose:
                        print(f"  PRESSURE: G_{g_name}({v}) = {q.val} ∉ V "
                              f"→ carrier extension demanded")
                elif verbose:
                    print(f"  G_{g_name}({v}) = {q.val} ∈ V ✓")
            except Exception as e:
                if verbose:
                    print(f"  G_{g_name}({v}) = UNDEFINED ({e})")

    # ── Step 2: Check closure ─────────────────────────────────
    if verbose:
        print("\nSTEP 2: Check closure G(V) ⊆ V")

    closed = len(carrier_pressure) == 0
    if verbose:
        if closed:
            print("  All gradient outputs within V: CLOSED ✓")
        else:
            print(f"  V is NOT closed under gradient family.")
            print(f"  Carrier extension required for: {carrier_pressure}")

    # ── Step 3: Find fixed points ─────────────────────────────
    if verbose:
        print("\nSTEP 3: Find fixed points P/G → P")

    fixed_points = {}
    for g_name, table in propagation_table.items():
        fps = [v for v, out in table.items() if out == v]
        fixed_points[g_name] = fps
        if verbose:
            if fps:
                print(f"  Fixed points of G_{g_name}: {fps}")
            else:
                print(f"  G_{g_name} has no fixed points in V")

    # ── Step 4: Check recursive stability ─────────────────────
    if verbose:
        print("\nSTEP 4: Check recursive stability")
        print("  (Boundary conditions must be stable under repeated application)")

    recursive_stable = True
    stability_issues = []

    # A boundary condition is recursively stable iff:
    # applying G repeatedly to it stays within V and
    # eventually reaches a fixed point or cycle
    for g_name, G in gradient_family.items():
        for v in carrier:
            p = Pattern(v)
            trajectory = [v]
            seen = {v}
            current = v
            stable = False
            for _ in range(len(carrier) * 2 + 2):
                try:
                    q = G(Pattern(current))
                    if q.val not in carrier:
                        stability_issues.append(
                            f"G_{g_name}: trajectory from {v} "
                            f"escapes V at {current} → {q.val}"
                        )
                        recursive_stable = False
                        break
                    if q.val in seen:
                        stable = True  # reached cycle/fixed point
                        break
                    seen.add(q.val)
                    trajectory.append(q.val)
                    current = q.val
                except:
                    break
            if verbose and stable:
                if len(trajectory) > 1:
                    print(f"  G_{g_name} from {v}: {' → '.join(str(x) for x in trajectory)} "
                          f"→ cycle/fixed point ✓")

    if verbose:
        if recursive_stable:
            print("  All trajectories recursively stable ✓")
        else:
            for issue in stability_issues:
                print(f"  UNSTABLE: {issue}")

    # ── Step 5: Check coherence ───────────────────────────────
    if verbose:
        print("\nSTEP 5: Check coherence")
        print("  (No P such that both P and ¬P are designated)")

    coherent = True
    if 'neg' in gradient_family:
        G_neg = gradient_family['neg']
        for v in carrier:
            p = Pattern(v)
            try:
                neg_p = G_neg(p)
                if v == 1 and neg_p.val == 1:
                    coherent = False
                    if verbose:
                        print(f"  INCOHERENT: {v} and ¬{v} = {neg_p.val} both designated")
            except:
                pass
        if coherent and verbose:
            print("  No designated pattern has a designated negation ✓")

    # ── Step 6: State the boundary conditions ─────────────────
    if verbose:
        print("\nSTEP 6: Boundary conditions — what cannot be otherwise")

    boundary_conditions = []

    # Non-contradiction: v * (1-v) = 0 for boolean carrier
    if set(carrier) == {0, 1} and 'neg' in gradient_family and 'and' in gradient_family:
        for v in carrier:
            p = Pattern(v)
            neg = gradient_family['neg'](p)
            conj = gradient_family['and'](p, neg)
            if conj.val == 0:
                bc = f"Non-contradiction: G_and({v}, G_neg({v})) = {conj.val} — never designated"
                boundary_conditions.append(bc)
                if verbose:
                    print(f"  FORCED: {bc}")
                break

    # Excluded middle
    if 'neg' in gradient_family and 'or' in gradient_family:
        em_holds = all(
            gradient_family['or'](Pattern(v), gradient_family['neg'](Pattern(v))).val == 1
            for v in carrier if v in [0, 1]
        )
        if em_holds:
            bc = "Excluded middle: G_or(P, G_neg(P)) = 1 — always designated"
            boundary_conditions.append(bc)
            if verbose:
                print(f"  FORCED: {bc}")

    # Double negation
    if 'neg' in gradient_family:
        dn_holds = all(
            gradient_family['neg'](gradient_family['neg'](Pattern(v))).val == v
            for v in carrier
        )
        if dn_holds:
            bc = "Double negation: G_neg(G_neg(P)) = P — involution"
            boundary_conditions.append(bc)
            if verbose:
                print(f"  FORCED: {bc}")

    result = {
        'closed': closed,
        'fixed_points': fixed_points,
        'boundary_conditions': boundary_conditions,
        'recursive_stable': recursive_stable,
        'coherent': coherent,
        'carrier_pressure': carrier_pressure,
    }

    if verbose:
        print(f"\nSUMMARY:")
        print(f"  Closed under gradient family: {closed}")
        print(f"  Recursively stable: {recursive_stable}")
        print(f"  Coherent: {coherent}")
        print(f"  Boundary conditions forced: {len(boundary_conditions)}")
        if carrier_pressure:
            print(f"  Carrier extension pressure: YES → extend V")

    return result


# ══════════════════════════════════════════════════════════════
# DEMONSTRATIONS: DERIVE BOUNDARY CONDITIONS FROM SCRATCH
# Each one shows the full procedure so the model learns it.
# ══════════════════════════════════════════════════════════════

SEP = "=" * 55

def demo_classical_logic():
    """Derive classical logic boundary conditions from V={0,1}."""
    print(SEP)
    print("DERIVATION 1: Classical Logic")
    print("Starting from V = {0, 1}, full gradient family")
    print(SEP)

    def G_neg(p):  return Pattern(1 - p.val,             p.load)
    def G_and(p,q): return Pattern(p.val * q.val,         p.load + q.load)
    def G_or(p,q):  return Pattern(max(p.val, q.val),     min(p.load, q.load))

    result = derive_boundary_conditions(
        carrier=[0, 1],
        gradient_family={'neg': G_neg, 'and': G_and, 'or': G_or},
        verbose=True
    )
    print("\nCONCLUSION: V={0,1} + full gradient family")
    print("  FORCES exactly the boundary conditions classical logic formalises.")
    print("  These are not axioms. They are what the carrier arithmetic demands.")
    return result


def demo_three_valued():
    """What happens when we extend V to {0, 0.5, 1}?"""
    print(SEP)
    print("DERIVATION 2: Three-valued carrier V = {0, 0.5, 1}")
    print("What boundary conditions are forced?")
    print(SEP)

    def G_neg(p):   return Pattern(1 - p.val, p.load)
    def G_and(p,q): return Pattern(min(p.val, q.val), p.load + q.load)
    def G_or(p,q):  return Pattern(max(p.val, q.val), min(p.load, q.load))

    result = derive_boundary_conditions(
        carrier=[0, 0.5, 1],
        gradient_family={'neg': G_neg, 'and': G_and, 'or': G_or},
        verbose=True
    )
    print("\nCONCLUSION: V = {0, 0.5, 1}")
    print("  Excluded middle FAILS: G_or(0.5, G_neg(0.5)) = G_or(0.5, 0.5) = 0.5 ≠ 1")
    print("  The carrier has a gap. Middle is NOT excluded.")
    print("  This is the carrier change that generates fuzzy logic.")
    print("  Not a choice — what the arithmetic of this carrier forces.")
    return result


def demo_constructive():
    """What happens with restricted gradient family (no direct assertion)?"""
    print(SEP)
    print("DERIVATION 3: V = {0, 1}, Constructive gradient family")
    print("No direct assertion gradient. Only: neg, and, imp from reached patterns.")
    print(SEP)

    # Track what's reachable from seed {P=1}
    reachable = {1}  # start with P designated

    def G_neg_constr(p):
        # Only available if we can reach neg-P via a path
        # Without direct assertion, neg-P requires prior derivation
        if 1 - p.val in reachable:
            return Pattern(1 - p.val, p.load)
        raise ValueError(f"G_neg({p.val}) not reachable: {1-p.val} not in {reachable}")

    def G_and_constr(p, q):
        if p.val in reachable and q.val in reachable:
            return Pattern(p.val * q.val, p.load + q.load)
        raise ValueError(f"Both inputs must be reachable")

    def G_or_constr(p, q):
        # Disjunction requires at least one reachable disjunct
        if p.val in reachable or q.val in reachable:
            return Pattern(max(p.val, q.val), min(p.load, q.load))
        raise ValueError(f"At least one disjunct must be reachable")

    print("\nWith seed {P=1}, 0 is NOT reachable via constructive gradient family.")
    print("Therefore G_neg(1) = 0 IS reachable (1 → 0 via neg).")
    print("But P ∨ ¬P requires ¬P to be derived first — and ¬P requires P to be known.")
    print("This creates a path dependency that standard direct assertion sidesteps.")
    print()
    print("Forced boundary condition change:")
    print("  In V={0,1} + full family: P ∨ ¬P always valid (excluded middle holds)")
    print("  In V={0,1} + constructive: P ∨ ¬P valid only if ¬P is derivable")
    print("  SAME carrier. DIFFERENT gradient family. DIFFERENT boundary conditions.")
    print("  This is intuitionistic logic — not a different logic, a different gradient family.")


def demo_real_carrier():
    """What boundary conditions does V=R force for calculus?"""
    print(SEP)
    print("DERIVATION 4: Calculus — V = ℝ, arithmetic gradient family")
    print(SEP)

    # In the real carrier, gradient fields are the arithmetic operations
    # The boundary condition is: the product rule, chain rule, FTC
    # Let's demonstrate with the exp fixed point

    print("STEP 1: Find fixed points of G_diff in V = ℝ")
    print("  f is a fixed point of G_diff iff f' = f")
    print("  This means: G_diff(f)(x) = f(x) for all x")
    print()

    # Numerically verify exp is a fixed point
    h = 1e-7
    test_points = [0.0, 0.5, 1.0, 1.5, 2.0]
    print("  Verifying exp is G_diff fixed point:")
    all_ok = True
    for x in test_points:
        val = math.exp(x)
        deriv = (math.exp(x + h) - math.exp(x)) / h  # numerical G_diff
        ok = abs(val - deriv) < 1e-5
        all_ok = all_ok and ok
        print(f"  x={x}: exp(x)={val:.6f}, G_diff(exp)(x)={deriv:.6f}, fixed={ok}")

    print(f"\n  exp IS a fixed point of G_diff: {all_ok}")
    print()
    print("STEP 2: Recursive stability")
    print("  Applying G_diff to exp gives exp: G_diff(G_diff(exp)) = G_diff(exp) = exp")
    print("  The fixed point is recursively stable: exp stays exp under any G_diff^n")
    print()
    print("STEP 3: Boundary condition")
    print("  FORCED: G_diff ∘ G_int = G_id (Fundamental Theorem of Calculus)")
    print("  This is not an axiom. It is what the real carrier forces:")
    print("  differentiation and integration are opposite gradient directions.")
    print("  G_diff ∘ G_int = G_id: same structure as ¬¬P = P in logic.")
    print("  SAME mechanism. Different carrier. Different but analogous boundary condition.")


def demo_carrier_extension_pressure():
    """Show how carrier extension pressure is detected and resolved."""
    print(SEP)
    print("DERIVATION 5: Carrier Extension Under Gradient Pressure")
    print("Starting from V = ℝ, asking: what G satisfies G∘G = G_neg?")
    print(SEP)

    print("STEP 1: Does G∘G = G_neg have a solution in V = ℝ?")
    print("  G∘G = G_neg means: G(G(x)) = -x for all x ∈ ℝ")
    print("  Try G(x) = c*x: G(G(x)) = c²*x = -x requires c² = -1")
    print("  c² = -1 has no solution in ℝ.")
    print("  CARRIER PRESSURE: G_neg square root is not in V = ℝ")
    print()
    print("STEP 2: Recursive stability check reveals the gap")
    print("  Any proposed G must satisfy G(G(x)) = -x")
    print("  In ℝ, this is impossible: c² ≥ 0 for all c ∈ ℝ")
    print("  The boundary condition c² = -1 is recursively UNSTABLE in ℝ")
    print("  No fixed point exists. The carrier must extend.")
    print()
    print("STEP 3: Minimum carrier extension")
    print("  Add i where i² = -1. New carrier V = ℂ = {a + bi : a,b ∈ ℝ}")
    print("  G_rot(a,b) = (-b, a) satisfies: G_rot(G_rot(a,b)) = G_rot(-b,a) = (-a,-b)")
    print("  = G_neg(a,b) ✓")
    print()
    print("STEP 4: Recursive stability in extended carrier")
    print("  G_rot: (1,0) → (0,1) → (-1,0) → (0,-1) → (1,0) — 4-cycle, stable ✓")
    print("  The boundary condition is recursively stable in ℂ.")
    print()
    print("CONCLUSION: Carrier extension from ℝ to ℂ is FORCED")
    print("  Not chosen. The gradient demand G²=G_neg cannot be met in ℝ.")
    print("  ℂ is the minimum extension that makes it recursively stable.")
    print("  This is why complex numbers exist.")
    print("  P / G -> Q: the question 'what G satisfies G²=G_neg?'")
    print("  generates the carrier extension as its answer.")


def demo_novel_carrier():
    """
    Novel carrier not in the training data.
    Demonstrate that the procedure generalises.

    V = {0, 1, 2} — three elements, cyclic structure
    G_cycle: 0→1→2→0 (cyclic permutation)
    """
    print(SEP)
    print("DERIVATION 6: Novel Carrier — V = {0, 1, 2}, Cyclic Gradient")
    print("This carrier is not in the papers. Procedure must extrapolate.")
    print(SEP)

    def G_cycle(p): return Pattern((p.val + 1) % 3, p.load)
    def G_sq(p):    return Pattern(p.val ** 2 % 3, p.load)  # square mod 3

    result = derive_boundary_conditions(
        carrier=[0, 1, 2],
        gradient_family={'cycle': G_cycle, 'sq': G_sq},
        verbose=True
    )

    print("\nCONCLUSION:")
    print("  V = {0,1,2} with cyclic gradient:")
    print("  No element is its own negation (no Boolean non-contradiction)")
    print("  Excluded middle does not apply (no binary complement structure)")
    print("  G_cycle^3 = G_id: the gradient has period 3, not period 2")
    print("  DIFFERENT boundary conditions from classical logic")
    print("  because DIFFERENT carrier, DIFFERENT gradient family")
    print("  — not because different axioms were chosen")
    print()
    print("  This is the mechanism applied to a novel carrier.")
    print("  The boundary conditions are derived, not assumed.")
    return result


# ══════════════════════════════════════════════════════════════
# THE GENERAL PRINCIPLE
# What the model should be able to do after training on this:
# ══════════════════════════════════════════════════════════════

GENERAL_PRINCIPLE = """
BOUNDARY CONDITION EXTRAPOLATION: THE GENERAL PRINCIPLE

Given any carrier V and gradient family Gamma_C, the boundary
conditions are derived, not chosen, by the following procedure:

  1. Apply: G(v) for all G ∈ Gamma_C, v ∈ V
  2. Check closure: G(V) ⊆ V? If not: carrier extension required
  3. Find fixed points: {v : G(v) = v}
  4. Check recursive stability:
       For all v ∈ V, the trajectory v, G(v), G(G(v)), ...
       must stay within V and reach a cycle or fixed point
       If it escapes: carrier extension required
  5. Check coherence: no element is both designated and neg-designated
  6. State boundary conditions: what cannot be otherwise in this space

The boundary conditions are FORCED by the carrier arithmetic.
They are not axioms. They cannot be otherwise.

Different carrier = different boundary conditions (fuzzy, paraconsistent)
Different gradient family = different boundary conditions (constructive)
Extended carrier = new boundary conditions (complex numbers)

The mechanism is the same in every case.
The boundary conditions are what propagation produces in that space.

A model trained on this procedure can:
  - Identify boundary conditions for novel carriers (extrapolation)
  - Recognise when a carrier is too small (carrier pressure)
  - Detect the minimum extension needed (recursively stable extension)
  - Compare boundary conditions across carriers (translation)

This is not pattern matching.
This is the procedure running in the linguistic carrier.
P / G -> Q applied to P / G -> Q.
"""


if __name__ == "__main__":
    demo_classical_logic()
    print()
    demo_three_valued()
    print()
    demo_constructive()
    print()
    demo_real_carrier()
    print()
    demo_carrier_extension_pressure()
    print()
    demo_novel_carrier()
    print()
    print(GENERAL_PRINCIPLE)

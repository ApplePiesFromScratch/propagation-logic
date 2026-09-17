# How to Map Any Formal System to V / G / θ

*The six-step identification guide from the source PDF, restated as this
repo's **admission gate**: a new carrier enters `carriers/` only by
walking these steps, and steps 4–5 must arrive as executable checks
wherever V is finite or the identities are symbolic.*

Every formal system is a specific choice of three parameters: a value
space **V**, a gradient family **G**, and a coherence threshold **θ**.
The propagation operator `P/G→Q` is constant across all of them.

## 1 · Identify V — the value space

What does the system return or produce? Truth values (`{0,1}`, `[0,1]`,
a finite label set), probabilities, states in a Hilbert space, ordinals,
heaps, markings, programs-up-to-contract.

> Classical: `V={0,1}`. Fuzzy: `[0,1]`. Quantum: density matrices.
> Ordinals: CNF terms below ε₀. The Living Map: contract classes.

## 2 · Identify G — the gradient family

What can be done to elements of V? Connectives, updates, brackets,
boundary maps, reductions, transforms.

> Classical: `{NOT, AND, OR}`. Bayes: `{condition, update}`.
> Lie: `{bracket, exp}`. Homology: `{∂ with ∂∂=0}`.

## 3 · Identify θ — the coherence threshold

What counts as acceptance? A designated value (1), a condition
(seriality, orthogonality, consistency of the decoherence functional),
a structural property (σ-additivity, the contract-plus-budget).

## 4 · Derive forced laws by enumeration  ← **must be executable**

For finite V: check every input combination under every G operator —
`carrierlib.finite.laws` does the 15-law sweep, `modal_forced` does all
Kripke frames to n=3, `ltl_valid` does all finite traces. For continuous
V: verify the identity **symbolically** (sympy: `d²=0`, Jacobi, CR
equations, Fisher integrals) or **numerically with stated tolerances**
(EMPIRICAL tier: Itô's quadratic variation, the H-theorem, GRW scaling).

A law is FORCED only if the check decides it. If the honest evidence is
a citation, tag the claim `PRESUMED` with the citation and let the paid
fraction say so.

## 5 · Find failures by counterexample  ← **must be executable**

One witness suffices, and the check should print it: `AND(½,¬½)=½` for
K3's value-reading LNC, the non-reflexive frame refuting T, the
1500-path measurement of `(dW)²=dt` refuting the naive chain rule,
ω=2.1 blowing up SOR.

**When the source document and the enumerator disagree, the enumerator
wins and the record says so.** This library already carries two such
corrections (see the README's findings section).

## 6 · Identify morphisms to other carriers

A morphism `f: V→V'` commutes with the gradients: `f(G(v)) = G'(f(v))`.
`carrierlib.finite.morphism` decides this per-operator on finite V —
which is exactly how the Gödel-threshold map got scoped to its honest
fragment.

---

### Verification principle

Every forced law must be re-derivable from V, G, θ alone by the
procedure above. If it cannot be, it is either an extra axiom (say so)
or the V/G/θ specification is incomplete (fix it). Run
`python library_verify.py` — the file this guide's source PDF names —
to see the whole library priced.

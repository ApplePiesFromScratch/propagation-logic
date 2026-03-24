# Propagation Logic

**A single-operator foundation for logic and calculus.**

*James Pugmire — Independent Researcher — March 2026 (Version 12)*

---
## Philosophy & Ontology

Propagation Logic is grounded in a **process ontology** in which becoming is primary and static substances are derivative.  
See **[ONTOLOGY.md]** **[PHILOSOPHY.md]** for the full philosophical framing.

## Overview

Propagation Logic (PL) is a formal system built on one primitive:

```
P / G → Q
```

A **loaded pattern** `P = (v_P, L_P)` propagates through a **gradient field** `G` in **context** `C`, producing output pattern `Q`. Every propagation step extends the pattern's loaded history. Every history sets the gradient demands for the next step.

Propositional logic, first-order logic, modal logic, probabilistic logic, and the core operations of calculus are each the boundary conditions forced by this mechanism over a specific carrier set with a specific gradient family. They are not separate systems — they are parameter settings of one mechanism.

| Setting | Carrier V | Result |
|---|---|---|
| Full gradient family | `{0,1}` | Classical logic |
| Constructive gradient family | `{0,1}` | Intuitionistic logic |
| Extended threshold | `{0,1}` | Paraconsistent logic |
| Context graph topology | `{0,1}` | K / S4 / S5 modal logic |
| Normalised measure over contexts | `{0,1}` | Kolmogorov probability |
| Arithmetic gradient fields | `ℝ` | Calculus |

The classical laws of logic are arithmetic facts about `{0,1}`, not axioms. The rules of calculus are the same load-combination structure instantiated over `ℝ`. Gödel incompleteness is maximum complexity — a pattern whose loaded history includes itself — operating identically in both settings.

---

## Repository structure

```
propagation-logic/
├── pl/
│   ├── __init__.py       — package exports
│   ├── core.py           — Pattern, Context, all gradient fields (§2–8)
│   └── calculus.py       — CalcPattern, integrate, newton_reconfigure (§13)
├── demos/
│   ├── logic_demos.py    — all inline demonstrations from §2–11
│   └── calculus_demos.py — all inline demonstrations from §13
├── tests/
│   └── test_pl.py        — 40 assertions covering every structural claim
├── README.md
├── LICENSE
└── requirements.txt
```

---

## Quick start

No dependencies beyond the Python standard library.

```bash
git clone https://github.com/<your-username>/propagation-logic
cd propagation-logic
python tests/test_pl.py        # 40 tests, all pass
python demos/logic_demos.py    # §2–11 demonstrations
python demos/calculus_demos.py # §13 demonstrations
```

Or with pytest:

```bash
pip install pytest
pytest tests/
```

---

## Usage

### Logic

```python
from pl.core import Pattern, Context, G_neg, G_and, G_or, G_imp

C = Context(threshold=1.0)   # two-element, unit threshold

P = Pattern(val=1, load=1.0)
Q = Pattern(val=1, load=0.8)

# Non-contradiction: P ∧ ¬P is never designated
assert G_and(P, G_neg(P)).val == 0

# Excluded middle: P ∨ ¬P is always valid
assert C.valid(G_or(P, G_neg(P)))

# Modus Ponens
assert G_imp(P, Q) == Q   # v_P=1 forces Q

# Gradient demand
print(C.demand(Pattern(1, 1.5)))   # 0.5 — reconfiguration pressure
print(C.rate(Pattern(1, 2.0)))     # 0.5 — incoherent pattern propagates slower
```

### Calculus

```python
from pl.calculus import CalcPattern, integrate, newton_reconfigure
import math

# Differentiation: seed with load=1, read derivative as output load
x = CalcPattern(1.0)                   # val=1, load=1 (differentiate w.r.t. x)
r = (x**2) * x.sin()                  # d/dx[x²·sin(x)] at x=1
print(r.load)                          # 2.2232442755...
print(2*math.sin(1) + math.cos(1))     # same, to machine precision

# exp is its own derivative (fixed point of G_exp)
e = CalcPattern(1.0).exp()
assert abs(e.val - e.load) < 1e-12    # val == load always

# Integration
area, n = integrate(lambda t: t**2, 0, 1)
print(area)    # 0.3333333333...

# Optimisation as reconfiguration (Definition 2.6)
# P = (f(x), f'(x)). Coherence: v_P = 0. Step: x ← x − v_P/L_P
def f(x): return CalcPattern(x)**2 - 2

root = newton_reconfigure(f, 1.0)
print(root)              # 1.4142135623...
print(math.sqrt(2))      # same
```

---

## Key concepts

### Loaded pattern

```
P = (v_P, L_P)
```

- `v_P ∈ V` — designation component. Over `{0,1}`: 1 = designated, 0 = undesignated. Over `ℝ`: current value of the expression.
- `L_P ≥ 0` — informational load, the scalar magnitude of the accumulated propagation history `H_P`.

### Context

```
C = (Γ_C, o_C, θ_C)
```

- `Γ_C` — available gradient fields
- `θ_C` — coherence threshold
- `demand(P, C) = max(0, L_P − θ_C)` — reconfiguration pressure
- `valid(P, C)` iff `v_P = 1` and `L_P ≤ θ_C`

### Propagation rate (Theorem 2.1)

```
rate(P, C) = min(L_P, θ_C) / L_P
```

Simpler patterns (lower load) propagate faster. Among incoherent patterns: `rate(P) > rate(Q) ⟺ L_P < L_Q`.

### The gradient fields

| Field | Value rule | Load rule | Name after the cut |
|---|---|---|---|
| `G_id` | `v` | `L` | Identity |
| `G_neg(P)` | `1 − v_P` | `L_P` | Negation |
| `G_and(P,Q)` | `v_P · v_Q` | `L_P + L_Q` | Conjunction |
| `G_or(P,Q)` | `max(v_P, v_Q)` | `min(L_P, L_Q)` | Disjunction |
| `G_imp(P,Q)` | `v_Q` if `v_P=1`, else `1` | `L_Q` if `v_P=1`, else `0` | Implication |

In the calculus regime (`V = ℝ`), the load rules of `G_mul`, `G_pow`, `G_sin`, `G_exp` etc. are exactly the rules of forward-mode automatic differentiation.

### Unification (Theorem 13.4)

Logic and calculus are both instances of the same mechanism over different carrier sets. The product rule and the law of non-contradiction are both consequences of how loaded history propagates through binary operations. The Taylor series and Gödel incompleteness are both instances of Observation 2.2 (maximum complexity) in different carrier settings.

---

## Tests

The test suite (`tests/test_pl.py`) contains 40 assertions covering:

- Support, demand, propagation rate (§2)
- All gradient field definitions and their properties (§3)
- The three classical laws as forced boundary conditions (§4)
- Quantifier load rules: sup for ∀, inf for ∃ (§5)
- Modus Ponens, Hypothetical Syllogism, Consistency (§6, §8)
- Modal K / S4 / S5 from graph topology (§7)
- Kolmogorov axioms from measure over valid contexts (§9)
- Paraconsistent logic from extended threshold (§11)
- Product rule, chain rule, quotient rule, exp fixed point (§13.2)
- Fundamental Theorem of Calculus (§13.3)
- Newton reconfiguration and quadratic convergence (§13.6)
- Unification: same load structure in logic and calculus (§13.5)

All 40 pass with no external dependencies.

---

## Paper

The full paper is included in the repository as `PL-v12.pdf`.

> Pugmire, J. (2026). *Propagation Logic: A Single-Operator Foundation for Logic and Calculus.* Version 12. SSRN. [link]

---

## Licence

MIT — see `LICENSE`.

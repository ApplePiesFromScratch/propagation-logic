# Propagation Logic

**A single mechanistic foundation for all of mathematics — grounded in process ontology.**

*James Pugmire — Independent Researcher — March 2026 (Version 12)*

---

## Philosophy & Ontology

Propagation Logic is grounded in a **process ontology** in which *becoming* is primary and static substances are derivative. Patterns propagate, accumulate history (load), and reconfigure under coherence pressure.

See **[PHILOSOPHY.md](PHILOSOPHY.md)** (main exposition) and the compact technical version **[ONTOLOGY.md](ONTOLOGY.md)**.

All claims are computationally verified and mechanism-based.

---

## Overview

PL is built on **one primitive operator**:

A loaded pattern `P = (v_P, L_P)` propagates through a gradient field `G` inside a context `C`. Load is the living history of the process. Reconfiguration pressure drives change when coherence is exceeded.

Logic, calculus, geometry, topology, category theory, type theory, paradoxes, and the structural core of the Millennium Problems are all **different gradient families and carrier/context tunings** of this single process.

---

## Repository Structure
propagation-logic/
├── pl/
│   ├── core.py
│   └── calculus.py
├── demos/
│   ├── logic_demos.py
│   ├── calculus_demos.py
│   ├── all_mathematics_demo.py          # Logic + calculus + optimization + series + vectors
│   ├── higher_structures_demo.py        # Geometry • Topology • Category • Type Theory
│   ├── paradoxes.py                     # Liar, Russell, Zeno, Curry, Berry as boundary failures
│   └── millennium/
│       ├── run_all.py
│       ├── p_vs_np.py
│       ├── navier_stokes.py
│       ├── yang_mills.py
│       ├── hodge.py
│       ├── bsd.py
│       └── riemann.py
├── tests/test_pl.py
├── PHILOSOPHY.md
├── ONTOLOGY.md
├── PL-v12.pdf
└── LICENSE

---

## Quick Start

```bash
git clone https://github.com/ApplePiesFromScratch/propagation-logic.git
cd propagation-logic

python tests/test_pl.py                          # 40 tests — all pass

# Core demos
python -m demos.logic_demos
python -m demos.calculus_demos

# Big unified demos
python -m demos.all_mathematics_demo             # All mathematics from one process
python -m demos.higher_structures_demo           # Geometry, topology, category & type theory

# Paradoxes & Millennium Problems
python -m demos.paradoxes
python -m demos.millennium.run_all               # All Millennium structural analyses
from pl.core import Pattern, Context, G_neg, G_and, G_or, G_imp

C = Context(threshold=1.0)

P = Pattern(val=1, load=1.0)
Q = Pattern(val=1, load=0.8)

assert G_and(P, G_neg(P)).val == 0                    # non-contradiction
assert C.valid(G_or(P, G_neg(P)))                     # excluded middle
assert G_imp(P, Q) == Q                               # modus ponens
from pl.calculus import CalcPattern, integrate, newton_reconfigure

x = CalcPattern(2.0)
y = (x ** 3) * x.sin()
print(y.val, y.load)          # value + derivative

area, _ = integrate(lambda t: t**2, 0, 1)
root = newton_reconfigure(lambda x: x**2 - 2, 1.0)
### Key Concepts

- **Pattern**: The fundamental entity. `P = (val, load)` — `val` is the current designation, `load` is accumulated propagation history.
- **Context**: Defines the coherence threshold `θ_C` and available gradient fields.
- **Gradient Field** (`G`): Defines how patterns combine and how load accumulates.
- **Reconfiguration Pressure**: `demand = max(0, load - θ_C)` — the mechanistic driver of change.
- **Propagation**: `P / G → Q` — the single primitive operation.

### Gradient Families (Boundary Conditions)

| Domain                    | Carrier Set | Gradient Family Tuning                  | Resulting System                     |
|---------------------------|-------------|-----------------------------------------|--------------------------------------|
| Classical Logic           | {0,1}       | Full Boolean gradients                  | Non-contradiction, modus ponens      |
| Intuitionistic Logic      | {0,1}       | Constructive / restricted gradients     | No excluded middle                   |
| Paraconsistent Logic      | {0,1}       | High coherence threshold                | Tolerates contradiction              |
| Calculus                  | ℝ           | Arithmetic forward-mode gradients       | Differentiation, integration, Newton |
| Geometry                  | Vector patterns | Distance & continuity gradients      | Euclidean distance, continuity       |
| Topology                  | Context topology | Load-preserving propagation           | Open sets, continuous maps           |
| Category Theory           | Gradients as morphisms | Composition of gradients            | Functors, natural transformations    |
| Type Theory               | Contexts as types | Inhabitation via coherence            | Dependent types, proofs as patterns  |
| Paradoxes                 | Self-referential gradients | Load recursion                        | Failed reconfigurations              |
| Millennium Problems       | High-dimensional carriers | Load asymmetry, fixed-point isolation | Structural analysis of open problems |

Full technical development and formal proofs: PL-v12.pdf

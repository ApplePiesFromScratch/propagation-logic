# Propagation Logic

**A single mechanistic foundation for all of mathematics — grounded in process ontology.**

*James Pugmire — Independent Researcher — March 2026 (Version 12)*

---

## Philosophy & Ontology

Propagation Logic is grounded in a **process ontology** in which *becoming* is primary and static substances are derivative. Patterns propagate, accumulate history (load), and reconfigure under coherence pressure.

See **[PHILOSOPHY.md](PHILOSOPHY.md)** (main exposition) and the compact technical version **[ONTOLOGY.md](ONTOLOGY.md)**.

---

## Overview

Propagation Logic (PL) is a formal system built on one primitive:
P / G → Q
textA loaded pattern `P = (v_P, L_P)` propagates through a gradient field `G` in context `C`, producing output pattern `Q`. Every propagation step extends the pattern’s loaded history.

Propositional logic, first-order logic, modal logic, probabilistic logic, and the core operations of calculus are each the boundary conditions forced by this mechanism over a specific carrier set with a specific gradient family. They are not separate systems — they are parameter settings of one mechanism.

### Gradient Families

| Setting                          | Carrier V   | Result                                      |
|----------------------------------|-------------|---------------------------------------------|
| Full gradient family             | {0,1}       | Classical logic                             |
| Constructive gradient family     | {0,1}       | Intuitionistic logic                        |
| Extended threshold               | {0,1}       | Paraconsistent logic                        |
| Context graph topology           | {0,1}       | K / S4 / S5 modal logic                     |
| Normalised measure over contexts | {0,1}       | Kolmogorov probability                      |
| Arithmetic gradient fields       | ℝ           | Calculus                                    |

The classical laws of logic are arithmetic facts about {0,1}, not axioms. The rules of calculus are the same load-combination structure instantiated over ℝ. Gödel incompleteness is maximum complexity — a pattern whose loaded history includes itself — operating identically in both settings.

---

## Repository Structure

```bash
propagation-logic/
├── pl/
│   ├── core.py           # Pattern, Context, all gradient fields
│   ├── calculus.py       # CalcPattern, integrate, newton_reconfigure
│   └── dras.py           # DRAS v4 — De-Reification Axiom Standard
├── demos/
│   ├── all_mathematics_demo.py      # Logic + calculus + optimization + series + vectors
│   ├── higher_structures_demo.py    # Geometry • Topology • Category • Type Theory
│   ├── paradoxes.py                 # Liar, Russell, Zeno, Curry, Berry
│   ├── dras_demo.py                 # DRAS v4 demonstration
│   ├── finite_demo.py               # Explicit finite number theory
│   ├── logic_demos.py
│   ├── calculus_demos.py
│   └── millennium/
│       ├── run_all.py
│       ├── p_vs_np.py
│       ├── navier_stokes.py
│       ├── yang_mills.py
│       ├── hodge.py
│       ├── bsd.py
│       └── riemann.py
├── tests/
│   └── test_pl.py        # 40 assertions covering every structural claim
├── PHILOSOPHY.md
├── ONTOLOGY.md
├── PL-v12.pdf
├── LICENSE
└── requirements.txt

Quick Start
Bashgit clone https://github.com/ApplePiesFromScratch/propagation-logic.git
cd propagation-logic

python tests/test_pl.py                          # 40 tests — all pass

# Core demos
python -m demos.logic_demos
python -m demos.calculus_demos

# Big unified demos
python -m demos.all_mathematics_demo             # All mathematics from one process
python -m demos.higher_structures_demo           # Geometry, topology, category & type theory
python -m demos.dras_demo                        # DRAS v4 demonstration
python -m demos.finite_demo                      # Finite number theory enforcement

# Paradoxes & Millennium Problems
python -m demos.paradoxes
python -m demos.millennium.run_all               # All Millennium structural analyses

Usage Examples
Logic
Pythonfrom pl.core import Pattern, Context, G_and, G_neg, G_or, G_imp

C = Context(threshold=1.0)
P = Pattern(val=1, load=1.0)
Q = Pattern(val=1, load=0.8)

assert G_and(P, G_neg(P)).val == 0                    # non-contradiction
assert C.valid(G_or(P, G_neg(P)))                     # excluded middle
assert G_imp(P, Q) == Q                               # modus ponens
Calculus
Pythonfrom pl.calculus import CalcPattern, integrate, newton_reconfigure
import math

x = CalcPattern(2.0)
y = (x ** 3) * x.sin()
print(y.val, y.load)          # value + derivative carried in load

DRAS Calculus (De-Reification Axiom Standard v4)
DRAS is a full de-reified extension of Propagation Logic.

Every quantity is a LoadedHistory α(E,x,t) — no constants exist.
Universal loading formula: q(E) = q₀ / (1 ± β·ln(E/E₀))
Explicit finite number theory: unbounded propagation (infinities) is rejected.
β and E₀ propagate correctly through arithmetic operations.

Run the demos:
Bashpython -m demos.dras_demo      # Main DRAS demonstration
python -m demos.finite_demo    # Shows rejection of unbounded load
This extension maintains the single mechanistic core (P / G → Q) while fully satisfying the DRAS axioms of de-reification and finitism.

Key Concepts

## Key Concepts

- **Pattern**: A propagating process. Written as `P = (val, load)`, where `val` is the transient designation (what appears as “value”) and `load` **is** the accumulated history of propagation itself. There are no static entities — only ongoing becoming.
- **Context**: The environment of propagation, defined by the available gradient fields and a coherence threshold `θ_C`.
- **Gradient Field** (`G`): The rule governing how one pattern propagates into another (`P / G → Q`).
- **Reconfiguration Pressure**: `demand = max(0, load - θ_C)` — the intrinsic driver of change when coherence is exceeded.
- **Propagation**: The single primitive operation `P / G → Q`. All structure (logic, calculus, geometry, etc.) emerges from this process under different boundary conditions.
- **Finite Number Theory**: All propagation is strictly bounded. Unbounded load growth (infinities) is disallowed because it would violate coherence. When load approaches the finite limit, reconfiguration must occur.

No substances. No eternal objects. Only processes in ongoing relation.
Paper
The full paper is included in the repository as PL-v12.pdf.

Contributions that deepen the process-ontological framing or extend DRAS are especially welcome.

Repository: https://github.com/ApplePiesFromScratch/propagation-logic

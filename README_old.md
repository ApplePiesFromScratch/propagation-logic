# Propagation Logic

**A single mechanistic foundation for all of mathematics and logic — grounded in process ontology.**

*James Pugmire — Independent Researcher — March 2026 (Version 12)*

---

## The Single Mechanism

**P / G → Q**

A loaded pattern `P = (v, L)` propagates through a gradient field `G` in a context `C`, producing a new pattern `Q`.  
Load `L` **is** the accumulated history of the process itself.  
Reconfiguration pressure (`demand = max(0, L - θ)`) drives all change when coherence is exceeded.

**Everything** — classical logic, intuitionistic logic, calculus, geometry, topology, category theory, probability, game theory, paradoxes, and the structural skeletons of the Millennium Problems — emerges as different **gradient families** and **carrier tunings** of this one process.

No separate axioms. No eternal objects. Only processes in ongoing relation.

### Gradient Families

| Setting                          | Carrier V   | Result                                      |
|----------------------------------|-------------|---------------------------------------------|
| Full gradient family             | {0,1}       | Classical logic                             |
| Constructive gradient family     | {0,1}       | Intuitionistic logic                        |
| Extended threshold               | {0,1}       | Paraconsistent logic                        |
| Context graph topology           | {0,1}       | K / S4 / S5 modal logic                     |
| Normalised measure over contexts | {0,1}       | Kolmogorov probability                      |
| Arithmetic gradient fields       | ℝ           | Calculus                                    |

---

## Repository Structure

```bash
propagation-logic/
├── pl/                          # Core implementation of the single mechanism
│   ├── core.py                  # Pattern, Context, gradient fields (logic + base)
│   ├── calculus.py              # CalcPattern, integrate, newton_reconfigure
│   └── dras.py                  # DRAS v4 — De-Reification Axiom Standard (finite, no constants)
├── demos/                       # Runnable Python demonstrations
│   ├── all_mathematics_demo.py
│   ├── higher_structures_demo.py
│   ├── paradoxes.py
│   ├── logic_demos.py
│   ├── calculus_demos.py
│   ├── dras_demo.py
│   ├── finite_demo.py
│   ├── mathesis_demo.py
|   ├── grammar-as-propagation.py
│   └── millennium/              # Structural analyses of the 7 Millennium Problems
├── explorations/                # Interactive visual explorations (Mathesis Universalis)
│   ├── mathesis_explorer.jsx    # Fixed points, sin/cos emergence, e/π/φ, logistic map,
│   │                            # Mandelbrot, dual numbers, full hierarchy
│   └── pl_game_theory.jsx       # Shared-carrier games, Nash vs Joint Coherence,
│                                # replicator dynamics, gradient geometry, game builder
├── tests/
│   └── test_pl.py               # 40 assertions — all structural claims verified
├── docs/
│   ├── PHILOSOPHY.md
│   ├── ONTOLOGY.md
│   ├── mathesis_universalis.pdf # Full long-form paper
│   └──PL-v12.pdf                   # Core technical paper (v12)
├── LICENSE
├── README.md
└── requirements.txt             # Pure standard library (no external deps)
Quick Start
Bashgit clone https://github.com/ApplePiesFromScratch/propagation-logic.git
cd propagation-logic

python tests/test_pl.py                  # 40 tests — all pass
Core Demos (run any of these)
Bashpython -m demos.all_mathematics_demo     # Unified math + logic from one mechanism
python -m demos.higher_structures_demo   # Geometry • Topology • Category • Type Theory
python -m demos.paradoxes                # Liar, Russell, Zeno, Curry, Berry
python -m demos.millennium.run_all       # All 7 Millennium Problems (structural view)
DRAS (De-Reification Axiom Standard v4)
Bashpython -m demos.dras_demo                # Full DRAS demonstration
python -m demos.finite_demo              # Explicit finite number theory

Interactive Explorations — Mathesis Universalis
Open these two files in a browser (see explorations/README.md for the 10-second setup using Babel standalone or Vite):

explorations/mathesis_explorer.jsx — Fixed points of derivatives, emergence of sin & cos, convergence signatures of e/π/φ, logistic map, Mandelbrot set, dual numbers (forward AD), full propagation hierarchy.
explorations/pl_game_theory.jsx — Game theory derived directly from the mechanism: shared carrier, drag, Nash Equilibrium vs Joint Coherence, iterated play, replicator dynamics (Theorem 2.1), gradient geometry, and a live game builder.

These make the single mechanism immediately visible and interactive.

Usage Examples
Logic (classical)
Pythonfrom pl.core import Pattern, Context, G_and, G_neg, G_or, G_imp

C = Context(threshold=1.0)
P = Pattern(val=1, load=1.0)
Q = Pattern(val=1, load=0.8)

assert G_and(P, G_neg(P)).val == 0                    # non-contradiction
assert C.valid(G_or(P, G_neg(P)))                     # excluded middle
assert G_imp(P, Q) == Q                               # modus ponens
Calculus (dual-number style)
Pythonfrom pl.calculus import CalcPattern

x = CalcPattern(2.0)
y = (x ** 3) * x.sin()          # derivative travels automatically in .load
print(y.val, y.load)            # value + exact derivative
DRAS v4 (finite, de-reified)
See demos/dras_demo.py — every quantity is a LoadedHistory with no constants.

Key Concepts

Pattern — propagating process P = (val, load)
Load — accumulated history (not a separate variable)
Context — coherence threshold θ + available gradients
Gradient Field G — rule of propagation (P / G → Q)
Reconfiguration Pressure — demand = max(0, load - θ)
Coherence — load ≤ θ

All of mathematics and logic are different tunings of this one process.

Papers

PL-v12.pdf — Core technical development
docs/mathesis_universalis.pdf — Full philosophical & structural exposition


Philosophy & Ontology
See docs/PHILOSOPHY.md (main exposition) and docs/ONTOLOGY.md (compact technical version).

Contributions that deepen the process-ontological framing or extend DRAS are warmly welcome.
Repository: https://github.com/ApplePiesFromScratch/propagation-logic
One mechanism. All of mathematics and logic.

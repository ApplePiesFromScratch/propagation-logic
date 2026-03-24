# Propagation Logic

**A single mechanistic foundation for all of mathematics — grounded in process ontology.**

*James Pugmire — Independent Researcher — March 2026 (Version 12)*

---

## Philosophy & Ontology

Propagation Logic is grounded in a **process ontology** in which *becoming* is primary and static substances are derivative. Patterns do not possess properties — they propagate, accumulate history (load), and reconfigure under coherence pressure.

See **[PHILOSOPHY.md](PHILOSOPHY.md)** (main exposition) and the compact technical version **[ONTOLOGY.md](ONTOLOGY.md)**.

All claims are computationally verified and mechanism-based.

---

## Overview

Propagation Logic (PL) is built on **one primitive operator**:
P / G → Q
textA **loaded pattern** `P = (v_P, L_P)` propagates through a **gradient field** `G` inside a **context** `C`, producing `Q`. Load `L_P` is the accumulated history of the process itself. Reconfiguration pressure appears when load exceeds the coherence threshold.

**Logic, calculus, geometry, topology, category theory, type theory, paradoxes, and even the structural skeletons of the Millennium Problems** are all different **gradient families** and **carrier/context tunings** of this single process.

| Domain                  | Carrier / Tuning                  | Manifestation                              |
|-------------------------|-----------------------------------|--------------------------------------------|
| Classical Logic         | {0,1} + full gradients            | Non-contradiction, modus ponens, etc.     |
| Intuitionistic Logic    | {0,1} + constructive gradients    | Restricted propagation                     |
| Paraconsistent Logic    | {0,1} + high threshold            | Tolerates contradiction                    |
| Calculus                | ℝ + arithmetic gradients          | Differentiation, integration, Newton      |
| Geometry / Topology     | Vector patterns + context topology| Distance, continuity, open sets            |
| Category / Type Theory  | Gradients as morphisms, contexts as types | Composition, inhabitation, functors       |
| Paradoxes               | Self-referential gradients        | Failed reconfigurations (Liar, Russell…)  |
| Millennium Problems     | High-dimensional carriers         | Load asymmetry, fixed-point isolation, etc.|

Classical laws and calculus rules emerge as **forced stabilizations** of the same load-combination arithmetic. Paradoxes are boundary failures of the mechanism. The Millennium Problems appear as deep questions about load, coherence, and gradient families.

---

## Repository Structure
propagation-logic/
├── pl/
│   ├── init.py
│   ├── core.py           # Pattern, Context, logical gradients
│   └── calculus.py       # CalcPattern, integrate, newton_reconfigure
├── demos/
│   ├── logic_demos.py
│   ├── calculus_demos.py
│   ├── all_mathematics_demo.py      # Unified logic + calculus + optimization + series + vectors
│   ├── higher_structures_demo.py    # Geometry • Topology • Category • Type Theory
│   ├── paradoxes.py                 # Liar, Russell, Zeno, Curry, Berry as boundary failures
│   └── millennium/
│       ├── run_all.py
│       ├── p_vs_np.py
│       ├── navier_stokes.py
│       ├── yang_mills.py
│       ├── hodge.py
│       ├── bsd.py
│       └── riemann.py               # (plus any others you add)
├── tests/
│   └── test_pl.py        # 40 assertions — all pass
├── PHILOSOPHY.md
├── ONTOLOGY.md
├── PL-v12.pdf
├── LICENSE
└── requirements.txt
text---

## Quick Start

No external dependencies (pure Python standard library).

```bash
git clone https://github.com/ApplePiesFromScratch/propagation-logic.git
cd propagation-logic

python tests/test_pl.py                    # 40 tests — all pass

# Core demos
python -m demos.logic_demos
python -m demos.calculus_demos

# Big unified demos
python -m demos.all_mathematics_demo       # All mathematics from one process
python -m demos.higher_structures_demo     # Geometry, topology, category & type theory

# Paradoxes & Millennium Problems
python -m demos.paradoxes
python -m demos.millennium.run_all         # Runs paradoxes + all Millennium structural analyses

Key Demos (Recommended Order)

all_mathematics_demo.py — Logic, calculus, optimization, series, vectors, probability — all in one file.
higher_structures_demo.py — Geometry, topology, category theory, type theory as gradient families.
paradoxes.py — Shows how every major paradox is a failed reconfiguration (boundary constraint).
millennium/run_all.py — Structural PL analysis of all seven Millennium Problems (with computational verification where possible).


Usage Examples
Logic (core.py)
Pythonfrom pl.core import Pattern, Context, G_and, G_neg, G_or, G_imp

C = Context(threshold=1.0)
P = Pattern(1, 1.0)
Q = Pattern(1, 0.8)

assert G_and(P, G_neg(P)).val == 0                    # non-contradiction
assert C.valid(G_or(P, G_neg(P)))                     # excluded middle
assert G_imp(P, Q) == Q                               # modus ponens
Calculus (calculus.py)
Pythonfrom pl.calculus import CalcPattern, integrate, newton_reconfigure

x = CalcPattern(2.0)
y = (x ** 3) * x.sin()
print(y.val, y.load)          # value + derivative carried in load

area, steps = integrate(lambda t: t**2, 0, 1)
root = newton_reconfigure(lambda x: x**2 - 2, 1.0)
Higher Structures & Paradoxes
Run the dedicated demo files — they contain extensive inline explanations tied directly to the paper and PHILOSOPHY.md.

Tests & Verification
tests/test_pl.py contains 40 assertions that verify:

All gradient laws and propagation rules
Classical, intuitionistic, paraconsistent, modal, and probabilistic logic
Full calculus rules (product/chain/FTC, Newton convergence)
Unification claims (same load structure for logic and calculus)

All tests pass.
The paradox and Millennium demos provide additional computational verification of structural claims.

Paper
The full technical development is in PL-v12.pdf (included in the repository).

Contributing
Contributions that deepen the process-ontological framing, add new gradient families, improve visualizations of propagation-as-becoming, or extend the Millennium / paradox analyses are especially welcome.
See PHILOSOPHY.md for the guiding spirit.

Repository: github.com/ApplePiesFromScratch/propagation-logic

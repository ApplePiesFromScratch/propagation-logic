# Propagation Logic

**A single mechanistic foundation for all of mathematics — grounded in process ontology.**

*James Pugmire — Independent Researcher — March 2026 (Version 12)*

---

## Philosophy & Ontology

Propagation Logic is grounded in a **process ontology** in which *becoming* is primary and static substances are derivative. Patterns do not possess properties — they propagate, accumulate history (load), and reconfigure under coherence pressure.

See **[PHILOSOPHY.md](PHILOSOPHY.md)** (main exposition) and the compact technical version **[ONTOLOGY.md](ONTOLOGY.md)**.

All claims are computationally verified from the single mechanism `P / G → Q`.

---

## Overview

PL is built on **one primitive operator**:

A loaded pattern `P = (v_P, L_P)` propagates through a gradient field `G` inside a context `C`. Load `L_P` **is** the accumulated history of the process itself. Reconfiguration pressure appears when load exceeds the coherence threshold.

**Everything** — logic, calculus, geometry, topology, category theory, type theory, paradoxes, and the structural skeletons of the Millennium Problems — emerges as different **gradient families** and **carrier/context tunings** of this single process.

---

## Repository Structure

```bash
propagation-logic/
├── pl/
│   ├── core.py           # Pattern, Context, logical gradients
│   └── calculus.py       # CalcPattern, integrate, newton_reconfigure
├── demos/
│   ├── all_mathematics_demo.py      # Logic + calculus + optimization + series + vectors
│   ├── higher_structures_demo.py    # Geometry • Topology • Category • Type Theory
│   ├── paradoxes.py                 # Liar, Russell, Zeno, Curry, Berry as boundary failures
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
│   └── test_pl.py        # 40 assertions — all pass
├── PHILOSOPHY.md
├── ONTOLOGY.md
├── PL-v12.pdf
├── LICENSE
└── requirements.txt

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
---
*Usage*
---
from pl.core import Pattern, Context, G_and, G_neg, G_or, G_imp

C = Context(threshold=1.0)
P = Pattern(val=1, load=1.0)
Q = Pattern(val=1, load=0.8)

assert G_and(P, G_neg(P)).val == 0                    # non-contradiction
assert C.valid(G_or(P, G_neg(P)))                     # excluded middle
assert G_imp(P, Q) == Q                               # modus ponens

from pl.calculus import CalcPattern, integrate, newton_reconfigure

x = CalcPattern(2.0)
y = (x ** 3) * x.sin()
print(y.val, y.load)          # value + derivative carried in load

Key Concepts & Gradient Families

Pattern: The fundamental entity. P = (val, load) — val is the current designation, load is accumulated propagation history.
Context: Defines the coherence threshold θ_C and available gradient fields.
Gradient Field (G): Defines how patterns combine and how load accumulates.
Reconfiguration Pressure: demand = max(0, load - θ_C) — the mechanistic driver of change.
Propagation: P / G → Q — the single primitive operation.

Gradient Families (Boundary Conditions)



























































DomainCarrier SetGradient Family TuningResulting SystemClassical Logic{0,1}Full Boolean gradientsNon-contradiction, modus ponensIntuitionistic Logic{0,1}Constructive / restrictedNo excluded middleParaconsistent Logic{0,1}High coherence thresholdTolerates contradictionCalculusℝArithmetic forward-modeDifferentiation, integration, NewtonGeometry / TopologyVector patternsDistance & continuity gradientsEuclidean distance, open setsCategory / Type TheoryGradients as morphismsComposition & inhabitationFunctors, dependent typesParadoxesSelf-referentialLoad recursionFailed reconfigurationsMillennium ProblemsHigh-dimensionalLoad asymmetry, fixed-point isolationStructural analysis of open problems

DRAS Calculus (De-Reification Axiom Standard)
A forthcoming extension (pl/dras.py) will add full DRAS v4 support on top of the same PL mechanism — every quantity becomes a LoadedHistory α(E,x,t) with universal loading, no constants, and thermodynamic coherence built in.

Tests & Verification
tests/test_pl.py contains 40 assertions that all pass, covering logic laws, calculus rules, and the unification claims.
The paradox and Millennium demos provide additional computational verification of structural claims.

Paper
Full technical development: PL-v12.pdf

Contributions that deepen the process-ontological framing or extend DRAS are especially welcome. See PHILOSOPHY.md.

Repository: https://github.com/ApplePiesFromScratch/propagation-logic
A single mechanistic process — load as living history, coherence pressure as driver of change — from which all of mathematics emerges.

# Propagation Logic

**A single mechanistic foundation for all of mathematics — grounded in process ontology.**

*James Pugmire — Independent Researcher — March 2026 (Version 12)*

---

## Philosophy & Ontology

Propagation Logic is grounded in a **process ontology** in which *becoming* is primary and static substances are derivative. Patterns propagate, accumulate history (load), and reconfigure under coherence pressure.

See **[PHILOSOPHY.md](PHILOSOPHY.md)** (main exposition) and the compact technical version **[ONTOLOGY.md](ONTOLOGY.md)**.

---


A loaded pattern `P = (v_P, L_P)` propagates through a gradient field `G` in context `C`. Load `L_P` **is** the accumulated history of the process itself. Reconfiguration pressure drives change when coherence is exceeded.

Logic, calculus, geometry, topology, category theory, type theory, paradoxes, game theory, and the structural skeletons of the Millennium Problems all emerge as different **gradient families** and **carrier/context tunings** of this single process.

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
├── pl/
│   ├── core.py           # Pattern, Context, all gradient fields
│   ├── calculus.py       # CalcPattern, integrate, newton_reconfigure
│   └── dras.py           # DRAS v4 — De-Reification Axiom Standard (finite, no constants)
├── demos/
│   ├── all_mathematics_demo.py
│   ├── higher_structures_demo.py
│   ├── paradoxes.py
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
├── explorations/                    # Mathesis Universalis — interactive visual explorations
│   ├── mathesis_explorer.jsx
│   └── pl_game_theory.jsx
├── tests/
│   └── test_pl.py        # 40 assertions covering every structural claim
├── docs/
│   ├── PHILOSOPHY.md
│   ├── ONTOLOGY.md
│   └── mathesis_universalis.pdf     # Full long-form paper
├── PL-v12.pdf
├── LICENSE
└── requirements.txt
git clone https://github.com/ApplePiesFromScratch/propagation-logic.git
cd propagation-logic

python tests/test_pl.py                          # 40 tests — all pass

# Core & unified demos
python -m demos.all_mathematics_demo
python -m demos.higher_structures_demo
python -m demos.dras_demo                        # DRAS v4
python -m demos.finite_demo                      # Finite number theory

# Paradoxes & Millennium
python -m demos.paradoxes
python -m demos.millennium.run_all

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

x = CalcPattern(2.0)
y = (x ** 3) * x.sin()
print(y.val, y.load)          # value + derivative carried in load

DRAS Calculus (De-Reification Axiom Standard v4)
DRAS is the fully de-reified extension of Propagation Logic.

Every quantity is a LoadedHistory α(E,x,t) — no constants.
Universal loading formula: q(E) = q₀ / (1 ± β·ln(E/E₀))
Explicit finite number theory: unbounded propagation (infinities) is rejected.
β and E₀ propagate correctly through arithmetic.

Bashpython -m demos.dras_demo      # Main DRAS demonstration
python -m demos.finite_demo    # Finite number theory enforcement

Interactive Explorations — Mathesis Universalis
The repository now includes two rich, interactive React-based explorations that make the mechanism tangible:

explorations/mathesis_explorer.jsx — Fixed points of differential operators, emergence of sin/cos, the three constants (e, π, φ), logistic map, Mandelbrot set, dual numbers, and the full propagation hierarchy.
explorations/pl_game_theory.jsx — Shared carrier games, iterated play, strategy evolution (replicator dynamics = Theorem 2.1), gradient geometry of the load landscape, and a custom game builder.

These visualizations demonstrate the mechanism in action: coherence boundaries, reconfiguration pressure, drag regimes, and fixed-point emergence become directly observable.

Key Concepts

Pattern: A propagating process. P = (val, load) where val is the transient designation and loadis the accumulated history of propagation itself.
Context: Defines available gradient fields and coherence threshold θ_C.
Gradient Field (G): Rule governing how patterns propagate (P / G → Q).
Reconfiguration Pressure: demand = max(0, load - θ_C) — intrinsic driver of change.
Finite Number Theory: All propagation is strictly bounded. Infinities (unbounded load) are disallowed as they violate coherence.

No substances. No eternal objects. Only processes in ongoing relation.

Paper

PL-v12.pdf — Core technical development
docs/mathesis_universalis.pdf — Full philosophical and structural paper (Mathesis Universalis)


Contributions that deepen the process-ontological framing or extend DRAS are especially welcome.

Repository: https://github.com/ApplePiesFromScratch/propagation-logic
A single mechanistic process — load as living history, coherence pressure as driver of change — from which all of mathematics emerges.
text

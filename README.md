# Propagation Logic

**One fixed propagation operator. Three parameters. Every formal system.**

`P / G → Q`

A single dynamical mechanism — loaded pattern propagation under gradient constraints — generates classical logic, all major non-classical logics, differential and integral calculus, number systems, probability theory, and the De-Reification Axiom Standard (DRAS). No additional axioms. No zero-cost primitives. The laws are forced by carrier arithmetic.

---

### The Core Insight

Every formal system is completely specified by three parameters:

- **V** — Value carrier (the space of possible designations: `{0,1}`, `{0,B,1}`, `[0,1]`, `ℝ`, `ℕ`, `ℂ`, …)
- **Γ** — Gradient family (the allowed operations: `full_bool`, `constructive`, `linear`, `differential`, …)
- **θ** — Coherence threshold (stability cutoff: `1.0` for crisp boolean, `0.0` for continuous/infinitesimal)

Change any one parameter and the entire set of forced laws changes mechanically. Paradoxes are not metaphysical mysteries — they are **thermodynamic load profiles** where a pattern's gradient demand exceeds the context's coherence capacity. The framework pays the energetic debt from the first step.

This is not analogy. It is structural identity. The same propagation engine that forces `¬¬P = P` in the boolean carrier also forces the Fundamental Theorem of Calculus in the real carrier.

---

### Canonical References (2026)

- **[Carrier Set Framework v2](docs/carrier_set_framework_v2.pdf)** — Complete teaching curriculum, carrier-set analysis, and implementation manual. The practical "how to use" guide.
- **[PL + DRAS + Calculus Unified v1](docs/PL_DRAS_Calculus_Unified_v1.pdf)** — Full mechanism, loaded-history calculus, zero-cost distinction fallacy, paradoxes as thermodynamic debt, DRAS, number systems as propagation structures, and self-application of the framework.

---

### Quick Start

```bash
git clone https://github.com/ApplePiesFromScratch/propagation-logic.git
cd propagation-logic

# Interactive tutorial
python core/carrier_tool.py --learn

# Full classical logic report
python core/carrier_tool.py classical

# See exactly what changes between two logics
python core/carrier_tool.py --diff classical intuitionistic

# Run the complete validation suite
python core/pl_unified.py
```

---

### What You Can Do Today

- Switch carriers and instantly derive different logics
- Run differential calculus as a direct extension of the same operator
- Explore paradoxes as explicit load profiles (Liar, Gödel, Russell, Yablo)
- Onboard new formal systems via JSON carriers — see `carriers/_schema.json`
- Verify every claim computationally — machine-precision calculus, falsifiable boundaries

---

### Repository Layout

```
propagation-logic/
├── core/
│   ├── pl_unified.py           Reference implementation (§0–§12, all assertions)
│   ├── carrier_tool.py         CLI: explore, diff, compare, and validate carriers
│   └── pl_paradox_engine.py    Paradox classification and load profiling
│
├── carriers/
│   ├── _schema.json            Schema every carrier definition must satisfy
│   ├── _template.json          Starting point for new carriers
│   └── *.json                  Classical, intuitionistic, paraconsistent, modal, …
│
├── demos/                      Self-contained worked examples
│   ├── pl_friendship_paradox.py
│   ├── pl_coastline.py
│   ├── pl_math_engine.py
│   ├── grammar_as_propagation.py
│   ├── quantum_b_state.py
│   ├── build_a_logic.py
│   └── flux_gradient.py
│
├── tests/                      Automated falsification suite
│   ├── test_carriers.py
│   └── test_unified.py
│
├── explorations/               Experimental extensions (no stability guarantee)
│
└── docs/                       Canonical PDFs
```

---

### Philosophy

> Code over philosophy. Mechanisms over tautologies. Parsimony over orthodoxy.

The foundational error of Western formal systems was the zero-cost distinction fallacy — treating the output of an energetically expensive boundary-maintenance process (identity, truth, constants) as a free primitive. Every paradox is the bill arriving. Propagation Logic pays the debt at the propagation layer itself.

---

### Status

- ✅ Single unified mechanism proven across logic, calculus, and DRAS
- ✅ Carrier tool with JSON schema and falsifiability standard
- ✅ Automated assertions passing across all sections (§0–§12)
- 🔄 Interactive CarrierExplorer web UI
- 🔄 Community carrier registry and new formal systems

We are building the Mathesis Universalis that actually runs.

---

### Contributing

See `CONTRIBUTING.md`. Every new carrier must include:

- At least one mathematically forced law with proof
- At least one explicit failure mode
- A pytest falsification test

New carriers are welcome. The framework is deliberately designed for rapid, falsifiable extension.

Every major claim in this repository is demonstrated in running code.  
Run `python core/pl_unified.py` and see for yourself.

Built with the explicit goal of being more falsifiable than what it replaces.

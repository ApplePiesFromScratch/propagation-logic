# Propagation Logic

**One fixed propagation operator. Three parameters. Every formal system.**

`P / G → Q`

A single dynamical mechanism — loaded pattern propagation under gradient constraints — generates classical logic, all major non-classical logics, differential and integral calculus, number systems, probability theory, and the De-Reification Axiom Standard (DRAS). No additional axioms. No zero-cost primitives. The laws are forced by carrier arithmetic.

### The Core Insight

Every formal system is completely specified by three parameters:
- **V** — Value carrier (the space of possible designations: `{0,1}`, `{0,B,1}`, `[0,1]`, `ℝ`, `ℕ`, `ℂ`, …)
- **Γ** — Gradient family (the allowed operations: `full_bool`, `constructive`, `linear`, `differential`, …)
- **θ** — Coherence threshold (stability cutoff: `1.0` for crisp boolean, `0.0` for continuous/infinitesimal)

Change any one parameter and the entire set of forced laws changes mechanically. Paradoxes are not metaphysical mysteries — they are **thermodynamic load profiles** where a pattern’s gradient demand exceeds the context’s coherence capacity. The framework pays the energetic debt from the first step.

This is not analogy. It is structural identity. The same propagation engine that forces `¬¬P = P` in the boolean carrier also forces the Fundamental Theorem of Calculus in the real carrier.

### Main Canonical References (2026)

These two documents are the **official foundation** of the project:

- **[Carrier Set Framework v2](docs/carrier_set_framework_v2.pdf)**  
  Complete teaching curriculum, carrier-set analysis, and implementation manual. The practical “how to use” guide.

- **[PL + DRAS + Calculus Unified v1](docs/PL_DRAS_Calculus_Unified_v1.pdf)**  
  Full mechanism, loaded-history calculus, zero-cost distinction fallacy, paradoxes as thermodynamic debt, DRAS, number systems as propagation structures, and self-application of the framework.

### Quick Start

```bash
# Clone and explore
git clone https://github.com/ApplePiesFromScratch/propagation-logic.git
cd propagation-logic

# Interactive tutorial
python core/carrier_tool.py --learn

# Full classical logic report
python core/carrier_tool.py classical

# See exactly what changes between logics
python core/carrier_tool.py --diff classical intuitionistic

# Run the complete validation suite (69 assertions)
python core/pl_unified.py
What You Can Do Today

Switch carriers and instantly derive different logics
Run differential calculus as a direct extension of the same operator
Explore paradoxes as explicit load profiles (Liar, Gödel, Russell, Yablo)
Onboard new formal systems via JSON carriers (see carriers/_schema.json)
Verify every claim computationally — machine-precision calculus, falsifiable boundaries

Repository Layout

carriers/ — JSON definitions for every formal system (classical, paraconsistent, linear, calculus, probability, modal, etc.)
core/ — Core propagation engine, carrier_tool.py, and unified validation
docs/ — The two canonical PDFs above
demos/ — Worked examples (paradoxes, calculus demos, etc.)
pl/ — Legacy rich implementation from v12 (preserved for historical depth)
tests/ — Automated falsification suite
explorations/ — Experimental extensions

Philosophy (in one sentence)
Code over philosophy. Mechanisms over tautologies. Parsimony over orthodoxy.
The foundational error of Western formal systems was the zero-cost distinction fallacy — treating the output of an energetically expensive boundary-maintenance process (identity, truth, constants) as a free primitive. Every paradox is the bill arriving. Propagation Logic pays the debt at the propagation layer itself.
Status & Roadmap

✅ Single unified mechanism proven across logic + calculus + DRAS
✅ Carrier tool + JSON schema + falsifiability standard
✅ 69 automated assertions passing
🔄 Full runtime simulation engine (in progress)
🔄 Interactive CarrierExplorer web UI
🔄 Community carrier registry + new formal systems

We are building the Mathesis Universalis that actually runs.

How to Contribute
See CONTRIBUTING.md — every new carrier must include:

At least one mathematically forced law with proof
At least one explicit failure mode
A pytest falsification test

New carriers are welcome. The framework is deliberately designed for rapid, falsifiable extension.

Every major claim in this repository is demonstrated in running code.
Run python core/pl_unified.py and see for yourself.

Built with the explicit goal of being more falsifiable than what it replaces.
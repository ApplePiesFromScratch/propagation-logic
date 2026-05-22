markdown
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
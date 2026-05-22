# Propagation Logic

**P / G → Q**

Every formal system is completely specified by three parameters:

| Parameter | Meaning | Examples |
|-----------|---------|---------|
| **V** | Value carrier — what values can a statement take? | `{0,1}`, `{0,B,1}`, `[0,1]`, `ℝ`, `ℕ`, `ℂ` |
| **Γ** | Gradient family — what operations are available? | `full_bool`, `constructive`, `linear`, `differential` |
| **θ** | Coherence threshold — when is a pattern stable? | `1.0` (boolean), `0.0` (infinitesimal) |

Change V, Γ, or θ. Watch the forced laws change. The mechanism stays constant.

```
Classical logic:     V={0,1},   Γ=full,          θ=1.0
Intuitionistic:      V={0,1},   Γ=constructive,  θ=1.0
Paraconsistent (LP): V={0,B,1}, Γ=full,          θ=1.0
Calculus:            V=ℝ,       Γ=differential,  θ=0.0
```

## Quick Start

```bash
git clone https://github.com/ApplePiesFromScratch/propagation-logic
cd propagation-logic
python core/pl_unified.py          # 12 sections, 69 assertions
python core/carrier_tool.py --learn  # interactive guide
python core/carrier_tool.py --diff classical intuitionistic
```

## Three Paths

**Student** → `docs/curriculum/` → `docs/papers/` → `core/pl_unified.py`

**Researcher** → `docs/papers/` → `carriers/_schema.json` → `CONTRIBUTING.md`

**Builder** → `core/pl_unified.py` → `examples/` → `core/carrier_tool.py` API

## What This Is Not

Not a claim that all formal systems are identical — they force genuinely
different behaviours. The point: those differences are consequences of
parameter choices, not mysterious independent metaphysical commitments.
An axiom is a static boundary condition of a specific propagation regime.

## Repository Structure

```
core/           The mechanism — stable, tested, 69 assertions
carriers/       Community carrier definitions (JSON)
docs/papers/    Foundational papers (PDF)
docs/curriculum/ Teaching materials
examples/       Worked examples
tests/          pytest suite
frontend/       CarrierExplorer.jsx (interactive parameter space)
```

## Papers

- [PL DRAS Calculus Unified](docs/papers/PL_DRAS_Calculus_Unified.pdf) — core framework
- [Identity as Artifact](docs/papers/identity_as_artifact.pdf) — thermodynamic grounding
- [The Zero-Cost Distinction Fallacy](docs/papers/zero_cost_fallacy.pdf) — foundational argument

## Citation

```bibtex
@software{pugmire2026pl,
  author  = {Pugmire, James Alexander},
  title   = {Propagation Logic},
  year    = {2026},
  url     = {https://github.com/ApplePiesFromScratch/propagation-logic},
  version = {2.0}
}
```

---
*The carrier sets the logic. The mechanism sets the rest.*

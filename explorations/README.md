# explorations/

Experimental extensions of the Propagation Logic framework.

Files here are **not guaranteed to run** without additional setup — several
import from a `pl/` package that is not yet part of the core distribution.
They are preserved because they contain genuine theoretical work that will
be migrated to `demos/` or `core/` as the repository matures.

### Contents

| File | Description | Status |
|---|---|---|
| `pl_fol3d.py` | Multi-protein folding via PL gradients | Needs `pl.calculus` |
| `higher_structures_demo.py` | Differential geometry, category theory, type theory as PL instances | Needs `pl.core`, `pl.calculus` |
| `mathesis_demo.py` | Dual numbers, flux, constructive number systems | Needs `pl.*` package |
| `dras_demo.py` | DRAS arithmetic with running coupling constants | Needs `pl.dras` |
| `grammar_as_propagation.py` | English grammar as a propagation carrier | Needs `pl.*` package |
| `mathesis_explorer.jsx` | React-based interactive carrier explorer | Standalone (browser) |
| `pl_game_theory.jsx` | Game theory visualisation (React) | Standalone (browser) |
| `logic_demos.py` | Extended logic demonstrations | Needs `pl.*` package |
| `all_mathematics_demo.py` | Broad mathematical survey | Needs `pl.*` package |
| `finite_demo.py` | Finite arithmetic as propagation structure | Needs `pl.*` package |

### The `pl/` package

Several files here import from `pl.core`, `pl.calculus`, `pl.dual`, `pl.flux`,
`pl.dras`, `pl.drag`, and `pl.numbers`. This package existed in an earlier
version of the repository. All of its functionality is now implemented inline
in `core/pl_unified.py` (§0–§12).

The migration path — extracting `pl_unified.py` into a proper importable
package — is tracked as an open issue.

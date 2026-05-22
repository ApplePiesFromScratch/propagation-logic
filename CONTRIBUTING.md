# Contributing to Propagation Logic

## Adding a New Carrier

Every carrier definition lives in `carriers/` as a JSON file following
the schema in `carriers/_schema.json`.

### Required Fields

1. **parameters**: V, Γ (Gamma), θ (theta) — all three required
2. **forced_laws**: at least one law with a derivation proof
3. **explicit_failures**: at least one boundary condition that fails
4. **falsification_test**: a pytest path that would fail if the definition is wrong

### Submission Process

1. Copy `carriers/_template.json` to `carriers/your_logic.json`
2. Fill all required fields
3. Write `tests/test_carriers.py::test_your_logic`
4. Run `python core/carrier_tool.py --validate carriers/your_logic.json`
5. Run `pytest tests/test_carriers.py` — all must pass
6. Open a PR with title `[Carrier] Your Logic Name`

### Falsifiability Standard

The schema requires explicit_failures because a carrier definition that
claims to force everything is almost certainly importing external axioms
it has not acknowledged. Every logic has boundaries. State them.

## Improving Core Code

- `core/pl_unified.py` is the primary reference implementation
- All changes must keep the 69 existing assertions passing
- New sections should add assertions, not just demonstrations
- Run `pytest tests/` before any PR

## Style

- Code: PEP 8, type hints where they clarify
- Comments: explain the mechanism, not just the operation
- Docstrings: state what the code proves, not just what it does

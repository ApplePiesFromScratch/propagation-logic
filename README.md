# Propagation Logic v0.3

`P / G → Q`

One operator. Three knobs. Presentations, not terrain.

This is a **rebuild** of [ApplePiesFromScratch/propagation-logic](https://github.com/ApplePiesFromScratch/propagation-logic).
The old tree treated the operator as a mathesis that *was* logic and calculus.
This tree keeps the operator and drops that claim.

```
V   alphabet
G   declared maps / isolation
θ   admission, refusal, budget
```

A name introduces structure. It does not uncover essence.
Nouns compress. The noun does not get to run.

## Quick start

```bash
python PROCESS.py          # kernel + ledger + μ + map   (one file)
python -m pl               # demo
python -m pl cert          # JSON certificate
python -m pl migrate       # v0.3 reconfig ledger
python -m pytest -q
```

```python
from pl import isolate, rate, certify, Runtime, V2, V3

x = isolate(3)
rate(x * x, x)                         # 6
c = certify(lambda z: z ** 3 + 2 * z, at=3)
# 29, FORCED-on-cut, falsifier attached

rt = Runtime(V2, 1)
rt.reconfigure(V3, "admit midpoint")   # pays RECONFIG + GUARD + μ
```

## What changed from the old repo

| old | v0.3 |
|---|---|
| `Γ` / Gamma | `G` |
| “structural identity with nature” | map; non-claims listed |
| laws authored `forced: true` | tier computed on a declared cut |
| isolate / guards implicit free | isolate unpriced; guards and μ on the ledger |
| V grows by adding `∞` or a point | leave-V → θ or registered μ |
| paradoxes as thermodynamic debt | load is stipulated, not derived |
| Mathesis that runs | replica, receipt, ledger line |

Details: `docs/CHANGELOG_FROM_V1.md`. Guardrails: `docs/GUARDRAILS.md`.

## Layout

```
PROCESS.py          standalone resume file
pl/                 kernel: reading, certify, migrate, prescreen
carriers/           JSON presentations (CL2, L3, K3, PROC)
docs/               guardrails, v0.3 spec, operator guide
insights.json       mapped receipts
tests/
```

Carrier JSON must name `V`, `G`, `theta`, `forced_on_cut`, `fails`, `falsifier`.
Schema: `carriers/_schema.json`. `Gamma` is retired.

## Guardrails (admission)

1. No `V,G,θ` in the sentence → not a claim.
2. Two presentations agree → grow `V` before one G.
3. Step leaves `V` → θ or registered μ.
4. Label changes no knob → comment.
5. Work happened → ledger line.

## Status

Runnable kernel. Certificates. Migration maps. Unified ledger.
Not a replacement for JAX, PhysX, or vanilla Doom.
Not how variation or the sky *are*.

## License

MIT (same terms as the upstream repo).

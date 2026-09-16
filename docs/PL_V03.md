# PL Process v0.3 — migration and unified ledger

Off-book work is a leak. v0.3 closes two slots that sat at cost 0.

This is a spec of a runtime cut. It is not a thermodynamics of nature.

---

## 1. Carrier migration

```
V_A  --[guard Θ, cost θ_guard]-->  allowed?
     --[map μ,    cost θ_μ    ]-->  x' ∈ V_B
     --[reconfig, cost θ_reconfig] billed on the same ledger
```

- No registered `μ: V_A → V_B` → `Theta` (teleport refused).
- `μ(x) ∉ V_B` → `Theta`.
- Live channel in `V_A` and `V_B` has no channel slot →
  `ChannelPreservationError` (guard fires **before** `μ`).
- Identity maps exist only for the same carrier name. `F → F` labelled
  “V3→Q” is a comment, not a map.

Declared maps in `cutad/migrate.py`:

| μ | load | refused |
|---|---|---|
| V2 → V3 | embed | — |
| V3 → QPAIR | open dead `r=0` | — |
| QPAIR → QJET2 | allocate `r2` | — |
| QPAIR → V3 | drop dead `r` | live `r` |

---

## 2. Unified ledger

```
Θ_total = θ_step + θ_guard + θ_reconfig + θ_μ  [+ θ_reify]
```

If `Θ_total > θ_max` → `Decohered`. The grow does not complete for free.

Stipulated prices (G of the budget carrier, not derived):

```
STEP 1    GUARD 1/4    RECONFIG 2    MIGRATE (per μ)    REIFY 1
```

A guard that **passes** still pays. Evaluating Θ is work.

---

## 3. What Gemini’s draft added, and what it missed

Added: first-class Guard / Map language; live-channel error name;
ledger unification sentence.

Missed: `source_v=F, target_v=F` is not a carrier change. Charging μ
before the live-channel check lets a doomed drop pay the map. v0.3
charges RECONFIG + GUARD, then refuses, and does not run μ.

---

## 4. Run

```
PYTHONPATH=. python3 -m pl.migrate
PYTHONPATH=. python3 -m pytest tests/test_migrate.py -q
```

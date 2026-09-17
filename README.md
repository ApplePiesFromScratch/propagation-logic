# carriersets

**85 formal systems cataloged as `P/G→Q` carriers — and the catalog
runs its own receipts: 92 executable checks decide 113 of its 218
claims live, and the library prints what fraction of itself is still
bibliography.**

Every formal system ever built is a specific choice of three
parameters: a value space **V**, a gradient family **G**, and a
coherence threshold **θ**. The propagation operator `P/G→Q` is constant
across all of them. This repo is the reference library of those
choices — nine sections, from classical logic to the Boundary Law —
where every "Forces" and "Breaks" claim either names a check that runs
on every build, or wears an honest tag (`PRESUMED` + citation,
`STIPULATED`, `OPEN`) and is priced at zero.

```
$ python library_verify.py

  == Propositional Logic  [14 carriers, paid 28/40 claims = 70%] ====
  [  ok]  1 Classical Logic          paid 3/4  FORC:3 PRES:1
  [  ok]  3 Kleene Strong (K3)       paid 3/3  FORC:3
  ...
  LIBRARY PAID FRACTION: 113/218 claims machine-decided here = 51.8%
  verdict PASS/STIPULATED   chain 86 sealed, replay=intact   1.3s
```

## The numbers (measured, not estimated)

| | |
|---|---|
| Carriers | **85** across 9 sections |
| Claims in the Forces/Breaks tables | **218** |
| Decided by executable check | **113 (51.8%)** — 99 FORCED, 7 EMPIRICAL, 7 CONDITIONAL |
| Honestly inherited | 102 PRESUMED (each with its citation), 2 STIPULATED, 1 OPEN (P vs NP — the only claim allowed that tier) |
| Executable checks | **92**, full suite ~2.2 s |
| Manifest | 86 hash-chained seals, byte-replayable |

What "decided" means here: all 15 classical laws enumerated over finite
V; every modal axiom decided over **all 585 Kripke frames up to three
worlds** (K holds everywhere; T bought exactly by reflexivity; Löb by
finite strict orders — and T *fails* there, incompleteness in
miniature); Cantor-normal-form ordinal arithmetic implemented so
`1+ω=ω≠ω+1` is a computation; the Galois correspondence for
`Q(√2,√3)` enumerated group-side and field-side; `d²=0` and the Jacobi
identity symbolic and exact; Itô's `(dW)²=dt` measured over 1500 paths
with 4-σ bounds; Zadeh's paradox computed to its absurd 100%; dilation
constructed; the busy beaver run to its halt; SOR pushed over
Ostrowski's ω=2 wall and watched decohere.

## Two places the enumerator corrected the source

The house rule is that when the table and the prose disagree, the table
wins. Building this library, it happened twice — to our own PDFs:

1. **K3's LNC has two readings, and the source used both silently.**
   Under the designation reading (kernel-compatible), LNC *holds* and
   K3's signature is 14/15 with LEM the lone sacrifice. Under the value
   reading, `AND(½,¬½)=½≠0` and LNC fails. `k3_signature` decides both
   and the record now says which is which.
2. **The Gödel→classical thresholding map is not a morphism.** The
   mapping guide claimed `v↦[v=1]` commutes with the gradients. It
   commutes with `{AND, OR}` and *fails for Gödel negation* (witness
   `½`: `f(¬½)=0` but `¬f(½)=1`). `morphism_godel_threshold_corrected`
   exhibits the witness; the claim is now scoped to its honest fragment.

## Layout

```
library_verify.py       the entry point the source PDF names — tables,
                        paid fractions, sealed manifest, exit 1 on any
                        check failure
CATALOG.md              the whole library as markdown, generated, with
                        live verification badges per claim
carriers/               the data: 85 records in 9 section modules
carrierlib/core.py      tiers, check registry, hash-chain seal/replay
carrierlib/finite.py    15-law enumerator (kernel-shared vocabulary),
                        morphism decider, exhaustive Kripke frames,
                        finite-trace LTL
carrierlib/checks/      92 checks in 9 themed modules
tools/render_catalog.py regenerates CATALOG.md from the data
tests/run.py            the gate
docs/MAPPING_GUIDE.md   the six steps, as the admission gate
docs/reference/         the two source PDFs
```

## The tier ladder

`FORCED` (complete enumeration or exact symbolic computation, here) >
`EMPIRICAL` (measured here, tolerances from measured spread, fixed
seeds) > `CONDITIONAL` (bounded instance, bound stated) > `STIPULATED`
(a convention the record declares, e.g. finite-trace LTL semantics) >
`PRESUMED` (inherited with citation — *not doubted, just not re-derived
here*) > `OPEN` (P vs NP, and nothing else).

The **paid fraction** — FORCED+EMPIRICAL+CONDITIONAL over all claims —
is the library's headline number and is computed at verify time, per
carrier, per section, and overall. Proof Theory sits at 0/4 paid and
Reverse Mathematics at 0/2, *on purpose*: cut elimination's blowup and
reversal meta-proofs are exactly the things no bounded demo does
justice, and pretending otherwise would be dressing claims above their
evidence.

## Relation to the other MathofLogic repos

- **[/PL](../PL)** — the kernel. `carrierlib.finite.laws` speaks the
  same 15-law vocabulary, so signatures computed here are comparable
  with `pl.py`'s (which is how the K3 finding surfaced).
- **[/rigor](../rigor)** — the audit toolbox whose claim-tier
  discipline this library applies to mathematics itself.
- **[/PL-lessons](../PL-lessons)** — the course; this is its reference
  shelf.
- **[/PL-Verify](../PL-Verify)** — the same honesty pointed at model
  outputs instead of theorems.

## Run it

```bash
pip install sympy numpy
python library_verify.py               # the whole library
python library_verify.py --carrier GL  # one carrier, verbose evidence
python tests/run.py                    # the gate
python tools/render_catalog.py         # regenerate CATALOG.md
```

## Non-claims

Printed with every verdict, kept here too: PRESUMED entries are not
doubted, only unpaid-for locally. The insight prose is commentary — the
checks decide the tables. And 85 carriers is a library, not the space
of all formal systems: the mapping guide is the door, and it is open.

MIT license. Trust infrastructure should not be paywalled.

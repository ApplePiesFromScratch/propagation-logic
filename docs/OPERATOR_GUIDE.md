# Operator distinction and testing guide

For any system specified as `(V, G, θ)`.

A name does not distinguish operators. A closed check on a declared
alphabet does. This file is the protocol. It does not report essences.

Copy it. Adapt the tables. Keep the falsifier rule.

---

## 1. The three knobs (only these)

| knob | question | refusal |
|---|---|---|
| **V** | What values may appear? | `LeavesV` — input not in the alphabet |
| **G** | What maps are allowed on V? | an op that returns outside V is not in G |
| **θ** | What is accepted, and what happens otherwise? | refuse, decohere, or quarantine — do not add `∞` |

`P / G → Q` is constant. Only the knobs change.

If two systems share a name (`AND`, `derivative`, `integral`, `update`)
and differ in any knob, they are different operators. Write two rows.

---

## 2. Distinguishing operators

### 2.1 Same word, list the structure

For each named op write:

```
name:
  V:        alphabet (finite list, or "Q", or "claimed unlistable")
  signature: arity and types
  rule:     the map, in one line
  θ:        when it refuses
  closes:   every output in V? (yes / no / unpaid)
  coincides_with: other names that agree on this V
  splits_when: the smallest V-growth that separates them
```

Example — three things all called AND:

```
AND-min       V={0,½,1}  min(a,b)           closes    ½∧½=½
AND-prod      V={0,½,1}  a·b                LEAVES V  ½∧½=¼
AND-luk       V={0,½,1}  max(0,a+b−1)       closes    ½∧½=0
```

On `V={0,1}` all three agree. That agreement is not portable.
Distinction is the growth of V, not a debate about the word AND.

### 2.2 Same mix, different isolation

If the combination rule is shared and only the comparison changes,
that is two *presentations*, not two algebras.

```
mix        (v,r)*(w,s) = (vw, rw+vs)     shared
STD-dual   isolate seed=1, then collapse r to a value
PROC-rate  rate(P, G) = P.r/G.r          G is an argument
```

Distinction test: rescale the seed. If the published number moves in
one presentation and not the other, they are not the same op.

### 2.3 Reconstruction vs primitive

Some ops exist only to rebuild a slot another presentation discarded.

| reconstruction | discarded slot |
|---|---|
| finite difference `h` | carried channel `r` |
| Riemann `n→∞` | telescope of carried pairs |
| L’Hôpital loop | `rate` of uncollapsed `0/0` |
| epicycle | warp of the angle channel |
| `∞` as a point | θ |

If you still hold the slot, the reconstruction is not in G. If you
threw the slot away, the reconstruction is a different carrier.

### 2.4 A name that changes no knob is a comment

`Tycho` printed on the same two circles as `Ptolemy-G1` is not a new
operator. The error table will match. Do not give it a new row.

---

## 3. Testing protocol

Every operator gets two tests. No exceptions.

1. **Close-test** — on a declared finite cut, every legal input lands
   in V, and the stated identity holds.
2. **θ-test** — the illegal input refuses. It does not return a
   value in V and does not invent an extra inhabitant.

A claim that cannot name a falsifier is not a claim.

### 3.1 Finite V — enumerate

```
for every a, b in V:
    if input is legal under θ:
        r = op(a, b)
        assert r in V
        assert identity(a, b, r)
    else:
        assert refuses(op, a, b)
```

Tier: `FORCED-on-cut` if discharged == |cut|. Scope is the cut, stated
in the claim.

### 3.2 Countable / claimed-infinite V — grid + unpaid lift

Pick a listed grid. Run the same loop. Tier is `FORCED-on-cut` of that
grid. The sentence “therefore for all ℝ” is `UNPAID`.

Do not emit a float and call V larger.

### 3.3 Gauge / presentation test

If isolation has a scale `k`:

```
assert op(rescale(P,k), rescale(G,k)) == op(P, G)
```

for every listed `k ≠ 0`. Failure means the op is reading a raw
channel as a fact.

### 3.4 Coincidence test (the distinction engine)

```
on V_small:  op_A == op_B     # recorded, not surprising
on V_grown:  op_A != op_B     # this is the distinction
```

If you cannot exhibit a grown V where they split, you do not yet have
two operators. You have one op and two comments.

### 3.5 Reconstruction test

If a candidate op is suspected to fake a slot:

```
hold the slot, compute primitive
discard the slot, run reconstruction
compare on the same cut
```

Finite difference vs `rate` on `x²`: primitive `6`, reconstruction
`6+h`. They never meet on listed `h`. That is the distinction.

### 3.6 Pre-screen a theorem before proving it

A statement can name values the carrier cannot hold. Screening first
saves the proof attempt.

```
python -m pl.prescreen
```

Pipeline, in order:

1. Named constants ∈ V?          else REFUSE
2. Named ops ∈ G?                else REFUSE
3. Named point θ-legal for those ops?  else REFUSE  (1/x at 0)
4. Quantifier fit the alphabet?  else DEFER         (MVT on ℝ)
5. Ops close on V?               else REFUSE        (product AND on V3)
6. Optional probe of the conclusion on listed V.
   Fail → REFUSE (LEM on K3). Hold → ADMIT.

ADMIT means “well-typed here; run the close-test.” It is not a proof.
DEFER means “typed, but the ∀ outruns listed V.”
REFUSE means the carrier that asked for the theorem cannot hold it.

Example receipts from the harness:

```
LEM on CL2              ADMIT
LEM on K3               REFUSE   OR(½,¬½) not designated
AND-idempotent on L3    REFUSE   ½∧½=0 ≠ ½
1/x at 0 on PROC        REFUSE   θ quot(..., 0): pole
mean value on ℝ / PROC  DEFER    quantifier unlistable
AND=product on V3       REFUSE   ½·½=¼ leaves V
```

`0` can sit in V and still be unstable for an op. Membership in V is
not enough. Step 3 is the stability check the question asked for.

---

## 4. Claim shape

```
statement:   one sentence, knobs visible
held:        bool
discharged:  how many cases ran
scope:       how many cases the sentence ranges over (or None)
declared:    is the scope part of the statement?
falsifier:   what a critic would exhibit
tier:        computed, not authored
```

```
tier:
  scope missing        → UNPAID  (or CONDITIONAL if marked derived)
  discharged == scope  → FORCED-on-cut if declared else FORCED
  0 < ratio < 1        → EMPIRICAL
  held is false        → UNPAID
```

Do not write `FORCED` by hand.

---

## 5. Worked distinctions

### 5.1 AND

| cut | min | product | luk |
|---|---|---|---|
| `{0,1}` | agree | agree | agree |
| `{0,½,1}` | `½` | `¼ ∉ V` | `0` |

Tests: enumerate both alphabets. Product’s close-test fails on V3.
That is sufficient distinction.

### 5.2 Derivative

| cut | unary D (seed 1) | rate(P,G) | fd h |
|---|---|---|---|
| `x²` at 3, seed 1 | 6, channel gone | 6, channel kept | 6+h |
| same, seed 2 | cannot state | 6 | 6+h |
| `0/0` values | collapsed 0 | channel ratio | undefined |

Tests: gauge sweep; `r` after D is 0; fd never equals 6 on listed h;
`rate((0,6),(0,1))=6` and `quot` refuses.

### 5.3 Integral

| cut | accumulate listed pairs | Riemann n panels |
|---|---|---|
| path readings already carried | 1 telescope = net | not the same input |
| only `f` samples | not an op of that V | n evals, error ~1/n |

Do not score them as the same job. Different inputs, different G.

### 5.4 Isolation in the sky

| cut | unary against Earth | rate(Mars, Sun) |
|---|---|---|
| two geo vectors already paid | leftover in radius | leftover becomes one circle |
| extra epicycle on Earth-seed | error can get worse | — |
| `e` on `rate(M,S)` | — | error drops |

Tests: same input vectors, two G’s, compare `(lon_max, rad_max)`
against a declared sky sample. Rename without changing G must match
exactly (G1 vs Tycho-circles).

---

## 6. Adding an operator to a system

1. Name the slot it corrects. If you cannot, stop.
2. Write V, rule, θ.
3. Close-test on a declared cut.
4. θ-test on the illegal input.
5. Coincidence-test against every same-word op already in the system,
   on a V large enough to split.
6. If it leaves V, do not add an inhabitant. Tighten θ or enlarge V
   *explicitly* and restart at 2.
7. Record the presentation (isolation, connectives) in the scope.
   A bare name is not a row.

---

## 7. What not to do

- Treat agreement on `{0,1}` as a law of thought.
- Collapse an interval to a decimal and keep the same V label.
- Put `∞` in V to avoid writing θ.
- Author a tier.
- File a claim without a falsifier.
- Call a rename a new operator.
- Lift `FORCED-on-cut` to an unlistable alphabet in the same sentence.

---

## 8. Minimal harness

`docs/operator_test.py` in this repo runs the AND split, the rate/D/fd
split, and the θ refusals. Use it as the template. Replace the
example ops with the system under test. Keep the two-test rule.

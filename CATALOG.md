# Carrier Library — Catalog

*Rendered from `carriers/` by `tools/render_catalog.py`. Every **FORCED/EMPIRICAL/CONDITIONAL** badge below was earned by an executable check at render time; every *PRESUMED/OPEN/STIPULATED* line says so and cites. `P/G→Q` is constant; only V, G, θ vary.*

**85 carriers · 218 claims · 113 machine-decided (51.8% paid fraction)**

## Propositional Logic — 14 carriers

### 01 · Classical Logic (`CL2`)
*Aristotle (384 BC); Frege (1879); Whitehead & Russell (1910)*

| | |
|---|---|
| **V** | {0,1} — exactly two truth values |
| **G** | NOT v=1-v; AND=product/min; OR=max; IMP(a,b)=max(1-a,b) |
| **θ** | 1.0 — only full truth designated |

Demanding an involutive NOT with no fixed point forces V={0,1} uniquely; LNC and LEM then follow by arithmetic — consequences of the carrier, not axioms. Complete commitment on every proposition, no gradations without information loss.

**Forces**
- **FORCED** `cl2_signature` — All 15 classical laws hold, by complete enumeration
  - *15/15 laws by enumeration over {0,1}: 15/15*
- **FORCED** `cl2_ex_falso` — Ex falso: AND(v,NOT v)=0, so OR(0,Q)=Q for any Q
  - *AND(v,NOT v)=0 so OR(0,Q)=Q — all 4 cases*

**Breaks on**
- **FORCED** `cl2_no_fixed_point` — No fixed point for NOT — the Liar is unrepresentable
  - *no v in {0,1} with NOT(v)=v — enumerated; the Liar has no home*
- *PRESUMED* — No gradations: v=0.5 cannot be represented  (by definition of V; see fuzzy carriers for the repair)

**Useful for:** classical mathematics · digital circuits · SAT solvers · SQL boolean logic

### 02 · Lukasiewicz Three-Valued Logic (L3) (`L3`)
*Jan Lukasiewicz (1920), O logice trojwartosciowej*

| | |
|---|---|
| **V** | {0, 1/2, 1} — false, indeterminate, true |
| **G** | NOT v=1-v; AND(a,b)=max(0,a+b-1); OR=min(1,a+b); IMP=min(1,1-a+b) |
| **θ** | 1.0 — only 1 designated |

The midpoint is negation's first fixed point — the Liar settles at 1/2 instead of oscillating. The strong t-norm makes truth expensive: a+b must EXCEED 1 before AND pays anything, so LNC and LEM survive the third value.

**Forces**
- **FORCED** `l3_signature` — LNC and LEM both hold at every value; DN holds
  - *LNC+LEM+DN hold on all 3 values; the bill: idempotence fails (AND(1/2,1/2)=0)*
- **FORCED** `l3_fixed_point` — NOT(1/2)=1/2 — the Liar's stable home
  - *NOT(1/2)=1/2 — negation's first fixed point; the Liar settles*

**Breaks on**
- **FORCED** `l3_two_halves` — AND(1/2,1/2)=0 — two half-truths produce no truth
  - *AND(1/2,1/2)=max(0,0)=0 — two half-truths produce no truth*
- *PRESUMED* — LEM fails if 1/2 is also designated  (immediate from OR(1/2,1/2)=1: designation choice, see LP)

**Useful for:** truth-gap logics · self-reference analysis · three-valued NULL semantics (partial)

### 03 · Kleene Strong Three-Valued Logic (K3) (`K3`)
*Stephen Kleene (1952), Introduction to Metamathematics*

| | |
|---|---|
| **V** | {0, 1/2, 1} — false, undefined, true |
| **G** | NOT v=1-v; AND=min; OR=max; IMP(a,b)=max(1-a,b) |
| **θ** | 1.0 — only 1 designated |

Same values as L3, lattice operators instead: 1/2 becomes a propagating taint — a computation that has not returned, contaminating everything it touches. Both source documents are honored: LNC holds under the designation reading (kernel parity, 14/15 lone-LEM signature) and fails under the value reading AND(1/2,NOT 1/2)=1/2 != 0 — the enumerator decides both, and the discrepancy is surfaced, not hidden.

**Forces**
- **FORCED** `k3_signature` — All lattice laws; DN; 14/15 signature with LEM the lone sacrifice (designation reading), value-reading LNC failure also exhibited
  - *both readings decided: under the designation reading LNC holds and the signature is 14/15 with LEM the lone sacrifice (kernel parity); under the value reading AND(1/2,NOT 1/2)=1/2 != 0, the library PD*
- **FORCED** `k3_taint` — 1/2 taints every AND below truth and every OR above falsehood
  - *min(1/2,x)<=1/2<=max(1/2,x) for all x — the undefined propagates*

**Breaks on**
- **FORCED** `k3_signature` — LEM fails: OR(1/2,NOT 1/2)=1/2, not designated
  - *both readings decided: under the designation reading LNC holds and the signature is 14/15 with LEM the lone sacrifice (kernel parity); under the value reading AND(1/2,NOT 1/2)=1/2 != 0, the library PD*

**Useful for:** partial function semantics · SQL NULL (strong reading) · partial evaluation

### 04 · Kleene Weak Three-Valued Logic (`WK3`)
*Stephen Kleene (1952), weak tables variant*

| | |
|---|---|
| **V** | {0, u, 1} — u = undefined, absorbing |
| **G** | NOT(u)=u; AND(u,x)=u and OR(u,x)=u unconditionally; classical on {0,1} |
| **θ** | 1.0 — u blocks all inference through it |

Weak K3 bans short-circuiting: a known 0 cannot rescue an AND, a known 1 cannot rescue an OR. Every subexpression must resolve — strict call-by-value, encoded in the tables.

**Forces**
- **FORCED** `wk3_absorbs` — u absorbs both operations regardless of the other argument; classical on {0,1}
  - *u absorbs both ops unconditionally (strong K3 would rescue: min(u,0)=0, max(u,1)=1 — contrast enumerated)*

**Breaks on**
- **FORCED** `wk3_absorbs` — AND(u,0)=u where strong K3 gives 0; OR(u,1)=u where strong gives 1 — the rescue is forbidden
  - *u absorbs both ops unconditionally (strong K3 would rescue: min(u,0)=0, max(u,1)=1 — contrast enumerated)*
- *PRESUMED* — LNC and LEM both fail at u  (direct from absorption)

**Useful for:** strict evaluation semantics · call-by-value models · error propagation

### 05 · Bochvar External Three-Valued Logic (B3) (`B3`)
*Dmitri Bochvar (1938)*

| | |
|---|---|
| **V** | {0, m, 1} — m = meaningless/paradoxical |
| **G** | internal: m absorbs; external assertion E(1)=1, E(0)=E(m)=0 |
| **θ** | 1.0 externally; m quarantined internally |

Two tiers: internally m infects every formula it touches (paradox contained, not resolved); the external operator then collapses m to 0, restoring classical decidability for sound formulas. Quarantine plus discharge.

**Forces**
- **FORCED** `b3_external_collapse` — m absorbs internally; E collapses m to 0 and preserves classical values
  - *m absorbs internally; E collapses m->0 — classical decidability restored outside the quarantine*

**Breaks on**
- *PRESUMED* — no internal LNC/LEM for m-valued formulas  (direct from absorption tables)

**Useful for:** paradox containment · partial information · undefined-value semantics

### 06 · Paraconsistent Logic LP (Priest) (`LP`)
*Graham Priest (1979), The Logic of Paradox*

| | |
|---|---|
| **V** | {0, B, 1}; B = both, arithmetically 1/2 |
| **G** | NOT v=1-v; AND=min; OR=max; DESIGNATED = {B, 1} |
| **θ** | designation includes the glut |

K3's tables with the middle value designated: contradictions become usable premises. Explosion is blocked by arithmetic — min cannot amplify B above B, so a glut never forces an arbitrary Q. The price is detachment: modus ponens fails.

**Forces**
- **FORCED** `lp_signature` — LEM holds; LNC fails; MP fails — the paraconsistent trade, enumerated
  - *glut designated: LNC fails, LEM holds; the price is detachment (MP fails)*
- **FORCED** `lp_no_explosion` — ex falso blocked: countermodel with designated glut and undesignated Q
  - *countermodel: glut=1/2 designated yet q=0 stays undesignated — min cannot amplify B above B*

**Breaks on**
- **FORCED** `lp_signature` — LNC: AND(B,NOT B)=B, designated
  - *glut designated: LNC fails, LEM holds; the price is detachment (MP fails)*

**Useful for:** dialethism · inconsistent databases · naive set theory without explosion

### 07 · Fuzzy Logic (Zadeh / product t-norm) (`FUZZY_PROD`)
*Lotfi Zadeh (1965), Fuzzy Sets*

| | |
|---|---|
| **V** | [0,1] continuous |
| **G** | NOT v=1-v; AND=a*b; OR=max; Goguen IMP |
| **θ** | 1.0 |

Continuum truth with multiplicative AND: conjunction always weakens in the interior (half times half is a quarter). LNC and LEM both leak at 0.5 — partial truth conjoined with partial falsehood is not nothing.

**Forces**
- **FORCED** `fuzzy_product_failures` — a*b <= min(a,b) (AND weakens); IMP(a,a)=1
  - *witnesses at v=0.5: LNC gives 0.25 not 0, LEM gives 0.5 not 1; a*b<=min on grid*

**Breaks on**
- **FORCED** `fuzzy_product_failures` — LNC gives 0.25 at v=0.5; LEM gives 0.5 — witnesses exhibited
  - *witnesses at v=0.5: LNC gives 0.25 not 0, LEM gives 0.5 not 1; a*b<=min on grid*
- *PRESUMED* — IMP(0,b) needs a convention  (Goguen residuum)

**Useful for:** fuzzy control · approximate reasoning · soft constraints

### 08 · Fuzzy Logic (Lukasiewicz / MV) (`FUZZY_LUK`)
*Lukasiewicz (1930); Chang (1958) MV-algebras*

| | |
|---|---|
| **V** | [0,1] — metric completion of the finite L_n chain |
| **G** | NOT v=1-v; AND=max(0,a+b-1); OR=min(1,a+b); IMP=min(1,1-a+b) |
| **θ** | 1.0 |

The unique continuous t-norm that keeps BOTH LNC and LEM on the whole interval: v+(1-v)-1=0 and v+(1-v)=1 identically. Classical law-keeping extended to a continuum, at the price of idempotence.

**Forces**
- **FORCED** `fuzzy_luk_both_laws` — LNC and LEM hold at every point of [0,1], exactly
  - *exact: v+(1-v)-1=0 and v+(1-v)=1 identically — LNC and LEM hold everywhere on [0,1]*

**Breaks on**
- *PRESUMED* — uniqueness among continuous t-norms  (Mostert-Shields classification; PRESUMED here)

**Useful for:** MV-algebras · fuzzy arithmetic · probability logic

### 09 · Fuzzy Logic (Godel / min t-norm) (`FUZZY_GODEL`)
*Godel (1932); Dummett (1959) LC*

| | |
|---|---|
| **V** | [0,1] linearly ordered |
| **G** | NOT(v)=1 if v=0 else 0; AND=min; OR=max; IMP crisp residuum |
| **θ** | 1.0 |

Negation is a cliff: every positive value negates to 0, so gradient information dies under NOT while AND/OR stay graded. Comparison logic — 'at least as true as' — with a binary trapdoor.

**Forces**
- *PRESUMED* — min idempotent; lattice laws throughout  (lattice identities on a chain; instance enumerated in heyting_open_sets and the 3-chain checks)

**Breaks on**
- **FORCED** `fuzzy_godel_failures` — NOT discontinuous (0.01 -> 0); DN fails; LEM fails at interior values — witnesses exhibited
  - *witnesses: NOT(NOT(0.01))=1 (DN dies with the discontinuity); LEM at 0.3 gives 0.3*

**Useful for:** intermediate logics · graded comparison · ordering semantics

### 10 · Intuitionistic Logic (BHK) (`INT`)
*Brouwer (1908); Heyting (1930); Kolmogorov (1932)*

| | |
|---|---|
| **V** | {0,1} but reachable only by explicit construction |
| **G** | OR needs a witness; IMP is a proof transformer; NOT P = P -> false |
| **θ** | 1.0 — truth is possession of a proof |

Same two values, different access rules: asserting P OR Q without a witness is not an operation. LEM is arithmetically sound but constructively unpurchasable for undecided P; refutation-of-refutation does not construct.

**Forces**
- **FORCED** `intuitionistic_countermodels` — LNC and DN-introduction hold; countermodel machinery confirms what survives
  - *3-chain Heyting countermodel: LEM fails at 1/2; ~~a->a fails; a->~~a and LNC hold — matching BHK expectations*

**Breaks on**
- **FORCED** `intuitionistic_countermodels` — LEM and DN-elimination fail: 3-chain Heyting countermodel, witness 1/2
  - *3-chain Heyting countermodel: LEM fails at 1/2; ~~a->a fails; a->~~a and LNC hold — matching BHK expectations*
- *PRESUMED* — disjunction property (a proof of P OR Q yields a proof of one)  (Godel-Gentzen; PRESUMED — proof-theoretic)

**Useful for:** constructive mathematics · Coq/Agda/Lean · Curry-Howard

### 11 · Linear Logic (`LINEAR`)
*Jean-Yves Girard (1987)*

| | |
|---|---|
| **V** | formulas as resources, used exactly once unless marked ! |
| **G** | tensor (both), additive AND (choose), -o (consume to produce), ! (unlimited) |
| **θ** | exact resource count |

Structural rules made purchasable: without !, you may neither copy a hypothesis (contraction) nor discard one (weakening). Proofs become conservation ledgers — every use has a cost and every cost is tracked.

**Forces**
- *PRESUMED* — linear MP transfers the resource; ! restores classical structure  (Girard 1987, sequent calculus; PRESUMED)
- **FORCED** `linear_no_copy_no_discard` — contraction and weakening invalid in the counting model
  - *resource counts: A|-A(x)A needs 1=2 (invalid); A,B|-A discards a purchased B (invalid) — in the counting model, which is the stipulated semantics of the !-free fragment*

**Breaks on**
- **FORCED** `linear_no_copy_no_discard` — A |- A tensor A fails (1 != 2); A,B |- A discards paid B
  - *resource counts: A|-A(x)A needs 1=2 (invalid); A,B|-A discards a purchased B (invalid) — in the counting model, which is the stipulated semantics of the !-free fragment*

**Useful for:** resource-aware type theory · Rust ownership semantics · session types

### 12 · Relevance Logic (R, E) (`RELEVANCE`)
*Ackermann (1956); Anderson & Belnap (1975)*

| | |
|---|---|
| **V** | {0,1} with a relevance filter on derivations |
| **G** | classical connectives; IMP valid only under variable sharing |
| **θ** | every premise must contribute a variable |

Material implication's paradoxes die by a syntactic tax: P -> Q must share content. Inference must use its premises, not merely coexist with them.

**Forces**
- **FORCED** `relevance_sharing_filter` — A -> A shares trivially; sharing filter is decidable and enforced
  - *variable-sharing: P->(Q->P) fails (P,Q disjoint); A->A trivially shares*

**Breaks on**
- **FORCED** `relevance_sharing_filter` — P -> (Q -> P) rejected: P and Q may share nothing
  - *variable-sharing: P->(Q->P) fails (P,Q disjoint); A->A trivially shares*
- *PRESUMED* — full R semantics (Routley-Meyer)  (Routley & Meyer 1973; PRESUMED)

**Useful for:** conditional logic · belief revision · models of explanation

### 13 · Dual-Intuitionistic Logic (co-Heyting) (`DUAL_INT`)
*Rauszer (1974); Goodman (1981)*

| | |
|---|---|
| **V** | co-Heyting algebras — closed sets where intuitionism has opens |
| **G** | subtraction A-B as the primitive; OR needs refutation evidence |
| **θ** | 0.0 — a proposition fails only on explicit refutation |

Every intuitionistic arrow reversed: refutations are the primitive certificates and default acceptance rules until a refutation lands. Where BHK asks 'can you prove it?', the dual asks 'can you refute its negation?'.

**Forces**
- **FORCED** `dual_intuitionistic_chain` — co-LEM holds on the dual chain: a OR ~a = 1 everywhere
  - *dual 3-chain: a OR ~a = 1 everywhere (co-LEM holds); a AND ~a = 1/2 at a=1/2 (co-LNC fails) — the mirror of intuitionism*

**Breaks on**
- **FORCED** `dual_intuitionistic_chain` — co-LNC fails: a AND ~a = 1/2 at the midpoint — the mirror image of intuitionism's LEM failure
  - *dual 3-chain: a OR ~a = 1 everywhere (co-LEM holds); a AND ~a = 1/2 at a=1/2 (co-LNC fails) — the mirror of intuitionism*

**Useful for:** default reasoning · paracomplete duals · over-approximation in abstract interpretation

### 14 · Substructural Logic (framework) (`SUBSTRUCT`)
*Gentzen (1935); Dosen (1988); Restall (2000)*

| | |
|---|---|
| **V** | sequents; V depends on retained structural rules |
| **G** | connectives fixed; Weakening/Contraction/Exchange/Cut are dials |
| **θ** | which structural rules survive |

Classical logic's four silent assumptions made explicit and individually removable: linear drops C, relevance drops W, Lambek drops E. Each removal is a real constraint — resources, relevance, word order — that classical proof ignores.

**Forces**
- *PRESUMED* — identity A |- A survives all removals  (Gentzen; immediate)
- **FORCED** `substructural_dials` — each dial is live: no-copy without C, order-sensitivity without E — demonstrated
  - *dropping C: counts must balance; dropping E: 'ab' != 'ba' under concatenation — each rule is a real dial*

**Breaks on**
- *PRESUMED* — cut elimination in most substructural systems  (Gentzen Hauptsatz and descendants; PRESUMED)

**Useful for:** type-theory foundations · Lambek grammars · resource-bounded computation


## Modal Logic — 8 carriers

### 15 · Modal Logic K (Kripke base) (`MODAL_K`)
*C.I. Lewis (1918); Kripke (1959-63)*

| | |
|---|---|
| **V** | worlds W with accessibility R; NECS/POSS index truth over R-neighbors |
| **G** | NECS = universal over accessible worlds; POSS = existential; R unconstrained |
| **θ** | the accessibility relation itself |

Necessity as universal quantification over R-neighbors, with R left free. Everything true here holds in EVERY modal logic; each constraint on R buys one more axiom, and the frames below pay for exactly what they claim.

**Forces**
- **FORCED** `K_axiom_all_frames` — K axiom, NEC/POS duality, NEC distributes over AND — at every world of every frame up to n=3
  - *K axiom, NEC/POS duality, and NEC-over-AND hold at every world of every frame up to n=3 (all 585 frames x all valuations)*

**Breaks on**
- **FORCED** `K_T_not_forced` — T not forced: explicit non-reflexive countermodel
  - *counterexample frame found (n=1, non-reflexive): NEC(P) without P — T is not free in K*
- *PRESUMED* — 4 and 5 not forced without transitivity/symmetry  (countermodels analogous; see S4/S5 records)

**Useful for:** temporal logic · deontic logic · provability logic · knowledge representation

### 16 · Modal Logic T (reflexive frames) (`MODAL_T`)
*Feys (1937); von Wright (1951)*

| | |
|---|---|
| **V** | Kripke frames with wRw for all w |
| **G** | K plus reflexivity |
| **θ** | self-accessibility |

One constraint, one theorem: a world that sees itself makes NECS(P) include the here-and-now, so necessity implies actuality with no further machinery.

**Forces**
- **FORCED** `T_from_reflexivity` — NECS(P) -> P forced on ALL reflexive frames; 4 still has a reflexive countermodel
  - *NEC(P)->P forced on ALL reflexive frames up to n=3; the 4-axiom still has a reflexive countermodel*

**Breaks on**
- **FORCED** `T_from_reflexivity` — 4 and B not forced
  - *NEC(P)->P forced on ALL reflexive frames up to n=3; the 4-axiom still has a reflexive countermodel*

**Useful for:** alethic modality · truthful epistemic logic · base for S4/S5

### 17 · Modal Logic S4 (preorder frames) (`MODAL_S4`)
*Lewis & Langford (1932); Kripke semantics*

| | |
|---|---|
| **V** | frames where R is reflexive and transitive |
| **G** | T plus transitivity |
| **θ** | preorder accessibility |

Transitivity makes necessity introspective: what is reachable from the reachable is already reachable, so NECS(P) is itself necessary. Knowing implies knowing that you know — but not knowing what you don't.

**Forces**
- **FORCED** `S4_from_preorder` — T and 4 forced on all preorders; 5 still fails on a preorder countermodel
  - *T and 4 forced on all preorder frames; 5 still fails on a preorder countermodel — introspection without negative introspection*

**Breaks on**
- **FORCED** `S4_from_preorder` — negative introspection absent
  - *T and 4 forced on all preorder frames; 5 still fails on a preorder countermodel — introspection without negative introspection*

**Useful for:** epistemic logic · tense logic · intuitionistic logic via Godel translation

### 18 · Modal Logic S5 (equivalence frames) (`MODAL_S5`)
*Lewis (1932)*

| | |
|---|---|
| **V** | frames where R is an equivalence relation |
| **G** | S4 plus symmetry |
| **θ** | full mutual accessibility within classes |

With R an equivalence, modality collapses to quantification over the class: possibility becomes stable (5 axiom) and all worlds in a class are modally interchangeable.

**Forces**
- **FORCED** `S5_from_equivalence` — 5 and B forced on ALL equivalence frames up to n=3
  - *5 and B forced on ALL equivalence frames up to n=3 — full mutual accessibility makes possibility stable*

**Breaks on**
- *PRESUMED* — cross-class inference unavailable  (immediate from the partition structure)

**Useful for:** metaphysical modality · full-introspection epistemics

### 19 · Provability Logic GL (Godel-Lob) (`MODAL_GL`)
*Lob (1955); Solovay (1976); Boolos (1979)*

| | |
|---|---|
| **V** | NECS(P) = 'PA proves P'; frames transitive + conversely well-founded |
| **G** | K + 4 + Lob axiom |
| **θ** | proof depth; well-foundedness of provability |

Necessity as provability: Lob's axiom holds on exactly the transitive conversely-well-founded frames, and T FAILS — a system strong enough to encode itself cannot prove its own soundness. The finite frames below exhibit both facts.

**Forces**
- **FORCED** `GL_lob_on_finite_strict_orders` — Lob axiom forced on all transitive irreflexive frames up to n=3
  - *Loeb axiom forced on all transitive irreflexive frames up to n=3 (finite = conversely well-founded); T fails there — the system cannot prove its own soundness, in miniature*

**Breaks on**
- **FORCED** `GL_lob_on_finite_strict_orders` — T fails on GL frames — provability does not imply truth inside the system
  - *Loeb axiom forced on all transitive irreflexive frames up to n=3 (finite = conversely well-founded); T fails there — the system cannot prove its own soundness, in miniature*
- *PRESUMED* — arithmetical completeness of GL for PA  (Solovay 1976; PRESUMED — needs arithmetic, not frames)

**Useful for:** incompleteness analysis · provability predicates · self-reference limits

### 20 · Epistemic Logic (multi-agent) (`EPISTEMIC`)
*Hintikka (1962); Fagin-Halpern-Moses-Vardi (1995)*

| | |
|---|---|
| **V** | worlds with per-agent indistinguishability relations R_i |
| **G** | K_i = universal over agent i's R; common knowledge = infinite closure |
| **θ** | epistemic indistinguishability per agent |

Knowledge as truth across indistinguishable worlds. Common knowledge is the fixed point of 'everyone knows that' — unreachable by any finite message exchange, which is why coordinated attack fails and simultaneous broadcast exists.

**Forces**
- **FORCED** `epistemic_distribution` — K_i distributes over AND, both directions, every frame
  - *K_i(P AND Q) <-> K_i(P) AND K_i(Q) both directions, every frame up to n=3 — knowledge distributes over conjunction*

**Breaks on**
- *PRESUMED* — common knowledge not achievable by finite communication  (Halpern & Moses 1990, coordinated attack; PRESUMED — an impossibility over unbounded protocols)

**Useful for:** distributed consensus · game theory · cryptographic protocol analysis

### 21 · Temporal Logic (LTL / CTL) (`TEMPORAL`)
*Prior (1957); Pnueli (1977); Clarke & Emerson (1981)*

| | |
|---|---|
| **V** | time steps as worlds; linear traces (LTL) or trees (CTL) |
| **G** | X next, F eventually, G always, U until |
| **θ** | finite paths verify F; G outruns any finite observation |

Modal logic pointed at time: F and G are POSS and NECS over the future. Under the finite-trace semantics this library STIPULATES (and says so), the classical dualities are decidable and decided.

**Forces**
- **FORCED** `ltl_finite_trace_laws` — F/G duality, FF=F, G(p)->p over ALL traces to length 5 (finite-trace semantics, a declared stipulation)
  - *F/G duality, FF=F, and G(p)->p decided over ALL traces up to length 5 — under finite-trace semantics, a stipulation the record declares (G over infinite time is not finitely checkable)*

**Breaks on**
- *PRESUMED* — G undecidable by finite observation on infinite traces  (definitional; the stipulation above is the honest boundary)
- *PRESUMED* — LTL and CTL incomparable in expressive power  (Clarke & Draghicescu 1988; PRESUMED)

**Useful for:** model checking (SPIN, NuSMV) · reactive specs · liveness/safety verification

### 22 · Deontic Logic (`DEONTIC`)
*von Wright (1951); Chisholm (1963)*

| | |
|---|---|
| **V** | worlds ranked by moral ideality; O/P/F over ideal worlds |
| **G** | O(P): P in all ideal accessible worlds; P(P): in some; F=O(NOT P) |
| **θ** | seriality — somewhere, an ideal world exists |

Obligation as necessity over ideal worlds. The one theorem everyone wants — obligatory implies permitted — is priced exactly by seriality, and the frames show it: give a world no ideal neighbor and O(P) holds vacuously while P(P) dies.

**Forces**
- **FORCED** `deontic_O_implies_P` — O(P)->P(P) forced by seriality and ONLY by it — both directions exhibited on frames
  - *O(P)->P(P) forced exactly by seriality (every world sees an ideal world); fails on a frame with a normless dead-end*

**Breaks on**
- *PRESUMED* — contrary-to-duty (Chisholm) paradoxes: violated obligations point at mutually inconsistent ideals  (Chisholm 1963; PRESUMED — a modeling inadequacy, not a frame fact)

**Useful for:** formal ethics / AI alignment · legal reasoning · normative multi-agent systems


## Many-Valued Logic — 6 carriers

### 23 · Post n-Valued Logic (P_n) (`POST_N`)
*Emil Post (1921)*

| | |
|---|---|
| **V** | {0, 1/(n-1), ..., 1} — n equally spaced values |
| **G** | NOT = cyclic shift of order n; AND=min; OR=max |
| **θ** | 1.0 |

Negation generalized from a mirror to a rotation: NOT^n is the identity. At n=2 the cycle IS classical negation and all 15 laws return; for n>2 the value-reading LNC/LEM die at interior points because a rotation is not a complement.

**Forces**
- **FORCED** `post_cyclic` — NOT has order exactly n; n=2 recovers the full classical signature; interior witnesses for value-reading failures
  - *NOT has order n (n=4 verified: 1/3->2/3->1->0->1/3); n=2 recovers all 15 classical laws; at v=1/3 the value-reading witnesses: min(v,NOT v)=1/3 != 0, max=2/3 != 1*

**Breaks on**
- **FORCED** `post_cyclic` — min(v, NOT v) != 0 and max != 1 at v=1/3 for n=4
  - *NOT has order n (n=4 verified: 1/3->2/3->1->0->1/3); n=2 recovers all 15 classical laws; at v=1/3 the value-reading witnesses: min(v,NOT v)=1/3 != 0, max=2/3 != 1*

**Useful for:** finite-valued logic · error-correcting code design · many-valued switching theory

### 24 · Belnap Four-Valued Logic (FOUR) (`BELNAP`)
*Nuel Belnap (1977)*

| | |
|---|---|
| **V** | {N, F, T, B} with independent truth and knowledge orderings |
| **G** | componentwise lattice ops per ordering; NOT swaps T/F, fixes N/B |
| **θ** | T designated; B = maximal but contradictory information |

Truth and information de-conflated: N is no evidence, B is too much. The bilattice keeps orthogonal what classical logic collapses — how a computer should think when its sources disagree.

**Forces**
- **FORCED** `belnap_bilattice` — bilattice structure; NOT swaps truth poles and fixes information poles; lattice laws
  - *NOT swaps truth poles, fixes information poles (N,B); lattice comm holds; LNC fails at the glut B*

**Breaks on**
- **FORCED** `belnap_bilattice` — LNC fails at B (self-negating glut); LEM fails at N
  - *NOT swaps truth poles, fixes information poles (N,B); lattice comm holds; LNC fails at the glut B*

**Useful for:** inconsistent databases · multi-source aggregation · paraconsistent reasoning

### 25 · MV-Algebra (Chang) (`MV_ALG`)
*C.C. Chang (1958)*

| | |
|---|---|
| **V** | [0,1] or any MV-algebra |
| **G** | bounded PLUS = min(1,a+b) and NOT = 1-a as the only primitives |
| **θ** | 1.0; PLUS saturates |

Two primitives generate all of Lukasiewicz logic: saturating addition and complement. 0.7 plus 0.8 is 1, not 1.5 — arithmetic with a ceiling, and the ceiling is what makes the connectives derivable.

**Forces**
- **FORCED** `mv_derives_lukasiewicz` — Lukasiewicz AND and OR both derived from PLUS and NOT on a grid; saturation exhibited
  - *AND/OR both derived from PLUS and NOT alone on a 7-point grid; 0.7(+)0.8 saturates to 1*

**Breaks on**
- *PRESUMED* — Chang completeness for infinite-valued Lukasiewicz  (Chang 1958-59; PRESUMED — a completeness theorem, not a finite enumeration)
- *PRESUMED* — product and Godel t-norms not captured  (standard; different residuated structures)

**Useful for:** algebraic semantics · many-valued arithmetic · probability-adjacent logic

### 26 · Effect Algebra (Quantum Logic) (`EFFECT`)
*Foulis & Bennett (1994)*

| | |
|---|---|
| **V** | quantum effects; [0,1] instance here |
| **G** | PARTIAL sum, defined only for orthogonal pairs; orthocomplement |
| **θ** | orthogonality: a (+) b exists iff a+b <= 1 |

Incompatibility as non-existence: the sum of two non-orthogonal effects is not zero, it is UNDEFINED. Uncertainty becomes a theorem of the algebra's partiality rather than an added postulate.

**Forces**
- **FORCED** `effect_algebra_partial` — commutativity where defined; x (+) x' = 1; the undefined case exhibited (0.7 (+) 0.6)
  - *x(+)x'=1 for all tested effects; 0.7(+)0.6 is UNDEFINED (not zero) — incompatibility as non-existence*

**Breaks on**
- *PRESUMED* — Boolean algebra is the special case where all pairs are orthogonal  (Foulis-Bennett; structural)

**Useful for:** quantum measurement theory · unsharp quantum logic · operational QM

### 27 · Heyting Algebra (`HEYTING`)
*Arend Heyting (1930)*

| | |
|---|---|
| **V** | lattices with implication as the residual of meet |
| **G** | MEET, JOIN, IMP(a,b) = largest c with a AND c <= b; NOT a = IMP(a,0) |
| **θ** | the top element; LEM fails when JOIN cannot reach it |

Implication defined by adjointness makes LNC a definitional consequence and leaves LEM optional. Open sets of any topological space form one: a region refuting P need not be complemented by one proving it — topology IS intuitionism.

**Forces**
- **FORCED** `heyting_open_sets` — adjointness and LNC forced on the open-set algebra of a 2-point space, by complete enumeration
  - *open sets of a 2-point space: adjointness and LNC forced; LEM fails at {a} (neg({a})={} so union misses b)*

**Breaks on**
- **FORCED** `heyting_open_sets` — LEM fails: {a} OR NOT{a} misses the top
  - *open sets of a 2-point space: adjointness and LNC forced; LEM fails at {a} (neg({a})={} so union misses b)*

**Useful for:** intuitionistic semantics · topos theory · locales · sheaf semantics

### 28 · Basic Logic (BL) / Hajek (`BL`)
*Petr Hajek (1998), Metamathematics of Fuzzy Logic*

| | |
|---|---|
| **V** | [0,1] or any BL-algebra |
| **G** | any continuous t-norm with its residuum; divisibility; prelinearity |
| **θ** | 1.0 |

The laws common to ALL continuous-t-norm logics, axiomatized: whatever continuous conjunction you pick, residuation and prelinearity come with it. Lukasiewicz, Godel, and product are the three irreducible generators.

**Forces**
- **CONDITIONAL** `bl_three_tnorms` — residuation and prelinearity hold for all three fundamental t-norms on the verification grid
  - *residuation + prelinearity verified for all three t-norms on a 5-point grid (grid is the stated bound; divisibility exact for these t-norms on it)*

**Breaks on**
- *PRESUMED* — every continuous t-norm is an ordinal sum of the three  (Mostert-Shields 1957; PRESUMED — a classification theorem)

**Useful for:** fuzzy-logic unification · truth-functional reasoning


## Set Theory & Type Theory — 7 carriers

### 29 · Zermelo-Fraenkel Set Theory (ZF/ZFC) (`ZF`)
*Zermelo (1908); Fraenkel (1922); Skolem (1922)*

| | |
|---|---|
| **V** | well-founded sets; cumulative hierarchy V_alpha |
| **G** | membership, power set, union, separation, replacement, infinity |
| **θ** | ordinal rank — patterns cohere at their level |

Mathematics built upward from nothing, level by level. Russell's paradox dies by geography: membership requires a strictly lower level, so nothing contains itself and the Russell class is always the whole floor you are standing on — never available as a brick.

**Forces**
- **FORCED** `zf_foundation_hf` — foundation and extensionality on the hereditarily finite universe; the Russell class at each rank IS the rank, and never a member of itself
  - *hereditarily finite universe, 16 sets: no x with x in x (foundation), extensionality by element comparison; Russell's class = the whole rank, and the rank is never a member of itself*

**Breaks on**
- *PRESUMED* — no universal set; CH undecidable in ZFC  (Godel 1938 + Cohen 1963; PRESUMED — forcing is beyond enumeration by nature)

**Useful for:** foundations · formal verification of mathematics · category-theory foundations

### 30 · New Foundations (NF / NFU) (`NF`)
*Quine (1937); Jensen (1969) NFU*

| | |
|---|---|
| **V** | all sets INCLUDING a universal set |
| **G** | comprehension restricted to stratified formulas |
| **θ** | consistent type-level assignment |

Russell blocked syntactically instead of ontologically: a set-forming formula must admit a consistent typing of its variables. {x : x not-in x} demands t = t+1 and is refused; {x : x = x} types trivially, so the universe exists.

**Forces**
- **FORCED** `nf_stratification` — stratification decided by type unification: Russell unstratifiable, identity stratifiable — the decision procedure implemented and run
  - *stratification decided by type unification: {x : x not-in x} needs t(x)=t(x)+1 (unsatisfiable); {x : x=x} stratifies — the universal set is admitted, Russell's is refused, syntactically*

**Breaks on**
- *PRESUMED* — AC is FALSE in NF (Specker); full NF consistency long open, NFU consistent  (Specker 1953; Jensen 1969; Holmes' claimed proof under review — PRESUMED status per the literature)

**Useful for:** alternative foundations · cardinality without choice

### 31 · Simple Theory of Types (Church) (`STT`)
*Russell (1908); Church (1940)*

| | |
|---|---|
| **V** | typed terms over base types e, t and arrows a->b |
| **G** | lambda abstraction and application, within type boundaries |
| **θ** | typability |

Self-application made ungrammatical: x x needs x to be both a and a->b, and the occurs check says no. The paradoxes are not disproved — they are unwritable.

**Forces**
- **FORCED** `stt_self_application_untypable` — lambda x.xx untypable — unification with occurs check, implemented and refusing
  - *unification with occurs check: a = a->b refused, so lambda x.xx is untypable; Russell's paradox dies in the type checker*

**Breaks on**
- *PRESUMED* — strong normalization of simply-typed terms  (Tait 1967; PRESUMED — reducibility argument)
- *PRESUMED* — no quantification over all types at once  (definitional stratification)

**Useful for:** HOL provers · typed functional languages · semantics of programming

### 32 · Martin-Lof Type Theory (`MLTT`)
*Per Martin-Lof (1975, 1984)*

| | |
|---|---|
| **V** | dependent types; types are first-class values |
| **G** | Pi and Sigma formation, beta/eta, identity types |
| **θ** | universe levels — each Type_n lives in Type_{n+1} |

Propositions ARE types and proofs ARE programs: to prove the universally quantified is to write the function. The universe tower does for type theory what ranks do for ZF.

**Forces**
- **CONDITIONAL** `mltt_curry_howard_instance` — Curry-Howard on an instance: the K combinator inhabits and computes A -> (B -> A)
  - *Curry-Howard on an instance: the K combinator inhabits A->(B->A) and computes; full MLTT (Pi/Sigma/Id, universes) is PRESUMED from Martin-Loef 1984 — this repo does not implement it*

**Breaks on**
- *PRESUMED* — Type:Type is inconsistent (Girard's paradox)  (Girard 1972; PRESUMED)
- *PRESUMED* — uniqueness of identity proofs fails in HoTT models  (Hofmann-Streicher groupoid model 1996; PRESUMED)

**Useful for:** Coq/Agda/Idris · certified software · program extraction

### 33 · Homotopy Type Theory (`HOTT`)
*Voevodsky (2006-2010); Univalent Foundations Program (2013)*

| | |
|---|---|
| **V** | types as spaces; identity proofs as paths; higher structure |
| **G** | path induction, transport, univalence: (A=B) = (A~=B) |
| **θ** | homotopy dimension |

Equality gets geometry: two proofs of a=b can themselves differ, and univalence declares isomorphic types literally equal. Structure-transport for free, at the cost of classical certainties becoming undecided.

**Forces**
- *PRESUMED* — univalence; function extensionality derivable; higher inductive types  (HoTT Book 2013; PRESUMED — this library does not implement a proof assistant, and says so)

**Breaks on**
- *PRESUMED* — LEM and AC undecided in pure HoTT  (HoTT Book ch.3; PRESUMED)

**Useful for:** univalent foundations · cubical Agda / Lean · synthetic homotopy theory

### 34 · Topos Logic (Lawvere-Tierney) (`TOPOS`)
*Lawvere & Tierney (1969-72)*

| | |
|---|---|
| **V** | a topos's subobject classifier Omega |
| **G** | connectives as universal properties on Omega |
| **θ** | the Grothendieck topology chosen |

Each mathematical universe carries its own logic, read off its Omega: in Set the classifier is {0,1} and logic is classical; in sheaves it is the opens, and logic goes intuitionistic. Logic is a dependent variable.

**Forces**
- **FORCED** `topos_subobject_classifier_Set` — Sub(A) ~ Hom(A, Omega) by complete enumeration in Set for |A| <= 3
  - *Sub(A) ~ Hom(A, {0,1}) verified by complete enumeration for |A| <= 3 — characteristic functions classify subobjects in Set*
- **FORCED** `heyting_open_sets` — sheaf-style Omega is Heyting, not Boolean: the open-set instance
  - *open sets of a 2-point space: adjointness and LNC forced; LEM fails at {a} (neg({a})={} so union misses b)*

**Breaks on**
- *PRESUMED* — LEM only in Boolean toposes  (Mac Lane & Moerdijk; PRESUMED as the general theorem — the failing instance above is exhibited)

**Useful for:** algebraic geometry · synthetic differential geometry · alternative foundations

### 65 · Ordinal Arithmetic (Cantor Normal Form) (`ORDINALS`)
*Cantor (1883); Gentzen (1936)*

| | |
|---|---|
| **V** | ordinals in CNF below epsilon_0 |
| **G** | non-commutative +, *, and omega-exponentiation on normal forms |
| **θ** | epsilon_0 — the proof-theoretic ordinal of PA |

Order types with base-omega positional notation. Addition reads left to right through infinity: a finite prefix drowns (1+w=w) while a finite suffix survives (w+1>w). Gentzen located PA exactly here: induction to epsilon_0 is PA's consistency, no more, no less.

**Forces**
- **FORCED** `ordinal_noncommutative` — CNF arithmetic implemented: 1+w=w yet w+1>w; every ordinal has a strict successor
  - *CNF arithmetic implemented and enumerated: 1+w=w yet w+1>w (commutativity dies at the first limit); every ordinal has a strict successor; normal form unique by construction*
- **FORCED** `ordinal_normal_form_unique` — normal forms are canonical: regrouping lands on the identical representation
  - *associativity regroups to the identical normal form — representation is canonical, like decimal notation with base omega*

**Breaks on**
- **FORCED** `ordinal_noncommutative` — commutativity of + and * — dead at the first limit
  - *CNF arithmetic implemented and enumerated: 1+w=w yet w+1>w (commutativity dies at the first limit); every ordinal has a strict successor; normal form unique by construction*
- *PRESUMED* — Gentzen: Con(PA) = induction to epsilon_0  (Gentzen 1936; PRESUMED — proof theory, not enumeration)

**Useful for:** ordinal analysis · termination proofs · consistency strength


## Mathematical Carriers — 19 carriers

### 35 · Differential Calculus (Dual Numbers) (`DUAL_NUM`)
*Leibniz (1684); Clifford (1873); Wengert (1964) autodiff*

| | |
|---|---|
| **V** | dual numbers a + b*eps with eps^2 = 0 |
| **G** | arithmetic extended through eps; the eps-slot carries the derivative |
| **θ** | machine epsilon |

One nilpotent element forces all of differential calculus: the product rule IS the cross term of (a+b eps)(c+d eps), the chain rule IS composition. Every autodiff framework is this algebra wearing a tensor library.

**Forces**
- **FORCED** `dual_product_chain_rule` — product and chain rules match sympy's derivatives exactly — forced by eps^2=0
  - *eps^2=0 forces Leibniz: dual product epsilon-part equals sympy's d(fg) exactly at x=1.7; chain rule likewise for (x^2-1)^3 — the rules are arithmetic, not axioms*

**Breaks on**
- **FORCED** `dual_nonsmooth_limit` — |x| at 0: one-sided slopes disagree — subgradients, not a derivative
  - *|x| at 0: one-sided slopes +1 and -1 — the subgradient set, not a derivative; smoothness is the carrier's theta*
- *PRESUMED* — stochastic paths need the Ito correction  (see the Ito carrier, where it is measured)

**Useful for:** backpropagation · scientific computing · sensitivity

### 36 · Complex Analysis (C-carrier) (`COMPLEX`)
*Cardano (1545); Euler; Cauchy (1821); Riemann (1851)*

| | |
|---|---|
| **V** | C = R^2 with rotation as multiplication |
| **G** | complex product; Cauchy-Riemann coupling; contour integration |
| **θ** | radius of analytic continuation |

Rotation baked into arithmetic (i^2 = -1 is two quarter-turns making a negation) buys ferocious rigidity: differentiable once means analytic forever, and closed loops integrate to zero unless they trap a singularity.

**Forces**
- **FORCED** `complex_cauchy_riemann` — Cauchy-Riemann verified symbolically for z^2 and exp(z)
  - *Cauchy-Riemann verified symbolically for z^2 and exp(z); |z|^2 breaks CR (u_x=2x != v_y=0) — real-smooth is not complex-differentiable*
- **CONDITIONAL** `complex_contour_theorem` — closed contour of z^2 vanishes; 1/z picks up exactly 2 pi i
  - *closed contour of z^2 = 3.8e-17 (Cauchy: 0); closed contour of 1/z = 2*pi*i to 1e-3 (the branch point priced) — numeric quadrature, tolerance stated*

**Breaks on**
- **FORCED** `complex_cauchy_riemann` — |z|^2 is real-smooth but not holomorphic — CR fails symbolically
  - *Cauchy-Riemann verified symbolically for z^2 and exp(z); |z|^2 breaks CR (u_x=2x != v_y=0) — real-smooth is not complex-differentiable*
- *PRESUMED* — log needs a branch cut  (standard; multivaluedness)

**Useful for:** fluid dynamics · electromagnetism · Fourier analysis · zeta and number theory

### 37 · Non-Standard Analysis (*R) (`NSA`)
*Abraham Robinson (1966)*

| | |
|---|---|
| **V** | hyperreals: R plus genuine infinitesimals and infinite numbers |
| **G** | transfer principle; standard-part projection |
| **θ** | the monad around each real |

Infinitesimals rehabilitated by model theory: every first-order truth about R transfers to *R, so dy/dx becomes a literal ratio and limits become the algebraic act of taking the standard part.

**Forces**
- *PRESUMED* — transfer principle; saturation  (Robinson 1966 via ultrapowers and compactness; PRESUMED — the construction needs an ultrafilter, which no enumeration exhibits. The dual-number carrier is this library's executable cousin)

**Breaks on**
- *PRESUMED* — the set of infinitesimals is external — unnameable inside the system  (Robinson 1966; PRESUMED)

**Useful for:** rigorous infinitesimal calculus · hyperfinite probability · ultraproducts

### 38 · p-adic Numbers (Q_p) (`PADIC`)
*Kurt Hensel (1897)*

| | |
|---|---|
| **V** | completion of Q under |x|_p = p^(-v_p(x)) |
| **G** | p-adic valuation and ultrametric distance |
| **θ** | 1/p — the unit ball |

Size inverted: divisible-by-p means SMALL. The metric sharpens to an ultrametric, every triangle is isosceles, and 1+p+p^2+... converges — to a negative rational.

**Forces**
- **FORCED** `padic_ultrametric` — ultrametric and isosceles property on random rationals; the geometric series of 5 sums to -1/4 in |.|_5
  - *ultrametric and every-triangle-isosceles verified on 60 random rationals (5-adic); the geometric series of p converges to 1/(1-p) = -1/4 in |.|_5 while diverging in R — smallness is divisibility*

**Breaks on**
- *PRESUMED* — Q_p and R are non-isomorphic completions; Ostrowski says they exhaust the options  (Ostrowski 1916; PRESUMED)

**Useful for:** local-global number theory · lattice cryptography · coding theory

### 39 · Tropical Arithmetic (min-plus) (`TROPICAL`)
*Cuninghame-Green (1960s); Maslov (1987)*

| | |
|---|---|
| **V** | R with +infinity; ADD=min, MUL=+ |
| **G** | idempotent semiring operations |
| **θ** | 0, the multiplicative identity |

Arithmetic where addition takes the better option and multiplication accumulates cost: matrix powers become shortest paths because Bellman's recursion IS tropical matrix multiplication. Optimization as algebra.

**Forces**
- **FORCED** `tropical_shortest_path` — semiring laws; tropical matrix power equals Floyd-Warshall exactly on a random graph
  - *semiring laws enumerated on samples; tropical matrix power equals Floyd-Warshall on a random 6-node graph exactly — Bellman's equation IS tropical multiplication*

**Breaks on**
- *PRESUMED* — no subtraction: min has no inverse  (idempotency kills cancellation; definitional)

**Useful for:** shortest paths · scheduling · tropical geometry · phylogenetics

### 40 · Quantum Mechanics (Density Matrix) (`QUANTUM`)
*von Neumann (1932); Dirac (1930)*

| | |
|---|---|
| **V** | positive Hermitian rho with trace 1 |
| **G** | unitary conjugation (reversible); measurement update (not) |
| **θ** | purity Tr(rho^2) |

States as operators: unitaries move probability without creating or destroying it, measurement renormalizes onto the observed branch, and linearity alone forbids copying the unknown.

**Forces**
- **FORCED** `quantum_density_matrix` — unitary evolution preserves trace and purity; Born weights normalize; no-cloning exhibited on a non-orthogonal pair
  - *random 3-level state: unitary evolution preserves trace and purity to 1e-10; measurement renormalizes with Born weight in [0,1]; cloning-by-linearity contradicts the clone of a superposition on the ex*

**Breaks on**
- *PRESUMED* — measurement is irreversible — the carrier changes  (see the Measurement Interpretations section, where the readings of this fact are priced separately)
- *PRESUMED* — non-commuting observables (Heisenberg)  ([x,p]=ih; standard)

**Useful for:** quantum computing · QKD · error correction

### 41 · Information Theory (Shannon) (`SHANNON`)
*Claude Shannon (1948)*

| | |
|---|---|
| **V** | probability distributions; entropies in bits |
| **G** | entropy, mutual information, KL divergence, capacity |
| **θ** | channel capacity C |

Uncertainty quantified once, correctly: H is the compression floor, capacity the transmission ceiling, and the data-processing inequality the law that no massaging of Y ever tells you more about X.

**Forces**
- **EMPIRICAL** `shannon_dpi` — data-processing inequality on 40 random Markov chains; BSC capacity computed
  - *data processing inequality I(X;Z) <= I(X;Y) held on 40 random Markov chains X->Y->Z (3-symbol); BSC(0.11) capacity 1-h(0.11) = 0.500 bits — processing only loses information*

**Breaks on**
- *PRESUMED* — differential entropy can be negative; zero-error theory is a different beast  (Shannon 1948; Korner-Orlitsky survey; PRESUMED)

**Useful for:** compression · error-correcting codes · crypto floors

### 42 · Statistical Mechanics (Gibbs/Boltzmann) (`STATMECH`)
*Boltzmann (1872); Gibbs (1902)*

| | |
|---|---|
| **V** | distributions over microstates |
| **G** | Hamiltonian flow (volume-preserving); entropy ascent |
| **θ** | k_B T — the thermal load unit |

The bridge from mechanics to thermodynamics is a constrained maximization: fix mean energy, maximize entropy, get exp(-E/kT) uniquely. Everything macroscopic is a derivative of its normalizer.

**Forces**
- **EMPIRICAL** `statmech_gibbs_maximizes` — Boltzmann beats every constraint-respecting perturbation — entropy maximum verified in the exact null space
  - *483 random perturbations inside the exact constraint null-space (sum and mean energy preserved to machine precision): none increased entropy — Gibbs is the constrained maximum, as strict concavity dem*

**Breaks on**
- *PRESUMED* — microscopic reversibility vs macroscopic arrow (Loschmidt); fluctuations in small systems  (Boltzmann's reply and modern fluctuation theorems; PRESUMED — see the Markov H-theorem check under Thermodynamics for the measurable core)

**Useful for:** materials · reaction rates · computation thermodynamics

### 43 · Fisher Information (Statistical Manifold) (`FISHER`)
*Fisher (1925); Rao (1945); Amari (1985)*

| | |
|---|---|
| **V** | smooth families of distributions |
| **G** | Fisher metric; natural gradient |
| **θ** | F itself — sensitivity per parameter |

Distinguishability given a geometry: F measures how loudly the data protests a parameter change, Cramer-Rao makes 1/F the price floor of unbiased estimation, and the natural gradient is descent that respects the terrain.

**Forces**
- **FORCED** `fisher_cramer_rao_gaussian` — Gaussian F = 1/sigma^2 computed symbolically; the sample mean sits exactly on the Cramer-Rao floor
  - *Fisher information of the Gaussian mean computed symbolically: F = 1/sigma^2 exactly, so Cramer-Rao floor = sigma^2 — met with equality by the sample mean (var sigma^2/n = (nF)^-1)*

**Breaks on**
- *PRESUMED* — singular models break invertibility  (Watanabe, singular learning theory; PRESUMED)

**Useful for:** optimal estimation · natural-gradient training · TRPO/PPO

### 55 · Category Theory (Functors & Naturality) (`CATEGORY`)
*Eilenberg & Mac Lane (1945)*

| | |
|---|---|
| **V** | objects known only through their morphisms |
| **G** | functors, natural transformations, adjunctions |
| **θ** | functoriality and naturality squares |

Identity through relationship: Yoneda says an object IS its pattern of incoming maps. The library runs the miniature: in a finite category, distinct objects have distinct hom-profiles, and the monad laws compute.

**Forces**
- **FORCED** `category_yoneda_finite` — Yoneda in miniature: hom-profiles separate all objects of a finite poset category
  - *Yoneda in miniature: in the poset category 0<=1<=2, the presheaf profile Hom(-,A) is distinct for every object — objects are determined by their morphisms, enumerated*
- **FORCED** `category_monad_laws` — monad laws for Maybe and List by complete enumeration
  - *Maybe and List monads: left identity, right identity, and associativity decided by complete enumeration over a 3-value domain and sampled Kleisli arrows — the monoid laws, executed*

**Breaks on**
- *PRESUMED* — not every functor has an adjoint; size issues loom  (Freyd adjoint functor theorem; PRESUMED)

**Useful for:** universal algebra · Haskell/Scala types · sheaves and topoi

### 56 · Galois Theory (Field Extensions) (`GALOIS`)
*Galois (1832); Dedekind & Weber (1882)*

| | |
|---|---|
| **V** | splitting fields with their automorphism groups |
| **G** | the order-reversing subgroup/subfield correspondence |
| **θ** | solvability of the group |

Polynomial solvability converted to group structure. The library enumerates the classic instance completely: Q(sqrt2,sqrt3) has group C2xC2 and its three subgroups fix exactly the three intermediate fields — the correspondence, run rather than recited.

**Forces**
- **FORCED** `galois_biquadratic` — all four automorphisms are field homs; group is C2xC2; three subgroups <-> three intermediate fields, enumerated
  - *Q(sqrt2,sqrt3): all four automorphisms verified as field homs; group = C2xC2 (every element self-inverse); the three proper subgroups fix exactly the three intermediate fields Q(sqrt3), Q(sqrt2), Q(sq*

**Breaks on**
- *PRESUMED* — degree >= 5 generically unsolvable (A_5 simple)  (Abel 1824, Galois 1832; PRESUMED — simplicity of A_5 not re-derived here)

**Useful for:** impossibility proofs · class field theory · elliptic-curve crypto · BCH codes

### 57 · Lebesgue Measure Theory (`LEBESGUE`)
*Lebesgue (1902); Borel (1898)*

| | |
|---|---|
| **V** | sigma-algebras with countably additive measure |
| **G** | integrate by partitioning the RANGE; Radon-Nikodym densities |
| **θ** | sigma-finiteness; completeness of L^p |

Integration turned sideways: slice function values, not the domain, and the pathological becomes tame — the indicator of the rationals integrates to 0 because countable sets vanish under any epsilon of covering.

**Forces**
- **CONDITIONAL** `lebesgue_convergence_instance` — monotone convergence exhibited; the rationals covered by total length < any epsilon, exactly
  - *monotone convergence exhibited on x^(1/n) up 1; the rationals covered by intervals of total length < any eps (geometric series, exact) — the Riemann-unintegrable 1_Q integrates to 0*

**Breaks on**
- *PRESUMED* — non-measurable sets under AC (Vitali, Banach-Tarski)  (Vitali 1905; PRESUMED — requires choice, definitionally beyond construction)
- *PRESUMED* — conditionally convergent improper integrals lost  (sin(x)/x on [0,oo); standard)

**Useful for:** probability foundations · L^2 Fourier theory · weak PDE solutions · stochastic integration

### 58 · Stochastic Calculus (Ito) (`ITO`)
*Kiyosi Ito (1944, 1951)*

| | |
|---|---|
| **V** | adapted processes on filtered probability spaces |
| **G** | the Ito integral (left endpoints, non-anticipating); Ito's lemma |
| **θ** | quadratic variation [W,W]_t = t |

Brownian paths carry area at first order — (dW)^2 = dt — so the chain rule must pay a second-derivative tax. The library MEASURES it: quadratic variation lands on t and W^2 - t sits flat, as the correction demands.

**Forces**
- **EMPIRICAL** `ito_quadratic_variation` — quadratic variation = t, W^2-t a martingale, isometry — 1500 paths, 4-sigma bounds from measured spread
  - *1500 Brownian paths, N=2000: quadratic variation mean 1.0003 vs t=1 with per-path spread 0.032 (the (dW)^2=dt fact, tightening as 1/sqrt(N)); W_t^2 - t mean -0.070 within 4 standard errors of 0 (Ito c*

**Breaks on**
- *PRESUMED* — the naive chain rule fails; Stratonovich buys it back at the cost of anticipation  (Ito 1951; Stratonovich 1966; PRESUMED as the general theorems — the failing instance is what the check measures)

**Useful for:** Black-Scholes · Langevin/Fokker-Planck · Kalman filtering · stochastic control

### 59 · Exterior Algebra & Differential Forms (`EXTERIOR`)
*Grassmann (1844); Cartan (1899); de Rham (1931)*

| | |
|---|---|
| **V** | antisymmetric multilinear k-forms |
| **G** | wedge product; exterior derivative d |
| **θ** | d^2 = 0 — the nilpotency identity |

Symmetric second partials meet antisymmetric wedges and cancel identically: d^2=0 is bookkeeping, not physics. Stokes then unifies every classical integral theorem into one equation, and the failures of local-to-global exactness are precisely the holes.

**Forces**
- **FORCED** `exterior_d_squared_zero` — d(d omega) = 0 symbolically for a random polynomial 1-form; Stokes on the unit square, exactly
  - *d(d(omega)) = 0 for a random polynomial 1-form on R^3 — the mixed partials cancel against wedge antisymmetry exactly; Stokes on the unit square: area integral equals line integral, symbolically*

**Breaks on**
- *PRESUMED* — closed but non-exact forms live on holes (H^1 of the circle)  (de Rham; the homology carrier computes the hole count executably)

**Useful for:** Maxwell in two lines · GR in form language · de Rham cohomology

### 60 · Lie Groups & Lie Algebras (`LIE`)
*Lie (1870s); Killing (1888); Cartan (1894)*

| | |
|---|---|
| **V** | smooth groups; tangent algebra at the identity |
| **G** | bracket [X,Y]; exponential map |
| **θ** | non-degeneracy of the Killing form |

Continuous symmetry differentiated: the bracket measures how flows fail to commute, exp reassembles the group from its germs, and Cartan's list of simple algebras is the periodic table of symmetry.

**Forces**
- **FORCED** `lie_so3_jacobi` — so(3): antisymmetry + Jacobi for all 27 basis triples, exactly; exp is a one-parameter homomorphism
  - *so(3): antisymmetry and the Jacobi identity verified for all 27 basis triples exactly; [Lx,Ly]=Lz; exp(tLz)exp(sLz)=exp((t+s)Lz) to machine precision — infinitesimal to finite, checked*

**Breaks on**
- *PRESUMED* — the algebra fixes the group only locally: SO(3) vs SU(2)  (double cover; PRESUMED — global topology outruns the tangent space)

**Useful for:** gauge symmetry · robotics (SO(3)/SE(3)) · symmetry reduction of ODEs

### 61 · Algebraic Topology (Singular Homology) (`HOMOLOGY`)
*Poincare (1895); Eilenberg-Steenrod (1945)*

| | |
|---|---|
| **V** | chain complexes over spaces |
| **G** | boundary maps with d.d = 0; induced maps |
| **θ** | Betti numbers |

Holes counted by linear algebra: cycles that bound nothing are the voids. The library computes them: boundary-of-boundary is the zero matrix, the circle scores (1,1), the tetrahedral sphere (1,0,1).

**Forces**
- **FORCED** `homology_circle_sphere` — d.d = 0 exactly; Betti numbers of circle and sphere by rank computation
  - *boundary-of-boundary is the zero matrix exactly; Betti numbers computed by rank: circle (1,1) — one loop; tetrahedral sphere (1,0,1) — one 2-hole, no 1-holes. Holes, counted by linear algebra*

**Breaks on**
- *PRESUMED* — homology is not a complete invariant (lens spaces); higher homotopy sees more  (Whitehead, lens space classification; PRESUMED)

**Useful for:** persistent homology / TDA · topological phases · configuration spaces

### 62 · Convex Analysis (KKT & Fenchel) (`CONVEX`)
*Fenchel (1949); Kuhn-Tucker (1951); Rockafellar (1970)*

| | |
|---|---|
| **V** | convex sets and functions |
| **G** | subgradients; conjugation; Lagrangian duality |
| **θ** | zero duality gap (Slater) |

The geometry where local honesty is global truth: every minimum is THE minimum, optimality certificates come as multipliers, and conjugating twice hands the function back unchanged.

**Forces**
- **FORCED** `convex_kkt_fenchel` — KKT solved exactly on a QP: multiplier nonneg, complementary slackness zero; f** = f for x^2
  - *KKT solved exactly for min x^2+y^2 s.t. x+y>=1: optimum (1/2,1/2), lambda=1>=0, complementary slackness 0; Fenchel double conjugate of x^2 returns x^2 — duality is an involution*

**Breaks on**
- *PRESUMED* — non-convexity demotes KKT to necessary-only  (standard; local minima return)

**Useful for:** SVM/LASSO · conic programming · compressed sensing · MPC

### 63 · Symplectic Geometry (Hamiltonian) (`SYMPLECTIC`)
*Lagrange (1808); Hamilton (1833); Arnold (1974)*

| | |
|---|---|
| **V** | even-dimensional phase space with a closed 2-form |
| **G** | Hamiltonian flows; Poisson bracket |
| **θ** | Liouville volume preservation |

Mechanics as geometry: the bracket runs the dynamics, symmetries become conserved quantities by Noether's dictionary, and phase-space volume is incompressible — which the discrete symplectic map honors with determinant exactly one.

**Forces**
- **FORCED** `symplectic_liouville_poisson` — bracket antisymmetry + Jacobi symbolically; symplectic Euler Jacobian det = 1 EXACTLY; energy conserved
  - *Poisson bracket antisymmetry and Jacobi verified symbolically on polynomial observables; symplectic Euler Jacobian det = 1 EXACTLY (Liouville for the discrete map); {H,H}=0 — energy conserved*

**Breaks on**
- *PRESUMED* — dissipation cannot be Hamiltonian; no-go for full quantization (Groenewold-van Hove)  (Groenewold 1946; PRESUMED)

**Useful for:** integrable systems · geometric integrators · canonical quantization · ray optics

### 64 · Surreal Numbers (Conway) (`SURREAL`)
*Conway (1976); Knuth (1974)*

| | |
|---|---|
| **V** | games {L|R} with no left option >= any right option |
| **G** | recursive addition, negation, multiplication; simplicity rule |
| **θ** | birthday — earlier is simpler is canonical |

Numbers born from nothing by a single recursion, ordered by one comparison rule. The library runs day 0 through 2: {0|1}+{0|1}=1 and 1+(-1)=0 fall out of the game order alone, no field axioms invoked.

**Forces**
- **FORCED** `surreal_birthdays` — Conway arithmetic on finite birthdays: half+half=1, additive inverses cancel, 1+1={1|}
  - *Conway's recursion implemented: {0|1}+{0|1} = 1, 1+(-1) = 0, 1+1 = {1|} — day-0..2 arithmetic verified by the game-order definition alone; the proper-class totality is PRESUMED*

**Breaks on**
- *PRESUMED* — No is a proper class — ZFC cannot hold it as one object  (Conway 1976; PRESUMED)

**Useful for:** combinatorial game theory · alternative infinitesimals · the maximal ordered field


## Computer Science — 15 carriers

### 44 · Kleene Algebra (Regular Languages) (`KLEENE`)
*Kleene (1956); Kozen (1994)*

| | |
|---|---|
| **V** | regular languages over an alphabet |
| **G** | union, concatenation, star |
| **θ** | automaton state count |

An idempotent semiring with closure: star is the least fixed point of repetition. Equality of regular expressions is DECIDABLE, and the library decides it — via automata, the semantic referee.

**Forces**
- **CONDITIONAL** `kleene_star_fixpoint` — a* = 1 + a a*, idempotency, and a denesting identity decided by NFA language comparison (bounded word length, stated)
  - *a* = 1 + a a*, a+a = a, and (a+b)* = (a* b*)* decided by NFA language comparison over all words up to length 6 — the bound is stated; for these star heights it separates all candidates*

**Breaks on**
- *PRESUMED* — context-free is out of reach (pumping)  (Bar-Hillel et al. 1961; PRESUMED)

**Useful for:** regex engines · model checking · protocol verification

### 45 · Hoare Logic (Pre/Postconditions) (`HOARE`)
*Tony Hoare (1969)*

| | |
|---|---|
| **V** | predicates over program states |
| **G** | triples composed sequentially; assignment reasons backwards |
| **θ** | partial vs total correctness |

Programs as predicate transformers: the loop rule is the whole game — find the invariant, show the body keeps it, conjoin the exit condition. The library establishes one over an entire bounded state space.

**Forces**
- **CONDITIONAL** `hoare_wp_bounded` — invariant established, preserved by every body execution, postcondition at exit — full space n < 8
  - *loop invariant s = i(i-1)/2 established, preserved by every body execution, and conjoined with the exit condition yields the postcondition — checked over the full state space n < 8 (the bound is the s*

**Breaks on**
- *PRESUMED* — unbounded loops need termination arguments beyond partial correctness  (total correctness needs well-founded variants; standard)

**Useful for:** Why3/VeriFast · safety-critical code · kernel proofs

### 46 · Separation Logic (Heaps) (`SEPARATION`)
*Reynolds (2002); O'Hearn & Pym (1999)*

| | |
|---|---|
| **V** | heaps as partial address maps |
| **G** | separating conjunction over DISJOINT regions; frame rule |
| **θ** | footprint disjointness |

Local reasoning made sound by geometry: P*R splits the heap, a command touching only P's footprint cannot disturb R, so specifications compose. Enumerated here over every small heap: the frame survives every mutation.

**Forces**
- **FORCED** `separation_frame_rule` — frame rule verified over all enumerated heaps: the R-region is bit-identical after the mutation
  - *{1|->_} [1]:=7 {1|->7} framed by every disjoint R over the enumerated heap space: the R-region is bit-identical after — local reasoning is sound because footprints are disjoint*

**Breaks on**
- *PRESUMED* — concurrency and permissions need CSL machinery  (O'Hearn 2007; PRESUMED)

**Useful for:** memory-safety proofs · Rust semantics · OS verification

### 47 · Lambda Calculus (`LAMBDA`)
*Church (1932-36); Church-Rosser (1936)*

| | |
|---|---|
| **V** | lambda terms (de Bruijn here) |
| **G** | beta reduction |
| **θ** | possession of a normal form |

Two constructors and one rewrite rule reach all of computation. Confluence means reduction order cannot change answers, only whether you get one — and Omega demonstrates the 'whether' live.

**Forces**
- **CONDITIONAL** `lambda_church_rosser_bounded` — both redex orders of (II)(II) join; Church 2+2 reduces to Church 4 exactly; Omega finds no normal form in 100 steps (bound stated)
  - *confluence exhibited: both redex choices of (II)(II) join at the same normal form; Church 2+2 beta-reduces to Church 4 exactly; Omega has no normal form within 100 steps — the bound is honest (diverge*

**Breaks on**
- *PRESUMED* — normal-form possession undecidable in general  (Church 1936; PRESUMED — the fuel bound above is the honest finite shadow of it)

**Useful for:** functional languages · Curry-Howard · semantics

### 48 · Domain Theory (Scott) (`DOMAIN`)
*Dana Scott (1969-70)*

| | |
|---|---|
| **V** | complete partial orders with bottom = undefined |
| **G** | Scott-continuous functions; least fixed points by iteration |
| **θ** | approximation depth from bottom |

Recursion as a limit: start knowing nothing, unfold once per stage, and the ascending chain of partial answers converges to the meaning. The library iterates factorial into existence and watches the chain go stationary.

**Forces**
- **FORCED** `domain_lfp_iteration` — Kleene iteration reaches the least fixed point of the factorial functional; the chain is monotone
  - *Kleene iteration from bottom: each unfolding defines factorial on one more input, the chain is monotone (bot only ever resolves upward), and the least fixed point on 0..6 is reached and stationary — r*

**Breaks on**
- *PRESUMED* — parallel-or is not sequentially definable  (Plotkin 1977; PRESUMED)

**Useful for:** denotational semantics · laziness · recursive types

### 49 · Abstract Interpretation (Galois) (`ABSINT`)
*Cousot & Cousot (1977)*

| | |
|---|---|
| **V** | concrete states vs abstract approximations |
| **G** | alpha (abstract) adjoint to gamma (concretize); widening |
| **θ** | precision of the abstraction |

Program analysis as a Galois connection: the abstract world must over-approximate, so anything it rules out is truly absent — false positives are the tax, unsoundness never. The adjunction is decided here over the whole finite lattice.

**Forces**
- **FORCED** `absint_interval_galois` — alpha(S) <= a iff S <= gamma(a) over ALL subsets x ALL intervals; abstract + soundly over-approximates
  - *alpha(S) <= a iff S <= gamma(a) decided over ALL subsets (size<=3) x ALL intervals of 0..7 — a genuine Galois connection; abstract + soundly over-approximates concrete + (false positives are the price*

**Breaks on**
- *PRESUMED* — precision vs termination is a real trade (widening)  (Cousot^2 1977; structural)

**Useful for:** static analysis · verified compilers · taint analysis

### 50 · Process Algebra (CCS/CSP) (`PROCESS`)
*Milner (1980); Hoare (1985)*

| | |
|---|---|
| **V** | labelled transition systems up to bisimulation |
| **G** | prefix, choice, parallel composition with synchronization |
| **θ** | bisimulation depth |

Equivalence for interactive systems: traces record what happened, bisimulation records what could have been refused. The classic pair a.(b+c) vs a.b+a.c — identical traces, different commitments — is separated live by partition refinement.

**Forces**
- **FORCED** `bisimulation_vs_traces` — trace-equal but not bisimilar: the classic pair, computed
  - *a.(b+c) and a.b+a.c have identical trace sets (enumerated to depth 3) yet partition refinement separates them — after 'a', one still offers a choice, the other has already committed. Bisimulation sees*

**Breaks on**
- *PRESUMED* — general process equivalence undecidable (Turing power)  (Milner; PRESUMED)

**Useful for:** protocol verification · session types · Go channels

### 66 · Computability Theory (Turing) (`COMPUTABILITY`)
*Turing (1936); Church (1936); Kleene (1936)*

| | |
|---|---|
| **V** | partial functions N -> N; machines as data |
| **G** | universal simulation; many-one and Turing reductions |
| **θ** | totality / decidability |

The founding move: programs are strings, so machines can eat machines — the library's interpreter runs the busy beaver to its halt. The diagonal then lives exactly where no bounded demo can reach, and is tagged accordingly.

**Forces**
- **FORCED** `tm_universal_simulation` — TM interpreter runs the 2-state busy-beaver champion: halts at step 6 with 4 ones
  - *the 2-state busy-beaver champion simulated: halts in exactly 6 steps with 4 ones — machines-as-data runs; that no machine DECIDES halting for all inputs is PRESUMED (Turing 1936), and must be: the dia*

**Breaks on**
- *PRESUMED* — halting undecidable; Rice's theorem  (Turing 1936; Rice 1953; PRESUMED — necessarily: the diagonal quantifies over all machines)

**Useful for:** undecidability proofs · reductions · the CS bedrock

### 67 · Computational Complexity (P vs NP) (`COMPLEXITY`)
*Cook (1971); Karp (1972); Razborov (1987)*

| | |
|---|---|
| **V** | languages sorted into resource classes |
| **G** | polynomial-time reductions; circuits |
| **θ** | polynomial = feasible (Cobham) |

What can be VERIFIED fast versus what can be FOUND fast. The library runs Karp in miniature — a 3-coloring instance reduced to SAT, both sides brute-forced, answers agreeing — and files the big question at the only honest tier it has.

**Forces**
- **FORCED** `sat_reduction_instance` — reduction instance preserves the answer: 3-coloring to SAT, both brute-forced and agreeing
  - *Karp in miniature: 3-coloring encoded as SAT; both sides brute-forced and they AGREE (satisfiable, and K4 correctly uncolorable) — the reduction preserves the answer on the instance; that SAT is NP-co*
- *PRESUMED* — time hierarchy: more time is more power  (Hartmanis-Stearns 1965; PRESUMED)

**Breaks on**
- *OPEN* — P vs NP  (Clay Millennium Problem, open since 1971; relativization and natural-proofs barriers block the known routes)
- *PRESUMED* — natural proofs barrier  (Razborov-Rudich 1997; PRESUMED)

**Useful for:** crypto hardness · approximation regimes · SAT-solver practice

### 68 · Proof Theory (Gentzen) (`PROOF_THEORY`)
*Hilbert (1900); Gentzen (1935); Takeuti; Feferman*

| | |
|---|---|
| **V** | proofs as syntactic trees; sequents |
| **G** | cut elimination; ordinal assignment |
| **θ** | the proof-theoretic ordinal |

Proofs as objects of study: cut elimination trades lemmas for transparency (every formula a subformula of the goal), and each theory earns an ordinal — its exact rung on the consistency-strength ladder. This section is deliberately citation-heavy: cut elimination's blowup is precisely why no small demo does it justice, and the paid fraction says so.

**Forces**
- *PRESUMED* — Hauptsatz: every provable sequent has a cut-free proof  (Gentzen 1935; PRESUMED)
- *PRESUMED* — Con(PA) equivalent to induction below epsilon_0 — the ordinal side is executable in the ORDINALS carrier  (Gentzen 1936; PRESUMED here, CNF arithmetic FORCED there)

**Breaks on**
- *PRESUMED* — no sufficiently strong consistent T proves Con(T)  (Godel 1931; PRESUMED)
- *PRESUMED* — cut-free proofs can be non-elementarily longer  (Statman 1978; PRESUMED)

**Useful for:** consistency proofs · reverse mathematics · automated deduction

### 69 · Model Theory (Tarski) (`MODEL_THEORY`)
*Tarski (1936); Godel (1930); Morley (1965)*

| | |
|---|---|
| **V** | first-order structures and their theories |
| **G** | Tarskian satisfaction; ultraproducts; elementary maps |
| **θ** | cardinality — which first-order logic cannot pin down |

Languages meet their interpretations: truth defined compositionally (and implemented here, running on finite graphs), completeness weds proof to validity, and compactness guarantees non-standard models — infinitesimals and infinite integers are features of first-order expressiveness, not bugs.

**Forces**
- **FORCED** `tarski_satisfaction_finite` — Tarski satisfaction implemented; isomorphic finite structures agree on every tested sentence
  - *Tarski's truth definition implemented compositionally; the 3-cycle satisfies totality and irreflexivity; two isomorphic presentations agree on every tested sentence — satisfaction is structural. Compa*
- *PRESUMED* — completeness: provable iff valid  (Godel 1930; PRESUMED)

**Breaks on**
- *PRESUMED* — N and R not first-order characterizable (Lowenheim-Skolem both directions)  (Lowenheim 1915, Skolem 1920; PRESUMED — about infinite models by nature)

**Useful for:** non-standard analysis · algebraic axiomatics · database theory

### 70 · Reverse Mathematics (Big Five) (`REVERSE_MATH`)
*Friedman (1975); Simpson (1999)*

| | |
|---|---|
| **V** | subsystems of second-order arithmetic |
| **G** | proving the AXIOM back from the THEOREM over RCA_0 |
| **θ** | the five calibration marks RCA_0 < WKL_0 < ACA_0 < ATR_0 < Pi11-CA_0 |

Theorems priced by the set-existence they secretly demand — and almost all of classical analysis lands on one of just five rungs. The methodology is this library's own discipline applied to mathematics itself, which is why it is cataloged even though every claim here is PRESUMED: reversals are meta-proofs no instance can exhibit.

**Forces**
- *PRESUMED* — the Big Five phenomenon; WKL_0 = Heine-Borel = Brouwer fixed point (over RCA_0)  (Simpson, SOSOA 1999; PRESUMED)

**Breaks on**
- *PRESUMED* — Ramsey for pairs falls strictly between the rungs  (Seetapun-Slaman 1995, Liu 2012; PRESUMED)

**Useful for:** axiom calibration · computable mathematics · philosophy of proof

### 71 · Monads (Effects as Structure) (`MONADS`)
*Mac Lane (1971); Moggi (1991); Wadler (1992)*

| | |
|---|---|
| **V** | endofunctors with return and join |
| **G** | Kleisli composition |
| **θ** | the three monad laws |

Side effects packaged as algebra: return injects purity, bind sequences effects, and the three laws are exactly monoid laws one level up. The library enumerates them for Maybe and List — the laws your code must satisfy or your refactorings lie.

**Forces**
- **FORCED** `category_monad_laws` — left identity, right identity, associativity — Maybe and List, complete enumeration over the test domain
  - *Maybe and List monads: left identity, right identity, and associativity decided by complete enumeration over a 3-value domain and sampled Kleisli arrows — the monoid laws, executed*

**Breaks on**
- *PRESUMED* — monads do not compose without a distributive law  (Beck 1969; PRESUMED)

**Useful for:** Haskell effects · denotational semantics · query languages

### 72 · Petri Nets (Token Flow) (`PETRI`)
*Carl Adam Petri (1962)*

| | |
|---|---|
| **V** | markings of a place/transition net |
| **G** | local firing; reachability |
| **θ** | place invariants — conservation laws |

Concurrency without a clock: transitions fire on local sufficiency, conflicts are shared hunger, and a place invariant is a conservation law the net cannot break — verified here across the ENTIRE reachable state space.

**Forces**
- **FORCED** `petri_invariant_conservation` — x.C = 0 invariant; token count conserved across all reachable markings by exhaustive BFS; no deadlock in this net
  - *place-invariant x=(1,1): x.C = 0; token count 3 conserved across ALL 4 reachable markings (exhaustive BFS); every reachable marking enables a transition — no deadlock in this net*

**Breaks on**
- *PRESUMED* — reachability decidable but expensive (EXPSPACE-hard); inhibitor arcs buy Turing power and lose decidability  (Mayr 1981; Lipton 1976; PRESUMED)

**Useful for:** workflow engines · metabolic networks · async hardware

### 84 · Program-Variant Optimisation (The Living Map) (`LIVING_MAP`)
*paudit.py (2026); Young (1950); Ostrowski (1954)*

| | |
|---|---|
| **V** | programs up to contract equivalence on a probe set |
| **G** | contract-preserving transforms; relaxation-parameter choice |
| **θ** | the budget and the contract |

Optimisation as propagation: descend the load without leaving the contract class, and let theta refuse every cheaper variant that breaks a bridge. The gate runs live here — a closed form accepted for keeping the contract and dropping the load, a subtly wrong variant refused — and the solver's coherence wall at omega = 2 is measured as divergence, not slowness.

**Forces**
- **FORCED** `program_variant_contract_gate` — the accept/refuse gate on a live instance: contract kept + load dropped = accepted; contract broken = refused
  - *the campaign gate on a live instance: closed-form variant keeps the contract on all probes AND drops the load (20 vs 78 ops) — accepted; the broken variant leaves the contract class — refused. The pro*
- **EMPIRICAL** `sor_coherence_boundary` — SOR converges inside the wall, decoheres beyond it (omega 1.5 vs 2.1 on an SPD system)
  - *SOR on an SPD tridiagonal system: omega=1.5 converges to the direct solution (1e-6); omega=2.1 diverges — Ostrowski's coherence wall at omega=2, measured as decoherence, not slowness*

**Breaks on**
- *STIPULATED* — a finite probe set is not semantic equivalence — the contract is STIPULATED on every accept  (declared by the carrier itself, as the source PDF does)
- *PRESUMED* — gated local speedups do not compose to global optimality  (Amdahl + the moving critical path; structural)

**Useful for:** compiler passes with receipts · solver tuning · regression-safe refactoring · critical-path analysis


## Physics — 4 carriers

### 51 · DRAS Scale Carrier (Renormalization Group) (`DRAS_SCALE`)
*Wilson (1971); Callan-Symanzik; DRAS formalism (Pugmire 2026)*

| | |
|---|---|
| **V** | (coupling, scale, load) |
| **G** | running of the coupling with ln E; beta function |
| **θ** | the Landau pole — load diverges as the denominator dies |

Couplings are functions of the zoom level. The one-loop running composes as an exact group in ln E, shrinking couplings are asymptotically free, and the growing branch hits its pole precisely where the algebra says it must — decoherence as divergence, measured.

**Forces**
- **FORCED** `dras_scale_group_law` — group law in ln E exact to 1e-12; asymptotic-freedom direction confirmed; pole located and hit
  - *one-loop running composes exactly as a group in ln E (0.4 then 0.6 = 1.0, to 1e-12); growing-coupling branch blows up at the predicted pole ln E = 1/(beta v0) = 6.67 (value x1000 just below it); shrin*

**Breaks on**
- *PRESUMED* — Landau pole in QED/phi^4 signals breakdown, not physics  (Landau 1955; triviality results; PRESUMED beyond the toy)

**Useful for:** QCD asymptotic freedom · critical phenomena · effective field theory

### 52 · Thermodynamic Carrier (Entropy / Landauer) (`THERMO`)
*Carnot (1824); Clausius; Boltzmann; Landauer (1961); Berut (2012)*

| | |
|---|---|
| **V** | (S, E, N, V) or phase-space distributions |
| **G** | Hamiltonian flow; entropy ascent; bit erasure |
| **θ** | k_B T — and k_B T ln 2 per erased bit |

Information is physical: forgetting one bit costs at least kT ln 2 of heat, which is Maxwell's demon's invoice. The measurable core of the second law — relative entropy to equilibrium never increasing — is verified here at every step of every random chain tried.

**Forces**
- **EMPIRICAL** `landauer_and_h_theorem` — Landauer bill at 300K = 2.87e-21 J, exact arithmetic; Markov H-theorem held at every step, 30 random chains
  - *kT ln2 at 300K = 2.87e-21 J per erased bit (the arithmetic, exact); relative entropy to stationarity was non-increasing at EVERY step of 25 steps x 30 random 4-state Markov chains — the H-theorem, mea*

**Breaks on**
- *PRESUMED* — local entropy dips in small systems (fluctuation theorems)  (Evans-Searles; Jarzynski; PRESUMED)

**Useful for:** thermodynamics of computation · demon exorcism · energy floors for AI

### 53 · General Relativity (Manifold Carrier) (`GR`)
*Einstein (1915); Riemann (1854)*

| | |
|---|---|
| **V** | Lorentzian manifolds with metric g |
| **G** | covariant derivative; Einstein equations G = 8 pi T |
| **θ** | curvature scale; singularities where it diverges |

Gravity as geometry: free fall is a straight line in a curved book-keeping. The daily-life number is computed here — GPS clocks gain ~38 microseconds a day from the weak-field arithmetic, or the map drifts kilometers.

**Forces**
- **FORCED** `gr_gps_time_dilation` — GPS time dilation: +45.7 gravitational, -7.2 velocity, net ~38.5 us/day from the weak-field formulas
  - *weak-field GR arithmetic: gravitational +45.7 us/day, velocity -7.2 us/day, net +38.5 us/day — the ~38 us/day GPS must correct or drift ~11 km/day; field equations themselves PRESUMED (Einstein 1915)*
- *PRESUMED* — Bianchi identity = energy-momentum conservation  (Einstein 1915; differential-geometric identity; PRESUMED)

**Breaks on**
- *PRESUMED* — singularities: the theory predicts its own edge  (Penrose 1965, Hawking; PRESUMED)
- *PRESUMED* — incompatible with QM at the Planck scale  (the open problem of quantum gravity; PRESUMED)

**Useful for:** GPS corrections · black holes · LIGO · cosmology

### 54 · Quantum Field Theory (Fock Space) (`QFT`)
*Dirac (1927); Feynman, Schwinger, Tomonaga (1940s)*

| | |
|---|---|
| **V** | Fock space — superpositions of any particle number |
| **G** | creation/annihilation; path integral; renormalization group |
| **θ** | UV cutoff; renormalizability as finite load per order |

Particles as excitations of fields. The free-field engine is Wick's theorem — correlators are sums over pairings — and the library computes its smallest instances exactly: E[x^4] = 3 sigma^4 because three is the number of pairings, symbolically, combinatorially, and by Monte Carlo.

**Forces**
- **FORCED** `qft_wick_gaussian` — Wick on the Gaussian: 4th and 6th moments match the (2n-1)!! pairing count, symbolic + MC
  - *Wick on the Gaussian: E[x^4]=3 sigma^4 and E[x^6]=15 sigma^6 integrated symbolically, exactly matching the (2n-1)!! pairing count, cross-checked by Monte Carlo to 2% — free-field correlators are pairi*

**Breaks on**
- *PRESUMED* — loop divergences need renormalization; gravity is non-renormalizable  ('t Hooft-Veltman; PRESUMED)

**Useful for:** the Standard Model · QED precision · BCS theory


## Probability & Evidence — 6 carriers

### 73 · Kolmogorov Probability Theory (`KOLMOGOROV`)
*Kolmogorov (1933)*

| | |
|---|---|
| **V** | probability spaces (Omega, F, P) |
| **G** | conditioning; expectation; independence |
| **θ** | P(Omega)=1 and sigma-additivity — the whole axiom bill |

Probability as measure: two axioms, and Bayes, total probability, and monotonicity fall out as arithmetic — verified here on fifty random finite spaces where nothing extra could hide.

**Forces**
- **FORCED** `kolmogorov_axioms_to_bayes` — Bayes, total probability, monotonicity as pure arithmetic of the measure — 50 random spaces
  - *on 50 random finite probability spaces: Bayes' identity, the law of total probability, and monotonicity all reduce to arithmetic of the measure — no new axiom needed beyond additivity and P(Omega)=1 (*

**Breaks on**
- *PRESUMED* — conditioning on measure-zero events undefined without regular versions  (Kolmogorov 1933; standard)
- *PRESUMED* — one measure cannot express ignorance — see the imprecise carrier  (motivating Walley 1991)

**Useful for:** statistics · stochastic processes · finance

### 74 · Bayesian Probability (Prior-Posterior) (`BAYES`)
*Bayes (1763); Laplace (1812); de Finetti (1937)*

| | |
|---|---|
| **V** | coherent degrees of belief over hypotheses |
| **G** | Bayes updating; Jeffrey conditionalization |
| **θ** | coherence — or a Dutch book exists |

Belief with a solvency requirement: incoherent credences are a purchasable loss, and the library constructs the purchase. Sequential and joint updating provably coincide — run on thirty random cases — so evidence order cannot be gamed.

**Forces**
- **FORCED** `bayes_sequential_and_dutch_book` — sequential = joint updating on 30 random cases; the Dutch book against P(A)=P(~A)=0.6 constructed: +0.20 guaranteed
  - *sequential updating equals joint updating on 30 random cases (conditional independence given H); and the Dutch book is constructed: prices P(A)=P(~A)=0.6 hand the bookie a guaranteed +0.20 per unit st*
- *PRESUMED* — posteriors converge to the truth (Bernstein-von Mises)  (regularity conditions apply; PRESUMED)

**Breaks on**
- *PRESUMED* — prior sensitivity with scarce data; no universal uninformative prior  (Jeffreys, Bernardo; standard)

**Useful for:** ML · diagnosis · A/B testing · spam filtering

### 75 · Dempster-Shafer Evidence Theory (`DEMPSTER_SHAFER`)
*Dempster (1967); Shafer (1976)*

| | |
|---|---|
| **V** | basic probability assignments over SETS of hypotheses |
| **G** | Dempster's combination rule, normalizing conflict away |
| **θ** | the belief-plausibility interval |

Ignorance finally distinguishable from uniform uncertainty: mass on a set means 'one of these, cannot say which'. The famous failure is computed exactly — two doctors 99% sure of DIFFERENT diseases combine to certainty in the one neither believed.

**Forces**
- **FORCED** `dempster_shafer_zadeh` — Bel <= Pl; vacuous BPA yields [0,1]; classical probability recovered on singletons
  - *Zadeh's paradox computed exactly: two sources 99% sure of DIFFERENT diagnoses combine to 100% certainty in the tumor NEITHER believed (conflict K=0.9998 normalized away); Bel<=Pl verified; the vacuous*

**Breaks on**
- **FORCED** `dempster_shafer_zadeh` — Zadeh's paradox computed: 0.99/0.99 conflict normalizes to 100% tumor
  - *Zadeh's paradox computed exactly: two sources 99% sure of DIFFERENT diagnoses combine to 100% certainty in the tumor NEITHER believed (conflict K=0.9998 normalized away); Bel<=Pl verified; the vacuous*
- *PRESUMED* — independence of sources assumed by the rule  (Shafer 1976; standard caveat)

**Useful for:** sensor fusion · expert systems · forensic combination

### 76 · Possibility Theory (Zadeh/Dubois-Prade) (`POSSIBILITY`)
*Zadeh (1978); Dubois & Prade (1988)*

| | |
|---|---|
| **V** | possibility distributions, sup-normalized |
| **G** | Pi maxitive over unions; necessity by duality |
| **θ** | normalization: something is fully possible |

Additivity swapped for max: the possibility of a union is its best member, so A and not-A can both be fully possible at once — which is exactly what not-knowing looks like, and what a probability measure cannot say.

**Forces**
- **FORCED** `possibility_maxitive` — maxitivity enumerated; N(A) = 1 - Pi(~A) duality; the vacuous distribution expresses ignorance
  - *Pi(A u B) = max — enumerated; N(A) = 1 - Pi(~A) duality holds; under the vacuous distribution both A and ~A carry possibility 1 simultaneously — the additivity axiom is the thing removed, and ignoranc*

**Breaks on**
- *PRESUMED* — probability-possibility transforms are not unique  (Dubois-Prade-Sandri 1993; PRESUMED)

**Useful for:** fuzzy control · linguistic vagueness · deep-uncertainty risk

### 77 · Imprecise Probability (Credal Sets) (`IMPRECISE`)
*Walley (1991); Kuznetsov (1991)*

| | |
|---|---|
| **V** | convex sets of probability measures |
| **G** | robust Bayes: update every member; natural extension |
| **θ** | the credal set — singleton means classical, everything means ignorance |

When the model itself is uncertain, carry the whole set. The library constructs the theory's most counterintuitive honest moment: DILATION, where observing evidence widens the interval from a point to [0.2, 0.8] — learning that you know less than you thought.

**Forces**
- **FORCED** `imprecise_credal_dilation` — conjugacy P_*(A) + P^*(~A) = 1; dilation constructed and exhibited
  - *dilation constructed: prior interval for X is [0.50,0.50] (a point), posterior after observing Y=0 is [0.20,0.80] — conditioning WIDENED the interval; evidence can honestly increase imprecision, which*

**Breaks on**
- *PRESUMED* — decision theory goes set-valued; inference can be NP-hard in extreme points  (Walley 1991; de Campos et al.; PRESUMED)

**Useful for:** robust statistics · credal networks · sensitivity analysis

### 85 · Distinction Cost (The Boundary Law) (`BOUNDARY_LAW`)
*distinction.py (2026); Chernoff/Hoeffding; Shannon (1948)*

| | |
|---|---|
| **V** | pairs of hypotheses separated by a gap, under noise |
| **G** | repeated noisy probing; redundancy against error |
| **θ** | confidence 1 - delta |

What a distinction costs to maintain: not the distance between the values but the looks needed to be sure, which scales as 1/gap^2. The near-boundary call is the expensive one — the medical test at threshold, the speed camera at the limit — and the library measures the exponent.

**Forces**
- **EMPIRICAL** `boundary_law_scaling` — sample count scales as 1/gap^2 (log-log slope ~2 across a gap halving) and lands the formula's order of magnitude
  - *halving the gap multiplied the required sample count by ~4 (log-log slopes ['2.4', '1.9'] vs exponent 2); measured n=175 at gap=0.2 vs formula 461 — same order. The near-boundary distinction is the ex*

**Breaks on**
- *STIPULATED* — exponents are per-system in native load units; universality NOT claimed  (declared by the source carrier itself)
- *PRESUMED* — Gaussian noise modeled; heavy tails can change the exponent  (stated scope)

**Useful for:** sample-size planning · code-redundancy design · A/B tests near a decision boundary · bandit exploration


## Measurement Interpretations — 6 carriers

### 78 · Copenhagen Interpretation (`COPENHAGEN`)
*Bohr (1927); Heisenberg (1927)*

| | |
|---|---|
| **V** | quantum state before, classical outcome after; nothing between |
| **G** | unitary evolution, then primitive projective collapse |
| **θ** | the Heisenberg cut — deliberately unspecified |

Quantum mechanics as a theory of measurement outcomes, with the between-times question ruled out of order. It runs the lab perfectly and declines the ontology on principle.

**Forces**
- **FORCED** `born_rule_shared_instance` — the Born statistics — the shared empirical core, computed exactly on the qubit instance
  - *the shared empirical core computed: P(0) = cos^2(0.3) = 0.9127, probabilities sum to 1 — every interpretation in this section reproduces exactly this table, which is WHY experiment has not separated t*
- *PRESUMED* — complementarity: conjugate observables never jointly definite  (Bohr 1928; PRESUMED)

**Breaks on**
- *PRESUMED* — no mechanism or location for the cut (the measurement problem)  (Bell, 'Against Measurement' 1990; PRESUMED)
- *PRESUMED* — macroscopic superpositions undefined (the cat)  (Schrodinger 1935; PRESUMED)

**Useful for:** working-physicist default · state prep and readout · spectroscopy

### 79 · Many-Worlds Interpretation (Everett) (`MWI`)
*Everett (1957); DeWitt (1970)*

| | |
|---|---|
| **V** | one universal wavefunction; branches via decoherence |
| **G** | unitary evolution ONLY — measurement is entanglement |
| **θ** | decoherence time — when branches stop interfering |

Delete the collapse postulate and keep the books: measurement entangles, decoherence separates, every outcome persists in its branch. The library runs the bookkeeping — norm exactly preserved, Born weights intact on both branches, nothing collapsed.

**Forces**
- **FORCED** `mwi_unitarity_no_collapse` — premeasurement as a unitary: norm preserved, both outcomes persist with cos^2/sin^2 weights
  - *premeasurement as a unitary: the norm is exactly preserved, both outcomes persist as orthogonal branches with Born weights cos^2/sin^2, nothing collapsed — the bookkeeping MWI runs on, executed; the B*
- **FORCED** `born_rule_shared_instance` — shared Born statistics
  - *the shared empirical core computed: P(0) = cos^2(0.3) = 0.9127, probabilities sum to 1 — every interpretation in this section reproduces exactly this table, which is WHY experiment has not separated t*

**Breaks on**
- *PRESUMED* — the Born rule must be DERIVED, and the derivations (Deutsch-Wallace, envariance) remain contested  (Wallace 2012; Adlam and critics; PRESUMED)
- *PRESUMED* — branch structure only approximate  (Zurek pointer bases; PRESUMED)

**Useful for:** quantum cosmology · decoherence theory · entanglement without collapse

### 80 · Pilot Wave Theory (de Broglie-Bohm) (`BOHM`)
*de Broglie (1927); Bohm (1952)*

| | |
|---|---|
| **V** | wavefunction PLUS actual particle positions |
| **G** | Schrodinger for the wave; the guiding equation for the particles |
| **θ** | quantum equilibrium: initial rho = |psi|^2 |

Determinism restored by doubling the ontology: the wave guides, the particles ride, and Born statistics follow from an equilibrium hypothesis the dynamics preserves. Collapse becomes mere selection of the occupied branch.

**Forces**
- **FORCED** `born_rule_shared_instance` — shared Born statistics (given quantum equilibrium)
  - *the shared empirical core computed: P(0) = cos^2(0.3) = 0.9127, probabilities sum to 1 — every interpretation in this section reproduces exactly this table, which is WHY experiment has not separated t*
- *PRESUMED* — equivariance: rho = |psi|^2 preserved for all time  (Bohm 1952; Durr-Goldstein-Zanghi 1992; PRESUMED)

**Breaks on**
- *PRESUMED* — explicit nonlocality; a preferred foliation in tension with relativity  (Bell's theorem makes the nonlocality mandatory; PRESUMED)
- *PRESUMED* — empty branches persist as real  (Bohm 1952; the ontological bill)

**Useful for:** EPR/Bell analysis with a mechanism · quantum trajectories intuition

### 81 · Consistent Histories (`HISTORIES`)
*Griffiths (1984); Gell-Mann & Hartle (1990); Omnes (1992)*

| | |
|---|---|
| **V** | families of projector sequences (histories) |
| **G** | the decoherence functional; probabilities inside consistent families |
| **θ** | consistency: off-diagonal decoherence functional = 0 |

Probability without observers: a family of histories earns classical probability exactly when its interference terms vanish. The library computes a full 16-pair decoherence functional and watches the condition hold and the probabilities turn Kolmogorov.

**Forces**
- **FORCED** `consistent_histories_qubit` — off-diagonals exactly zero for the same-basis qubit family; diagonal probabilities additive and Born
  - *the decoherence functional computed for all 16 history pairs: off-diagonals exactly zero (a consistent family), diagonal probabilities Kolmogorov-additive and matching Born — classical reasoning valid*

**Breaks on**
- *PRESUMED* — no rule selects among incompatible consistent frameworks; cross-framework inference forbidden  (Griffiths' single-framework rule; Dowker-Kent 1996; PRESUMED)

**Useful for:** closed-system QM · quantum cosmology · decoherence analysis

### 82 · Objective Collapse (GRW / Penrose OR) (`GRW`)
*Ghirardi-Rimini-Weber (1986); Penrose (1989)*

| | |
|---|---|
| **V** | wavefunctions subject to spontaneous stochastic localization |
| **G** | Schrodinger plus random Gaussian hits at rate lambda per particle |
| **θ** | lambda ~ 1e-16 /s and width ~ 1e-7 m — tuned so micro stays quantum and macro snaps |

Make collapse physics: one tiny per-particle rate, amplified by particle count. A dust grain's superposition dies in microseconds while an electron's lives for eons — and the N-scaling of survival is exactly what the library simulates.

**Forces**
- **EMPIRICAL** `grw_rate_scaling` — first-hit survival scales as 1/(N lambda) across a 1000x range of N
  - *simulated first-hit lifetimes: mean survival scales as 1/(N lambda) across N=1 vs N=1000 to within 8% — micro coherence with macro collapse from ONE stochastic rate; that nature actually runs this mod*
- **FORCED** `born_rule_shared_instance` — shared Born statistics FAPP
  - *the shared empirical core computed: P(0) = cos^2(0.3) = 0.9127, probabilities sum to 1 — every interpretation in this section reproduces exactly this table, which is WHY experiment has not separated t*

**Breaks on**
- *PRESUMED* — slight energy non-conservation per hit; no complete relativistic version; no experimental discrimination yet  (GRW 1986; CSL literature; ongoing optomechanics tests; PRESUMED and honestly undecided)

**Useful for:** mesoscopic superposition experiments · measurement-problem dissolution proposals

### 83 · Relational Quantum Mechanics (Rovelli) (`RELATIONAL`)
*Rovelli (1996)*

| | |
|---|---|
| **V** | states defined only RELATIVE to an observing system |
| **G** | interactions actualize relative facts |
| **θ** | the interaction event |

Special relativity's move replayed on the quantum state: no observer-independent state, only relations. Wigner and his friend stop contradicting each other because their descriptions were never required to be one description.

**Forces**
- **FORCED** `born_rule_shared_instance` — shared Born statistics within each observer's account
  - *the shared empirical core computed: P(0) = cos^2(0.3) = 0.9127, probabilities sum to 1 — every interpretation in this section reproduces exactly this table, which is WHY experiment has not separated t*
- *PRESUMED* — internal consistency of each perspective  (Rovelli 1996; PRESUMED)

**Breaks on**
- *PRESUMED* — cross-perspective facts require care; correlations taken as primitive  (Frauchiger-Renner adjacent debates; PRESUMED)

**Useful for:** loop quantum gravity · quantum reference frames · Bell without absolutes

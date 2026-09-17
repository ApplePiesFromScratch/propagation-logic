"""carriers.propositional — 14 carriers. Claims cite checks or sources."""

CARRIERS = [
 dict(id=1, key="CL2", name="Classical Logic",
  origin="Aristotle (384 BC); Frege (1879); Whitehead & Russell (1910)",
  V="{0,1} — exactly two truth values",
  G="NOT v=1-v; AND=product/min; OR=max; IMP(a,b)=max(1-a,b)",
  theta="1.0 — only full truth designated",
  insight=("Demanding an involutive NOT with no fixed point forces V={0,1} "
           "uniquely; LNC and LEM then follow by arithmetic — consequences "
           "of the carrier, not axioms. Complete commitment on every "
           "proposition, no gradations without information loss."),
  forces=[
   dict(claim="All 15 classical laws hold, by complete enumeration",
        check="cl2_signature"),
   dict(claim="Ex falso: AND(v,NOT v)=0, so OR(0,Q)=Q for any Q",
        check="cl2_ex_falso")],
  breaks=[
   dict(claim="No fixed point for NOT — the Liar is unrepresentable",
        check="cl2_no_fixed_point"),
   dict(claim="No gradations: v=0.5 cannot be represented",
        cite="by definition of V; see fuzzy carriers for the repair")],
  useful_for=["classical mathematics", "digital circuits", "SAT solvers",
              "SQL boolean logic"]),

 dict(id=2, key="L3", name="Lukasiewicz Three-Valued Logic (L3)",
  origin="Jan Lukasiewicz (1920), O logice trojwartosciowej",
  V="{0, 1/2, 1} — false, indeterminate, true",
  G="NOT v=1-v; AND(a,b)=max(0,a+b-1); OR=min(1,a+b); IMP=min(1,1-a+b)",
  theta="1.0 — only 1 designated",
  insight=("The midpoint is negation's first fixed point — the Liar "
           "settles at 1/2 instead of oscillating. The strong t-norm "
           "makes truth expensive: a+b must EXCEED 1 before AND pays "
           "anything, so LNC and LEM survive the third value."),
  forces=[
   dict(claim="LNC and LEM both hold at every value; DN holds",
        check="l3_signature"),
   dict(claim="NOT(1/2)=1/2 — the Liar's stable home", check="l3_fixed_point")],
  breaks=[
   dict(claim="AND(1/2,1/2)=0 — two half-truths produce no truth",
        check="l3_two_halves"),
   dict(claim="LEM fails if 1/2 is also designated",
        cite="immediate from OR(1/2,1/2)=1: designation choice, see LP")],
  useful_for=["truth-gap logics", "self-reference analysis",
              "three-valued NULL semantics (partial)"]),

 dict(id=3, key="K3", name="Kleene Strong Three-Valued Logic (K3)",
  origin="Stephen Kleene (1952), Introduction to Metamathematics",
  V="{0, 1/2, 1} — false, undefined, true",
  G="NOT v=1-v; AND=min; OR=max; IMP(a,b)=max(1-a,b)",
  theta="1.0 — only 1 designated",
  insight=("Same values as L3, lattice operators instead: 1/2 becomes a "
           "propagating taint — a computation that has not returned, "
           "contaminating everything it touches. Both source documents "
           "are honored: LNC holds under the designation reading (kernel "
           "parity, 14/15 lone-LEM signature) and fails under the value "
           "reading AND(1/2,NOT 1/2)=1/2 != 0 — the enumerator decides "
           "both, and the discrepancy is surfaced, not hidden."),
  forces=[
   dict(claim="All lattice laws; DN; 14/15 signature with LEM the lone "
              "sacrifice (designation reading), value-reading LNC "
              "failure also exhibited", check="k3_signature"),
   dict(claim="1/2 taints every AND below truth and every OR above "
              "falsehood", check="k3_taint")],
  breaks=[
   dict(claim="LEM fails: OR(1/2,NOT 1/2)=1/2, not designated",
        check="k3_signature")],
  useful_for=["partial function semantics", "SQL NULL (strong reading)",
              "partial evaluation"]),

 dict(id=4, key="WK3", name="Kleene Weak Three-Valued Logic",
  origin="Stephen Kleene (1952), weak tables variant",
  V="{0, u, 1} — u = undefined, absorbing",
  G="NOT(u)=u; AND(u,x)=u and OR(u,x)=u unconditionally; classical on {0,1}",
  theta="1.0 — u blocks all inference through it",
  insight=("Weak K3 bans short-circuiting: a known 0 cannot rescue an "
           "AND, a known 1 cannot rescue an OR. Every subexpression must "
           "resolve — strict call-by-value, encoded in the tables."),
  forces=[
   dict(claim="u absorbs both operations regardless of the other "
              "argument; classical on {0,1}", check="wk3_absorbs")],
  breaks=[
   dict(claim="AND(u,0)=u where strong K3 gives 0; OR(u,1)=u where "
              "strong gives 1 — the rescue is forbidden",
        check="wk3_absorbs"),
   dict(claim="LNC and LEM both fail at u", cite="direct from absorption")],
  useful_for=["strict evaluation semantics", "call-by-value models",
              "error propagation"]),

 dict(id=5, key="B3", name="Bochvar External Three-Valued Logic (B3)",
  origin="Dmitri Bochvar (1938)",
  V="{0, m, 1} — m = meaningless/paradoxical",
  G="internal: m absorbs; external assertion E(1)=1, E(0)=E(m)=0",
  theta="1.0 externally; m quarantined internally",
  insight=("Two tiers: internally m infects every formula it touches "
           "(paradox contained, not resolved); the external operator "
           "then collapses m to 0, restoring classical decidability for "
           "sound formulas. Quarantine plus discharge."),
  forces=[
   dict(claim="m absorbs internally; E collapses m to 0 and preserves "
              "classical values", check="b3_external_collapse")],
  breaks=[
   dict(claim="no internal LNC/LEM for m-valued formulas",
        cite="direct from absorption tables")],
  useful_for=["paradox containment", "partial information",
              "undefined-value semantics"]),

 dict(id=6, key="LP", name="Paraconsistent Logic LP (Priest)",
  origin="Graham Priest (1979), The Logic of Paradox",
  V="{0, B, 1}; B = both, arithmetically 1/2",
  G="NOT v=1-v; AND=min; OR=max; DESIGNATED = {B, 1}",
  theta="designation includes the glut",
  insight=("K3's tables with the middle value designated: contradictions "
           "become usable premises. Explosion is blocked by arithmetic — "
           "min cannot amplify B above B, so a glut never forces an "
           "arbitrary Q. The price is detachment: modus ponens fails."),
  forces=[
   dict(claim="LEM holds; LNC fails; MP fails — the paraconsistent "
              "trade, enumerated", check="lp_signature"),
   dict(claim="ex falso blocked: countermodel with designated glut and "
              "undesignated Q", check="lp_no_explosion")],
  breaks=[
   dict(claim="LNC: AND(B,NOT B)=B, designated", check="lp_signature")],
  useful_for=["dialethism", "inconsistent databases",
              "naive set theory without explosion"]),

 dict(id=7, key="FUZZY_PROD", name="Fuzzy Logic (Zadeh / product t-norm)",
  origin="Lotfi Zadeh (1965), Fuzzy Sets",
  V="[0,1] continuous",
  G="NOT v=1-v; AND=a*b; OR=max; Goguen IMP",
  theta="1.0",
  insight=("Continuum truth with multiplicative AND: conjunction always "
           "weakens in the interior (half times half is a quarter). LNC "
           "and LEM both leak at 0.5 — partial truth conjoined with "
           "partial falsehood is not nothing."),
  forces=[
   dict(claim="a*b <= min(a,b) (AND weakens); IMP(a,a)=1",
        check="fuzzy_product_failures")],
  breaks=[
   dict(claim="LNC gives 0.25 at v=0.5; LEM gives 0.5 — witnesses "
              "exhibited", check="fuzzy_product_failures"),
   dict(claim="IMP(0,b) needs a convention", cite="Goguen residuum")],
  useful_for=["fuzzy control", "approximate reasoning",
              "soft constraints"]),

 dict(id=8, key="FUZZY_LUK", name="Fuzzy Logic (Lukasiewicz / MV)",
  origin="Lukasiewicz (1930); Chang (1958) MV-algebras",
  V="[0,1] — metric completion of the finite L_n chain",
  G="NOT v=1-v; AND=max(0,a+b-1); OR=min(1,a+b); IMP=min(1,1-a+b)",
  theta="1.0",
  insight=("The unique continuous t-norm that keeps BOTH LNC and LEM on "
           "the whole interval: v+(1-v)-1=0 and v+(1-v)=1 identically. "
           "Classical law-keeping extended to a continuum, at the price "
           "of idempotence."),
  forces=[
   dict(claim="LNC and LEM hold at every point of [0,1], exactly",
        check="fuzzy_luk_both_laws")],
  breaks=[
   dict(claim="uniqueness among continuous t-norms",
        cite="Mostert-Shields classification; PRESUMED here")],
  useful_for=["MV-algebras", "fuzzy arithmetic", "probability logic"]),

 dict(id=9, key="FUZZY_GODEL", name="Fuzzy Logic (Godel / min t-norm)",
  origin="Godel (1932); Dummett (1959) LC",
  V="[0,1] linearly ordered",
  G="NOT(v)=1 if v=0 else 0; AND=min; OR=max; IMP crisp residuum",
  theta="1.0",
  insight=("Negation is a cliff: every positive value negates to 0, so "
           "gradient information dies under NOT while AND/OR stay "
           "graded. Comparison logic — 'at least as true as' — with a "
           "binary trapdoor."),
  forces=[
   dict(claim="min idempotent; lattice laws throughout",
        cite="lattice identities on a chain; instance enumerated in "
             "heyting_open_sets and the 3-chain checks")],
  breaks=[
   dict(claim="NOT discontinuous (0.01 -> 0); DN fails; LEM fails at "
              "interior values — witnesses exhibited",
        check="fuzzy_godel_failures")],
  useful_for=["intermediate logics", "graded comparison",
              "ordering semantics"]),

 dict(id=10, key="INT", name="Intuitionistic Logic (BHK)",
  origin="Brouwer (1908); Heyting (1930); Kolmogorov (1932)",
  V="{0,1} but reachable only by explicit construction",
  G="OR needs a witness; IMP is a proof transformer; NOT P = P -> false",
  theta="1.0 — truth is possession of a proof",
  insight=("Same two values, different access rules: asserting P OR Q "
           "without a witness is not an operation. LEM is arithmetically "
           "sound but constructively unpurchasable for undecided P; "
           "refutation-of-refutation does not construct."),
  forces=[
   dict(claim="LNC and DN-introduction hold; countermodel machinery "
              "confirms what survives", check="intuitionistic_countermodels")],
  breaks=[
   dict(claim="LEM and DN-elimination fail: 3-chain Heyting "
              "countermodel, witness 1/2", check="intuitionistic_countermodels"),
   dict(claim="disjunction property (a proof of P OR Q yields a proof "
              "of one)", cite="Godel-Gentzen; PRESUMED — proof-theoretic")],
  useful_for=["constructive mathematics", "Coq/Agda/Lean",
              "Curry-Howard"]),

 dict(id=11, key="LINEAR", name="Linear Logic",
  origin="Jean-Yves Girard (1987)",
  V="formulas as resources, used exactly once unless marked !",
  G="tensor (both), additive AND (choose), -o (consume to produce), ! (unlimited)",
  theta="exact resource count",
  insight=("Structural rules made purchasable: without !, you may "
           "neither copy a hypothesis (contraction) nor discard one "
           "(weakening). Proofs become conservation ledgers — every use "
           "has a cost and every cost is tracked."),
  forces=[
   dict(claim="linear MP transfers the resource; ! restores classical "
              "structure", cite="Girard 1987, sequent calculus; PRESUMED"),
   dict(claim="contraction and weakening invalid in the counting model",
        check="linear_no_copy_no_discard")],
  breaks=[
   dict(claim="A |- A tensor A fails (1 != 2); A,B |- A discards paid "
              "B", check="linear_no_copy_no_discard")],
  useful_for=["resource-aware type theory", "Rust ownership semantics",
              "session types"]),

 dict(id=12, key="RELEVANCE", name="Relevance Logic (R, E)",
  origin="Ackermann (1956); Anderson & Belnap (1975)",
  V="{0,1} with a relevance filter on derivations",
  G="classical connectives; IMP valid only under variable sharing",
  theta="every premise must contribute a variable",
  insight=("Material implication's paradoxes die by a syntactic tax: "
           "P -> Q must share content. Inference must use its premises, "
           "not merely coexist with them."),
  forces=[
   dict(claim="A -> A shares trivially; sharing filter is decidable "
              "and enforced", check="relevance_sharing_filter")],
  breaks=[
   dict(claim="P -> (Q -> P) rejected: P and Q may share nothing",
        check="relevance_sharing_filter"),
   dict(claim="full R semantics (Routley-Meyer)",
        cite="Routley & Meyer 1973; PRESUMED")],
  useful_for=["conditional logic", "belief revision",
              "models of explanation"]),

 dict(id=13, key="DUAL_INT", name="Dual-Intuitionistic Logic (co-Heyting)",
  origin="Rauszer (1974); Goodman (1981)",
  V="co-Heyting algebras — closed sets where intuitionism has opens",
  G="subtraction A-B as the primitive; OR needs refutation evidence",
  theta="0.0 — a proposition fails only on explicit refutation",
  insight=("Every intuitionistic arrow reversed: refutations are the "
           "primitive certificates and default acceptance rules until a "
           "refutation lands. Where BHK asks 'can you prove it?', the "
           "dual asks 'can you refute its negation?'."),
  forces=[
   dict(claim="co-LEM holds on the dual chain: a OR ~a = 1 everywhere",
        check="dual_intuitionistic_chain")],
  breaks=[
   dict(claim="co-LNC fails: a AND ~a = 1/2 at the midpoint — the "
              "mirror image of intuitionism's LEM failure",
        check="dual_intuitionistic_chain")],
  useful_for=["default reasoning", "paracomplete duals",
              "over-approximation in abstract interpretation"]),

 dict(id=14, key="SUBSTRUCT", name="Substructural Logic (framework)",
  origin="Gentzen (1935); Dosen (1988); Restall (2000)",
  V="sequents; V depends on retained structural rules",
  G="connectives fixed; Weakening/Contraction/Exchange/Cut are dials",
  theta="which structural rules survive",
  insight=("Classical logic's four silent assumptions made explicit and "
           "individually removable: linear drops C, relevance drops W, "
           "Lambek drops E. Each removal is a real constraint — "
           "resources, relevance, word order — that classical proof "
           "ignores."),
  forces=[
   dict(claim="identity A |- A survives all removals",
        cite="Gentzen; immediate"),
   dict(claim="each dial is live: no-copy without C, order-sensitivity "
              "without E — demonstrated", check="substructural_dials")],
  breaks=[
   dict(claim="cut elimination in most substructural systems",
        cite="Gentzen Hauptsatz and descendants; PRESUMED")],
  useful_for=["type-theory foundations", "Lambek grammars",
              "resource-bounded computation"]),
]

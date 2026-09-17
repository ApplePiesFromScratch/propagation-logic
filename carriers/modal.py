"""carriers.modal — 8 Kripke-family carriers, axioms decided by
complete frame enumeration up to 3 worlds."""

CARRIERS = [
 dict(id=15, key="MODAL_K", name="Modal Logic K (Kripke base)",
  origin="C.I. Lewis (1918); Kripke (1959-63)",
  V="worlds W with accessibility R; NECS/POSS index truth over R-neighbors",
  G="NECS = universal over accessible worlds; POSS = existential; R unconstrained",
  theta="the accessibility relation itself",
  insight=("Necessity as universal quantification over R-neighbors, with "
           "R left free. Everything true here holds in EVERY modal logic; "
           "each constraint on R buys one more axiom, and the frames "
           "below pay for exactly what they claim."),
  forces=[
   dict(claim="K axiom, NEC/POS duality, NEC distributes over AND — at "
              "every world of every frame up to n=3", check="K_axiom_all_frames")],
  breaks=[
   dict(claim="T not forced: explicit non-reflexive countermodel",
        check="K_T_not_forced"),
   dict(claim="4 and 5 not forced without transitivity/symmetry",
        cite="countermodels analogous; see S4/S5 records")],
  useful_for=["temporal logic", "deontic logic", "provability logic",
              "knowledge representation"]),

 dict(id=16, key="MODAL_T", name="Modal Logic T (reflexive frames)",
  origin="Feys (1937); von Wright (1951)",
  V="Kripke frames with wRw for all w",
  G="K plus reflexivity",
  theta="self-accessibility",
  insight=("One constraint, one theorem: a world that sees itself makes "
           "NECS(P) include the here-and-now, so necessity implies "
           "actuality with no further machinery."),
  forces=[
   dict(claim="NECS(P) -> P forced on ALL reflexive frames; 4 still has "
              "a reflexive countermodel", check="T_from_reflexivity")],
  breaks=[
   dict(claim="4 and B not forced", check="T_from_reflexivity")],
  useful_for=["alethic modality", "truthful epistemic logic",
              "base for S4/S5"]),

 dict(id=17, key="MODAL_S4", name="Modal Logic S4 (preorder frames)",
  origin="Lewis & Langford (1932); Kripke semantics",
  V="frames where R is reflexive and transitive",
  G="T plus transitivity",
  theta="preorder accessibility",
  insight=("Transitivity makes necessity introspective: what is "
           "reachable from the reachable is already reachable, so "
           "NECS(P) is itself necessary. Knowing implies knowing that "
           "you know — but not knowing what you don't."),
  forces=[
   dict(claim="T and 4 forced on all preorders; 5 still fails on a "
              "preorder countermodel", check="S4_from_preorder")],
  breaks=[
   dict(claim="negative introspection absent", check="S4_from_preorder")],
  useful_for=["epistemic logic", "tense logic",
              "intuitionistic logic via Godel translation"]),

 dict(id=18, key="MODAL_S5", name="Modal Logic S5 (equivalence frames)",
  origin="Lewis (1932)",
  V="frames where R is an equivalence relation",
  G="S4 plus symmetry",
  theta="full mutual accessibility within classes",
  insight=("With R an equivalence, modality collapses to quantification "
           "over the class: possibility becomes stable (5 axiom) and all "
           "worlds in a class are modally interchangeable."),
  forces=[
   dict(claim="5 and B forced on ALL equivalence frames up to n=3",
        check="S5_from_equivalence")],
  breaks=[
   dict(claim="cross-class inference unavailable",
        cite="immediate from the partition structure")],
  useful_for=["metaphysical modality", "full-introspection epistemics"]),

 dict(id=19, key="MODAL_GL", name="Provability Logic GL (Godel-Lob)",
  origin="Lob (1955); Solovay (1976); Boolos (1979)",
  V="NECS(P) = 'PA proves P'; frames transitive + conversely well-founded",
  G="K + 4 + Lob axiom",
  theta="proof depth; well-foundedness of provability",
  insight=("Necessity as provability: Lob's axiom holds on exactly the "
           "transitive conversely-well-founded frames, and T FAILS — a "
           "system strong enough to encode itself cannot prove its own "
           "soundness. The finite frames below exhibit both facts."),
  forces=[
   dict(claim="Lob axiom forced on all transitive irreflexive frames "
              "up to n=3", check="GL_lob_on_finite_strict_orders")],
  breaks=[
   dict(claim="T fails on GL frames — provability does not imply truth "
              "inside the system", check="GL_lob_on_finite_strict_orders"),
   dict(claim="arithmetical completeness of GL for PA",
        cite="Solovay 1976; PRESUMED — needs arithmetic, not frames")],
  useful_for=["incompleteness analysis", "provability predicates",
              "self-reference limits"]),

 dict(id=20, key="EPISTEMIC", name="Epistemic Logic (multi-agent)",
  origin="Hintikka (1962); Fagin-Halpern-Moses-Vardi (1995)",
  V="worlds with per-agent indistinguishability relations R_i",
  G="K_i = universal over agent i's R; common knowledge = infinite closure",
  theta="epistemic indistinguishability per agent",
  insight=("Knowledge as truth across indistinguishable worlds. Common "
           "knowledge is the fixed point of 'everyone knows that' — "
           "unreachable by any finite message exchange, which is why "
           "coordinated attack fails and simultaneous broadcast exists."),
  forces=[
   dict(claim="K_i distributes over AND, both directions, every frame",
        check="epistemic_distribution")],
  breaks=[
   dict(claim="common knowledge not achievable by finite communication",
        cite="Halpern & Moses 1990, coordinated attack; PRESUMED — an "
             "impossibility over unbounded protocols")],
  useful_for=["distributed consensus", "game theory",
              "cryptographic protocol analysis"]),

 dict(id=21, key="TEMPORAL", name="Temporal Logic (LTL / CTL)",
  origin="Prior (1957); Pnueli (1977); Clarke & Emerson (1981)",
  V="time steps as worlds; linear traces (LTL) or trees (CTL)",
  G="X next, F eventually, G always, U until",
  theta="finite paths verify F; G outruns any finite observation",
  insight=("Modal logic pointed at time: F and G are POSS and NECS over "
           "the future. Under the finite-trace semantics this library "
           "STIPULATES (and says so), the classical dualities are "
           "decidable and decided."),
  forces=[
   dict(claim="F/G duality, FF=F, G(p)->p over ALL traces to length 5 "
              "(finite-trace semantics, a declared stipulation)",
        check="ltl_finite_trace_laws")],
  breaks=[
   dict(claim="G undecidable by finite observation on infinite traces",
        cite="definitional; the stipulation above is the honest boundary"),
   dict(claim="LTL and CTL incomparable in expressive power",
        cite="Clarke & Draghicescu 1988; PRESUMED")],
  useful_for=["model checking (SPIN, NuSMV)", "reactive specs",
              "liveness/safety verification"]),

 dict(id=22, key="DEONTIC", name="Deontic Logic",
  origin="von Wright (1951); Chisholm (1963)",
  V="worlds ranked by moral ideality; O/P/F over ideal worlds",
  G="O(P): P in all ideal accessible worlds; P(P): in some; F=O(NOT P)",
  theta="seriality — somewhere, an ideal world exists",
  insight=("Obligation as necessity over ideal worlds. The one theorem "
           "everyone wants — obligatory implies permitted — is priced "
           "exactly by seriality, and the frames show it: give a world "
           "no ideal neighbor and O(P) holds vacuously while P(P) dies."),
  forces=[
   dict(claim="O(P)->P(P) forced by seriality and ONLY by it — both "
              "directions exhibited on frames", check="deontic_O_implies_P")],
  breaks=[
   dict(claim="contrary-to-duty (Chisholm) paradoxes: violated "
              "obligations point at mutually inconsistent ideals",
        cite="Chisholm 1963; PRESUMED — a modeling inadequacy, not a "
             "frame fact")],
  useful_for=["formal ethics / AI alignment", "legal reasoning",
              "normative multi-agent systems"]),
]

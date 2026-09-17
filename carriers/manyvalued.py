"""carriers.manyvalued — 6 carriers."""

CARRIERS = [
 dict(id=23, key="POST_N", name="Post n-Valued Logic (P_n)",
  origin="Emil Post (1921)",
  V="{0, 1/(n-1), ..., 1} — n equally spaced values",
  G="NOT = cyclic shift of order n; AND=min; OR=max",
  theta="1.0",
  insight=("Negation generalized from a mirror to a rotation: NOT^n is "
           "the identity. At n=2 the cycle IS classical negation and all "
           "15 laws return; for n>2 the value-reading LNC/LEM die at "
           "interior points because a rotation is not a complement."),
  forces=[
   dict(claim="NOT has order exactly n; n=2 recovers the full classical "
              "signature; interior witnesses for value-reading failures",
        check="post_cyclic")],
  breaks=[
   dict(claim="min(v, NOT v) != 0 and max != 1 at v=1/3 for n=4",
        check="post_cyclic")],
  useful_for=["finite-valued logic", "error-correcting code design",
              "many-valued switching theory"]),

 dict(id=24, key="BELNAP", name="Belnap Four-Valued Logic (FOUR)",
  origin="Nuel Belnap (1977)",
  V="{N, F, T, B} with independent truth and knowledge orderings",
  G="componentwise lattice ops per ordering; NOT swaps T/F, fixes N/B",
  theta="T designated; B = maximal but contradictory information",
  insight=("Truth and information de-conflated: N is no evidence, B is "
           "too much. The bilattice keeps orthogonal what classical "
           "logic collapses — how a computer should think when its "
           "sources disagree."),
  forces=[
   dict(claim="bilattice structure; NOT swaps truth poles and fixes "
              "information poles; lattice laws", check="belnap_bilattice")],
  breaks=[
   dict(claim="LNC fails at B (self-negating glut); LEM fails at N",
        check="belnap_bilattice")],
  useful_for=["inconsistent databases", "multi-source aggregation",
              "paraconsistent reasoning"]),

 dict(id=25, key="MV_ALG", name="MV-Algebra (Chang)",
  origin="C.C. Chang (1958)",
  V="[0,1] or any MV-algebra",
  G="bounded PLUS = min(1,a+b) and NOT = 1-a as the only primitives",
  theta="1.0; PLUS saturates",
  insight=("Two primitives generate all of Lukasiewicz logic: saturating "
           "addition and complement. 0.7 plus 0.8 is 1, not 1.5 — "
           "arithmetic with a ceiling, and the ceiling is what makes the "
           "connectives derivable."),
  forces=[
   dict(claim="Lukasiewicz AND and OR both derived from PLUS and NOT "
              "on a grid; saturation exhibited", check="mv_derives_lukasiewicz")],
  breaks=[
   dict(claim="Chang completeness for infinite-valued Lukasiewicz",
        cite="Chang 1958-59; PRESUMED — a completeness theorem, not a "
             "finite enumeration"),
   dict(claim="product and Godel t-norms not captured",
        cite="standard; different residuated structures")],
  useful_for=["algebraic semantics", "many-valued arithmetic",
              "probability-adjacent logic"]),

 dict(id=26, key="EFFECT", name="Effect Algebra (Quantum Logic)",
  origin="Foulis & Bennett (1994)",
  V="quantum effects; [0,1] instance here",
  G="PARTIAL sum, defined only for orthogonal pairs; orthocomplement",
  theta="orthogonality: a (+) b exists iff a+b <= 1",
  insight=("Incompatibility as non-existence: the sum of two "
           "non-orthogonal effects is not zero, it is UNDEFINED. "
           "Uncertainty becomes a theorem of the algebra's partiality "
           "rather than an added postulate."),
  forces=[
   dict(claim="commutativity where defined; x (+) x' = 1; the "
              "undefined case exhibited (0.7 (+) 0.6)",
        check="effect_algebra_partial")],
  breaks=[
   dict(claim="Boolean algebra is the special case where all pairs are "
              "orthogonal", cite="Foulis-Bennett; structural")],
  useful_for=["quantum measurement theory", "unsharp quantum logic",
              "operational QM"]),

 dict(id=27, key="HEYTING", name="Heyting Algebra",
  origin="Arend Heyting (1930)",
  V="lattices with implication as the residual of meet",
  G="MEET, JOIN, IMP(a,b) = largest c with a AND c <= b; NOT a = IMP(a,0)",
  theta="the top element; LEM fails when JOIN cannot reach it",
  insight=("Implication defined by adjointness makes LNC a definitional "
           "consequence and leaves LEM optional. Open sets of any "
           "topological space form one: a region refuting P need not be "
           "complemented by one proving it — topology IS intuitionism."),
  forces=[
   dict(claim="adjointness and LNC forced on the open-set algebra of a "
              "2-point space, by complete enumeration",
        check="heyting_open_sets")],
  breaks=[
   dict(claim="LEM fails: {a} OR NOT{a} misses the top",
        check="heyting_open_sets")],
  useful_for=["intuitionistic semantics", "topos theory", "locales",
              "sheaf semantics"]),

 dict(id=28, key="BL", name="Basic Logic (BL) / Hajek",
  origin="Petr Hajek (1998), Metamathematics of Fuzzy Logic",
  V="[0,1] or any BL-algebra",
  G="any continuous t-norm with its residuum; divisibility; prelinearity",
  theta="1.0",
  insight=("The laws common to ALL continuous-t-norm logics, "
           "axiomatized: whatever continuous conjunction you pick, "
           "residuation and prelinearity come with it. Lukasiewicz, "
           "Godel, and product are the three irreducible generators."),
  forces=[
   dict(claim="residuation and prelinearity hold for all three "
              "fundamental t-norms on the verification grid",
        check="bl_three_tnorms")],
  breaks=[
   dict(claim="every continuous t-norm is an ordinal sum of the three",
        cite="Mostert-Shields 1957; PRESUMED — a classification theorem")],
  useful_for=["fuzzy-logic unification", "truth-functional reasoning"]),
]

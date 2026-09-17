"""carriers.settype — 7 carriers."""

CARRIERS = [
 dict(id=29, key="ZF", name="Zermelo-Fraenkel Set Theory (ZF/ZFC)",
  origin="Zermelo (1908); Fraenkel (1922); Skolem (1922)",
  V="well-founded sets; cumulative hierarchy V_alpha",
  G="membership, power set, union, separation, replacement, infinity",
  theta="ordinal rank — patterns cohere at their level",
  insight=("Mathematics built upward from nothing, level by level. "
           "Russell's paradox dies by geography: membership requires a "
           "strictly lower level, so nothing contains itself and the "
           "Russell class is always the whole floor you are standing on "
           "— never available as a brick."),
  forces=[
   dict(claim="foundation and extensionality on the hereditarily "
              "finite universe; the Russell class at each rank IS the "
              "rank, and never a member of itself", check="zf_foundation_hf")],
  breaks=[
   dict(claim="no universal set; CH undecidable in ZFC",
        cite="Godel 1938 + Cohen 1963; PRESUMED — forcing is beyond "
             "enumeration by nature")],
  useful_for=["foundations", "formal verification of mathematics",
              "category-theory foundations"]),

 dict(id=30, key="NF", name="New Foundations (NF / NFU)",
  origin="Quine (1937); Jensen (1969) NFU",
  V="all sets INCLUDING a universal set",
  G="comprehension restricted to stratified formulas",
  theta="consistent type-level assignment",
  insight=("Russell blocked syntactically instead of ontologically: a "
           "set-forming formula must admit a consistent typing of its "
           "variables. {x : x not-in x} demands t = t+1 and is refused; "
           "{x : x = x} types trivially, so the universe exists."),
  forces=[
   dict(claim="stratification decided by type unification: Russell "
              "unstratifiable, identity stratifiable — the decision "
              "procedure implemented and run", check="nf_stratification")],
  breaks=[
   dict(claim="AC is FALSE in NF (Specker); full NF consistency long "
              "open, NFU consistent",
        cite="Specker 1953; Jensen 1969; Holmes' claimed proof under "
             "review — PRESUMED status per the literature")],
  useful_for=["alternative foundations", "cardinality without choice"]),

 dict(id=31, key="STT", name="Simple Theory of Types (Church)",
  origin="Russell (1908); Church (1940)",
  V="typed terms over base types e, t and arrows a->b",
  G="lambda abstraction and application, within type boundaries",
  theta="typability",
  insight=("Self-application made ungrammatical: x x needs x to be both "
           "a and a->b, and the occurs check says no. The paradoxes are "
           "not disproved — they are unwritable."),
  forces=[
   dict(claim="lambda x.xx untypable — unification with occurs check, "
              "implemented and refusing", check="stt_self_application_untypable")],
  breaks=[
   dict(claim="strong normalization of simply-typed terms",
        cite="Tait 1967; PRESUMED — reducibility argument"),
   dict(claim="no quantification over all types at once",
        cite="definitional stratification")],
  useful_for=["HOL provers", "typed functional languages",
              "semantics of programming"]),

 dict(id=32, key="MLTT", name="Martin-Lof Type Theory",
  origin="Per Martin-Lof (1975, 1984)",
  V="dependent types; types are first-class values",
  G="Pi and Sigma formation, beta/eta, identity types",
  theta="universe levels — each Type_n lives in Type_{n+1}",
  insight=("Propositions ARE types and proofs ARE programs: to prove "
           "the universally quantified is to write the function. The "
           "universe tower does for type theory what ranks do for ZF."),
  forces=[
   dict(claim="Curry-Howard on an instance: the K combinator inhabits "
              "and computes A -> (B -> A)", check="mltt_curry_howard_instance")],
  breaks=[
   dict(claim="Type:Type is inconsistent (Girard's paradox)",
        cite="Girard 1972; PRESUMED"),
   dict(claim="uniqueness of identity proofs fails in HoTT models",
        cite="Hofmann-Streicher groupoid model 1996; PRESUMED")],
  useful_for=["Coq/Agda/Idris", "certified software",
              "program extraction"]),

 dict(id=33, key="HOTT", name="Homotopy Type Theory",
  origin="Voevodsky (2006-2010); Univalent Foundations Program (2013)",
  V="types as spaces; identity proofs as paths; higher structure",
  G="path induction, transport, univalence: (A=B) = (A~=B)",
  theta="homotopy dimension",
  insight=("Equality gets geometry: two proofs of a=b can themselves "
           "differ, and univalence declares isomorphic types literally "
           "equal. Structure-transport for free, at the cost of "
           "classical certainties becoming undecided."),
  forces=[
   dict(claim="univalence; function extensionality derivable; higher "
              "inductive types",
        cite="HoTT Book 2013; PRESUMED — this library does not "
             "implement a proof assistant, and says so")],
  breaks=[
   dict(claim="LEM and AC undecided in pure HoTT",
        cite="HoTT Book ch.3; PRESUMED")],
  useful_for=["univalent foundations", "cubical Agda / Lean",
              "synthetic homotopy theory"]),

 dict(id=34, key="TOPOS", name="Topos Logic (Lawvere-Tierney)",
  origin="Lawvere & Tierney (1969-72)",
  V="a topos's subobject classifier Omega",
  G="connectives as universal properties on Omega",
  theta="the Grothendieck topology chosen",
  insight=("Each mathematical universe carries its own logic, read off "
           "its Omega: in Set the classifier is {0,1} and logic is "
           "classical; in sheaves it is the opens, and logic goes "
           "intuitionistic. Logic is a dependent variable."),
  forces=[
   dict(claim="Sub(A) ~ Hom(A, Omega) by complete enumeration in Set "
              "for |A| <= 3", check="topos_subobject_classifier_Set"),
   dict(claim="sheaf-style Omega is Heyting, not Boolean: the open-set "
              "instance", check="heyting_open_sets")],
  breaks=[
   dict(claim="LEM only in Boolean toposes",
        cite="Mac Lane & Moerdijk; PRESUMED as the general theorem — "
             "the failing instance above is exhibited")],
  useful_for=["algebraic geometry", "synthetic differential geometry",
              "alternative foundations"]),

 dict(id=65, key="ORDINALS", name="Ordinal Arithmetic (Cantor Normal Form)",
  origin="Cantor (1883); Gentzen (1936)",
  V="ordinals in CNF below epsilon_0",
  G="non-commutative +, *, and omega-exponentiation on normal forms",
  theta="epsilon_0 — the proof-theoretic ordinal of PA",
  insight=("Order types with base-omega positional notation. Addition "
           "reads left to right through infinity: a finite prefix "
           "drowns (1+w=w) while a finite suffix survives (w+1>w). "
           "Gentzen located PA exactly here: induction to epsilon_0 is "
           "PA's consistency, no more, no less."),
  forces=[
   dict(claim="CNF arithmetic implemented: 1+w=w yet w+1>w; every "
              "ordinal has a strict successor", check="ordinal_noncommutative"),
   dict(claim="normal forms are canonical: regrouping lands on the "
              "identical representation", check="ordinal_normal_form_unique")],
  breaks=[
   dict(claim="commutativity of + and * — dead at the first limit",
        check="ordinal_noncommutative"),
   dict(claim="Gentzen: Con(PA) = induction to epsilon_0",
        cite="Gentzen 1936; PRESUMED — proof theory, not enumeration")],
  useful_for=["ordinal analysis", "termination proofs",
              "consistency strength"]),
]

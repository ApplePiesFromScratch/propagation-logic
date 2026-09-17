"""carriers.cs — 15 carriers (the PDF's 14 plus the Living Map)."""

CARRIERS = [
 dict(id=44, key="KLEENE", name="Kleene Algebra (Regular Languages)",
  origin="Kleene (1956); Kozen (1994)",
  V="regular languages over an alphabet",
  G="union, concatenation, star",
  theta="automaton state count",
  insight=("An idempotent semiring with closure: star is the least "
           "fixed point of repetition. Equality of regular expressions "
           "is DECIDABLE, and the library decides it — via automata, "
           "the semantic referee."),
  forces=[
   dict(claim="a* = 1 + a a*, idempotency, and a denesting identity "
              "decided by NFA language comparison (bounded word length, "
              "stated)", check="kleene_star_fixpoint")],
  breaks=[
   dict(claim="context-free is out of reach (pumping)",
        cite="Bar-Hillel et al. 1961; PRESUMED")],
  useful_for=["regex engines", "model checking", "protocol verification"]),

 dict(id=45, key="HOARE", name="Hoare Logic (Pre/Postconditions)",
  origin="Tony Hoare (1969)",
  V="predicates over program states",
  G="triples composed sequentially; assignment reasons backwards",
  theta="partial vs total correctness",
  insight=("Programs as predicate transformers: the loop rule is the "
           "whole game — find the invariant, show the body keeps it, "
           "conjoin the exit condition. The library establishes one "
           "over an entire bounded state space."),
  forces=[
   dict(claim="invariant established, preserved by every body "
              "execution, postcondition at exit — full space n < 8",
        check="hoare_wp_bounded")],
  breaks=[
   dict(claim="unbounded loops need termination arguments beyond "
              "partial correctness", cite="total correctness needs "
              "well-founded variants; standard")],
  useful_for=["Why3/VeriFast", "safety-critical code", "kernel proofs"]),

 dict(id=46, key="SEPARATION", name="Separation Logic (Heaps)",
  origin="Reynolds (2002); O'Hearn & Pym (1999)",
  V="heaps as partial address maps",
  G="separating conjunction over DISJOINT regions; frame rule",
  theta="footprint disjointness",
  insight=("Local reasoning made sound by geometry: P*R splits the heap, "
           "a command touching only P's footprint cannot disturb R, so "
           "specifications compose. Enumerated here over every small "
           "heap: the frame survives every mutation."),
  forces=[
   dict(claim="frame rule verified over all enumerated heaps: the "
              "R-region is bit-identical after the mutation",
        check="separation_frame_rule")],
  breaks=[
   dict(claim="concurrency and permissions need CSL machinery",
        cite="O'Hearn 2007; PRESUMED")],
  useful_for=["memory-safety proofs", "Rust semantics", "OS verification"]),

 dict(id=47, key="LAMBDA", name="Lambda Calculus",
  origin="Church (1932-36); Church-Rosser (1936)",
  V="lambda terms (de Bruijn here)",
  G="beta reduction",
  theta="possession of a normal form",
  insight=("Two constructors and one rewrite rule reach all of "
           "computation. Confluence means reduction order cannot change "
           "answers, only whether you get one — and Omega demonstrates "
           "the 'whether' live."),
  forces=[
   dict(claim="both redex orders of (II)(II) join; Church 2+2 reduces "
              "to Church 4 exactly; Omega finds no normal form in 100 "
              "steps (bound stated)", check="lambda_church_rosser_bounded")],
  breaks=[
   dict(claim="normal-form possession undecidable in general",
        cite="Church 1936; PRESUMED — the fuel bound above is the "
             "honest finite shadow of it")],
  useful_for=["functional languages", "Curry-Howard", "semantics"]),

 dict(id=48, key="DOMAIN", name="Domain Theory (Scott)",
  origin="Dana Scott (1969-70)",
  V="complete partial orders with bottom = undefined",
  G="Scott-continuous functions; least fixed points by iteration",
  theta="approximation depth from bottom",
  insight=("Recursion as a limit: start knowing nothing, unfold once "
           "per stage, and the ascending chain of partial answers "
           "converges to the meaning. The library iterates factorial "
           "into existence and watches the chain go stationary."),
  forces=[
   dict(claim="Kleene iteration reaches the least fixed point of the "
              "factorial functional; the chain is monotone",
        check="domain_lfp_iteration")],
  breaks=[
   dict(claim="parallel-or is not sequentially definable",
        cite="Plotkin 1977; PRESUMED")],
  useful_for=["denotational semantics", "laziness", "recursive types"]),

 dict(id=49, key="ABSINT", name="Abstract Interpretation (Galois)",
  origin="Cousot & Cousot (1977)",
  V="concrete states vs abstract approximations",
  G="alpha (abstract) adjoint to gamma (concretize); widening",
  theta="precision of the abstraction",
  insight=("Program analysis as a Galois connection: the abstract world "
           "must over-approximate, so anything it rules out is truly "
           "absent — false positives are the tax, unsoundness never. "
           "The adjunction is decided here over the whole finite lattice."),
  forces=[
   dict(claim="alpha(S) <= a iff S <= gamma(a) over ALL subsets x ALL "
              "intervals; abstract + soundly over-approximates",
        check="absint_interval_galois")],
  breaks=[
   dict(claim="precision vs termination is a real trade (widening)",
        cite="Cousot^2 1977; structural")],
  useful_for=["static analysis", "verified compilers", "taint analysis"]),

 dict(id=50, key="PROCESS", name="Process Algebra (CCS/CSP)",
  origin="Milner (1980); Hoare (1985)",
  V="labelled transition systems up to bisimulation",
  G="prefix, choice, parallel composition with synchronization",
  theta="bisimulation depth",
  insight=("Equivalence for interactive systems: traces record what "
           "happened, bisimulation records what could have been "
           "refused. The classic pair a.(b+c) vs a.b+a.c — identical "
           "traces, different commitments — is separated live by "
           "partition refinement."),
  forces=[
   dict(claim="trace-equal but not bisimilar: the classic pair, "
              "computed", check="bisimulation_vs_traces")],
  breaks=[
   dict(claim="general process equivalence undecidable (Turing power)",
        cite="Milner; PRESUMED")],
  useful_for=["protocol verification", "session types", "Go channels"]),

 dict(id=66, key="COMPUTABILITY", name="Computability Theory (Turing)",
  origin="Turing (1936); Church (1936); Kleene (1936)",
  V="partial functions N -> N; machines as data",
  G="universal simulation; many-one and Turing reductions",
  theta="totality / decidability",
  insight=("The founding move: programs are strings, so machines can "
           "eat machines — the library's interpreter runs the busy "
           "beaver to its halt. The diagonal then lives exactly where "
           "no bounded demo can reach, and is tagged accordingly."),
  forces=[
   dict(claim="TM interpreter runs the 2-state busy-beaver champion: "
              "halts at step 6 with 4 ones", check="tm_universal_simulation")],
  breaks=[
   dict(claim="halting undecidable; Rice's theorem",
        cite="Turing 1936; Rice 1953; PRESUMED — necessarily: the "
             "diagonal quantifies over all machines")],
  useful_for=["undecidability proofs", "reductions", "the CS bedrock"]),

 dict(id=67, key="COMPLEXITY", name="Computational Complexity (P vs NP)",
  origin="Cook (1971); Karp (1972); Razborov (1987)",
  V="languages sorted into resource classes",
  G="polynomial-time reductions; circuits",
  theta="polynomial = feasible (Cobham)",
  insight=("What can be VERIFIED fast versus what can be FOUND fast. "
           "The library runs Karp in miniature — a 3-coloring instance "
           "reduced to SAT, both sides brute-forced, answers agreeing — "
           "and files the big question at the only honest tier it has."),
  forces=[
   dict(claim="reduction instance preserves the answer: 3-coloring to "
              "SAT, both brute-forced and agreeing",
        check="sat_reduction_instance"),
   dict(claim="time hierarchy: more time is more power",
        cite="Hartmanis-Stearns 1965; PRESUMED")],
  breaks=[
   dict(claim="P vs NP", tier="OPEN",
        cite="Clay Millennium Problem, open since 1971; relativization "
             "and natural-proofs barriers block the known routes"),
   dict(claim="natural proofs barrier",
        cite="Razborov-Rudich 1997; PRESUMED")],
  useful_for=["crypto hardness", "approximation regimes",
              "SAT-solver practice"]),

 dict(id=68, key="PROOF_THEORY", name="Proof Theory (Gentzen)",
  origin="Hilbert (1900); Gentzen (1935); Takeuti; Feferman",
  V="proofs as syntactic trees; sequents",
  G="cut elimination; ordinal assignment",
  theta="the proof-theoretic ordinal",
  insight=("Proofs as objects of study: cut elimination trades lemmas "
           "for transparency (every formula a subformula of the goal), "
           "and each theory earns an ordinal — its exact rung on the "
           "consistency-strength ladder. This section is deliberately "
           "citation-heavy: cut elimination's blowup is precisely why "
           "no small demo does it justice, and the paid fraction says so."),
  forces=[
   dict(claim="Hauptsatz: every provable sequent has a cut-free proof",
        cite="Gentzen 1935; PRESUMED"),
   dict(claim="Con(PA) equivalent to induction below epsilon_0 — the "
              "ordinal side is executable in the ORDINALS carrier",
        cite="Gentzen 1936; PRESUMED here, CNF arithmetic FORCED there")],
  breaks=[
   dict(claim="no sufficiently strong consistent T proves Con(T)",
        cite="Godel 1931; PRESUMED"),
   dict(claim="cut-free proofs can be non-elementarily longer",
        cite="Statman 1978; PRESUMED")],
  useful_for=["consistency proofs", "reverse mathematics",
              "automated deduction"]),

 dict(id=69, key="MODEL_THEORY", name="Model Theory (Tarski)",
  origin="Tarski (1936); Godel (1930); Morley (1965)",
  V="first-order structures and their theories",
  G="Tarskian satisfaction; ultraproducts; elementary maps",
  theta="cardinality — which first-order logic cannot pin down",
  insight=("Languages meet their interpretations: truth defined "
           "compositionally (and implemented here, running on finite "
           "graphs), completeness weds proof to validity, and "
           "compactness guarantees non-standard models — infinitesimals "
           "and infinite integers are features of first-order "
           "expressiveness, not bugs."),
  forces=[
   dict(claim="Tarski satisfaction implemented; isomorphic finite "
              "structures agree on every tested sentence",
        check="tarski_satisfaction_finite"),
   dict(claim="completeness: provable iff valid",
        cite="Godel 1930; PRESUMED")],
  breaks=[
   dict(claim="N and R not first-order characterizable "
              "(Lowenheim-Skolem both directions)",
        cite="Lowenheim 1915, Skolem 1920; PRESUMED — about infinite "
             "models by nature")],
  useful_for=["non-standard analysis", "algebraic axiomatics",
              "database theory"]),

 dict(id=70, key="REVERSE_MATH", name="Reverse Mathematics (Big Five)",
  origin="Friedman (1975); Simpson (1999)",
  V="subsystems of second-order arithmetic",
  G="proving the AXIOM back from the THEOREM over RCA_0",
  theta="the five calibration marks RCA_0 < WKL_0 < ACA_0 < ATR_0 < Pi11-CA_0",
  insight=("Theorems priced by the set-existence they secretly demand — "
           "and almost all of classical analysis lands on one of just "
           "five rungs. The methodology is this library's own discipline "
           "applied to mathematics itself, which is why it is cataloged "
           "even though every claim here is PRESUMED: reversals are "
           "meta-proofs no instance can exhibit."),
  forces=[
   dict(claim="the Big Five phenomenon; WKL_0 = Heine-Borel = Brouwer "
              "fixed point (over RCA_0)",
        cite="Simpson, SOSOA 1999; PRESUMED")],
  breaks=[
   dict(claim="Ramsey for pairs falls strictly between the rungs",
        cite="Seetapun-Slaman 1995, Liu 2012; PRESUMED")],
  useful_for=["axiom calibration", "computable mathematics",
              "philosophy of proof"]),

 dict(id=71, key="MONADS", name="Monads (Effects as Structure)",
  origin="Mac Lane (1971); Moggi (1991); Wadler (1992)",
  V="endofunctors with return and join",
  G="Kleisli composition",
  theta="the three monad laws",
  insight=("Side effects packaged as algebra: return injects purity, "
           "bind sequences effects, and the three laws are exactly "
           "monoid laws one level up. The library enumerates them for "
           "Maybe and List — the laws your code must satisfy or your "
           "refactorings lie."),
  forces=[
   dict(claim="left identity, right identity, associativity — Maybe "
              "and List, complete enumeration over the test domain",
        check="category_monad_laws")],
  breaks=[
   dict(claim="monads do not compose without a distributive law",
        cite="Beck 1969; PRESUMED")],
  useful_for=["Haskell effects", "denotational semantics",
              "query languages"]),

 dict(id=72, key="PETRI", name="Petri Nets (Token Flow)",
  origin="Carl Adam Petri (1962)",
  V="markings of a place/transition net",
  G="local firing; reachability",
  theta="place invariants — conservation laws",
  insight=("Concurrency without a clock: transitions fire on local "
           "sufficiency, conflicts are shared hunger, and a place "
           "invariant is a conservation law the net cannot break — "
           "verified here across the ENTIRE reachable state space."),
  forces=[
   dict(claim="x.C = 0 invariant; token count conserved across all "
              "reachable markings by exhaustive BFS; no deadlock in "
              "this net", check="petri_invariant_conservation")],
  breaks=[
   dict(claim="reachability decidable but expensive (EXPSPACE-hard); "
              "inhibitor arcs buy Turing power and lose decidability",
        cite="Mayr 1981; Lipton 1976; PRESUMED")],
  useful_for=["workflow engines", "metabolic networks",
              "async hardware"]),

 dict(id=84, key="LIVING_MAP", name="Program-Variant Optimisation (The Living Map)",
  origin="paudit.py (2026); Young (1950); Ostrowski (1954)",
  V="programs up to contract equivalence on a probe set",
  G="contract-preserving transforms; relaxation-parameter choice",
  theta="the budget and the contract",
  insight=("Optimisation as propagation: descend the load without "
           "leaving the contract class, and let theta refuse every "
           "cheaper variant that breaks a bridge. The gate runs live "
           "here — a closed form accepted for keeping the contract and "
           "dropping the load, a subtly wrong variant refused — and the "
           "solver's coherence wall at omega = 2 is measured as "
           "divergence, not slowness."),
  forces=[
   dict(claim="the accept/refuse gate on a live instance: contract "
              "kept + load dropped = accepted; contract broken = "
              "refused", check="program_variant_contract_gate"),
   dict(claim="SOR converges inside the wall, decoheres beyond it "
              "(omega 1.5 vs 2.1 on an SPD system)",
        check="sor_coherence_boundary")],
  breaks=[
   dict(claim="a finite probe set is not semantic equivalence — the "
              "contract is STIPULATED on every accept", tier="STIPULATED",
        cite="declared by the carrier itself, as the source PDF does"),
   dict(claim="gated local speedups do not compose to global optimality",
        cite="Amdahl + the moving critical path; structural")],
  useful_for=["compiler passes with receipts", "solver tuning",
              "regression-safe refactoring", "critical-path analysis"]),
]

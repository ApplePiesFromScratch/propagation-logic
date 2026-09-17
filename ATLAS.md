# Atlas

A map of maps. V, G, theta, what sits outside, what breaks.
Nouns are labels. Paid badges were earned at render time.
**89 carriers · 231 claims · 126 paid (54.5%)**


## Propositional Logic

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `CL2` | {0,1} — exactly two truth values | NOT v=1-v; AND=product/min; OR=max; IMP(a,b)=max(1-a,b) | 1.0 — only full truth designated |  | 3/4 |
| `L3` | {0, 1/2, 1} — false, indeterminate, true | NOT v=1-v; AND(a,b)=max(0,a+b-1); OR=min(1,a+b); IMP=min(1,1-a+b) | 1.0 — only 1 designated |  | 3/4 |
| `K3` | {0, 1/2, 1} — false, undefined, true | NOT v=1-v; AND=min; OR=max; IMP(a,b)=max(1-a,b) | 1.0 — only 1 designated |  | 3/3 |
| `WK3` | {0, u, 1} — u = undefined, absorbing | NOT(u)=u; AND(u,x)=u and OR(u,x)=u unconditionally; classical on {0,1} | 1.0 — u blocks all inference through it |  | 2/3 |
| `B3` | {0, m, 1} — m = meaningless/paradoxical | internal: m absorbs; external assertion E(1)=1, E(0)=E(m)=0 | 1.0 externally; m quarantined internally |  | 1/2 |
| `LP` | {0, B, 1}; B = both, arithmetically 1/2 | NOT v=1-v; AND=min; OR=max; DESIGNATED = {B, 1} | designation includes the glut |  | 3/3 |
| `FUZZY_PROD` | [0,1] continuous | NOT v=1-v; AND=a*b; OR=max; Goguen IMP | 1.0 |  | 2/3 |
| `FUZZY_LUK` | [0,1] — metric completion of the finite L_n chain | NOT v=1-v; AND=max(0,a+b-1); OR=min(1,a+b); IMP=min(1,1-a+b) | 1.0 |  | 1/2 |
| `FUZZY_GODEL` | [0,1] linearly ordered | NOT(v)=1 if v=0 else 0; AND=min; OR=max; IMP crisp residuum | 1.0 |  | 1/2 |
| `INT` | {0,1} but reachable only by explicit construction | OR needs a witness; IMP is a proof transformer; NOT P = P -> false | 1.0 — truth is possession of a proof |  | 2/3 |
| `LINEAR` | formulas as resources, used exactly once unless marked ! | tensor (both), additive AND (choose), -o (consume to produce), ! (unlimited) | exact resource count |  | 2/3 |
| `RELEVANCE` | {0,1} with a relevance filter on derivations | classical connectives; IMP valid only under variable sharing | every premise must contribute a variable |  | 2/3 |
| `DUAL_INT` | co-Heyting algebras — closed sets where intuitionism has opens | subtraction A-B as the primitive; OR needs refutation evidence | 0.0 — a proposition fails only on explicit refutation |  | 2/2 |
| `SUBSTRUCT` | sequents; V depends on retained structural rules | connectives fixed; Weakening/Contraction/Exchange/Cut are dials | which structural rules survive |  | 1/3 |

## Modal Logic

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `MODAL_K` | worlds W with accessibility R; NECS/POSS index truth over R-neighbors | NECS = universal over accessible worlds; POSS = existential; R unconstrained | the accessibility relation itself |  | 2/3 |
| `MODAL_T` | Kripke frames with wRw for all w | K plus reflexivity | self-accessibility |  | 2/2 |
| `MODAL_S4` | frames where R is reflexive and transitive | T plus transitivity | preorder accessibility |  | 2/2 |
| `MODAL_S5` | frames where R is an equivalence relation | S4 plus symmetry | full mutual accessibility within classes |  | 1/2 |
| `MODAL_GL` | NECS(P) = 'PA proves P'; frames transitive + conversely well-founded | K + 4 + Lob axiom | proof depth; well-foundedness of provability |  | 2/3 |
| `EPISTEMIC` | worlds with per-agent indistinguishability relations R_i | K_i = universal over agent i's R; common knowledge = infinite closure | epistemic indistinguishability per agent |  | 1/2 |
| `TEMPORAL` | time steps as worlds; linear traces (LTL) or trees (CTL) | X next, F eventually, G always, U until | finite paths verify F; G outruns any finite observation |  | 1/3 |
| `DEONTIC` | worlds ranked by moral ideality; O/P/F over ideal worlds | O(P): P in all ideal accessible worlds; P(P): in some; F=O(NOT P) | seriality — somewhere, an ideal world exists |  | 1/2 |

## Many-Valued Logic

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `POST_N` | {0, 1/(n-1), ..., 1} — n equally spaced values | NOT = cyclic shift of order n; AND=min; OR=max | 1.0 |  | 2/2 |
| `BELNAP` | {N, F, T, B} with independent truth and knowledge orderings | componentwise lattice ops per ordering; NOT swaps T/F, fixes N/B | T designated; B = maximal but contradictory information |  | 2/2 |
| `MV_ALG` | [0,1] or any MV-algebra | bounded PLUS = min(1,a+b) and NOT = 1-a as the only primitives | 1.0; PLUS saturates |  | 1/3 |
| `EFFECT` | quantum effects; [0,1] instance here | PARTIAL sum, defined only for orthogonal pairs; orthocomplement | orthogonality: a (+) b exists iff a+b <= 1 |  | 1/2 |
| `HEYTING` | lattices with implication as the residual of meet | MEET, JOIN, IMP(a,b) = largest c with a AND c <= b; NOT a = IMP(a,0) | the top element; LEM fails when JOIN cannot reach it |  | 2/2 |
| `BL` | [0,1] or any BL-algebra | any continuous t-norm with its residuum; divisibility; prelinearity | 1.0 |  | 1/2 |

## Set Theory & Type Theory

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `ZF` | well-founded sets; cumulative hierarchy V_alpha | membership, power set, union, separation, replacement, infinity | ordinal rank — patterns cohere at their level |  | 1/2 |
| `NF` | all sets INCLUDING a universal set | comprehension restricted to stratified formulas | consistent type-level assignment |  | 1/2 |
| `STT` | typed terms over base types e, t and arrows a->b | lambda abstraction and application, within type boundaries | typability |  | 1/3 |
| `MLTT` | dependent types; types are first-class values | Pi and Sigma formation, beta/eta, identity types | universe levels — each Type_n lives in Type_{n+1} |  | 1/3 |
| `HOTT` | types as spaces; identity proofs as paths; higher structure | path induction, transport, univalence: (A=B) = (A~=B) | homotopy dimension |  | 0/2 |
| `TOPOS` | a topos's subobject classifier Omega | connectives as universal properties on Omega | the Grothendieck topology chosen |  | 2/3 |
| `ORDINALS` | ordinals in CNF below epsilon_0 | non-commutative +, *, and omega-exponentiation on normal forms | epsilon_0 — the proof-theoretic ordinal of PA |  | 3/4 |

## Mathematical Carriers

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `DUAL_NUM` | dual numbers a + b*eps with eps^2 = 0 | arithmetic extended through eps; the eps-slot carries the derivative | machine epsilon |  | 2/3 |
| `COMPLEX` | C = R^2 with rotation as multiplication | complex product; Cauchy-Riemann coupling; contour integration | radius of analytic continuation |  | 3/4 |
| `NSA` | hyperreals: R plus genuine infinitesimals and infinite numbers | transfer principle; standard-part projection | the monad around each real |  | 0/2 |
| `PADIC` | completion of Q under |x|_p = p^(-v_p(x)) | p-adic valuation and ultrametric distance | 1/p — the unit ball |  | 1/2 |
| `TROPICAL` | R with +infinity; ADD=min, MUL=+ | idempotent semiring operations | 0, the multiplicative identity |  | 1/2 |
| `QUANTUM` | positive Hermitian rho with trace 1 | unitary conjugation (reversible); measurement update (not) | purity Tr(rho^2) |  | 1/3 |
| `SHANNON` | probability distributions; entropies in bits | entropy, mutual information, KL divergence, capacity | channel capacity C |  | 1/2 |
| `STATMECH` | distributions over microstates | Hamiltonian flow (volume-preserving); entropy ascent | k_B T — the thermal load unit |  | 1/2 |
| `FISHER` | smooth families of distributions | Fisher metric; natural gradient | F itself — sensitivity per parameter |  | 1/2 |
| `CATEGORY` | objects known only through their morphisms | functors, natural transformations, adjunctions | functoriality and naturality squares |  | 2/3 |
| `GALOIS` | splitting fields with their automorphism groups | the order-reversing subgroup/subfield correspondence | solvability of the group |  | 1/2 |
| `LEBESGUE` | sigma-algebras with countably additive measure | integrate by partitioning the RANGE; Radon-Nikodym densities | sigma-finiteness; completeness of L^p |  | 1/3 |
| `ITO` | adapted processes on filtered probability spaces | the Ito integral (left endpoints, non-anticipating); Ito's lemma | quadratic variation [W,W]_t = t |  | 1/2 |
| `EXTERIOR` | antisymmetric multilinear k-forms | wedge product; exterior derivative d | d^2 = 0 — the nilpotency identity |  | 1/2 |
| `LIE` | smooth groups; tangent algebra at the identity | bracket [X,Y]; exponential map | non-degeneracy of the Killing form |  | 1/2 |
| `HOMOLOGY` | chain complexes over spaces | boundary maps with d.d = 0; induced maps | Betti numbers |  | 1/2 |
| `CONVEX` | convex sets and functions | subgradients; conjugation; Lagrangian duality | zero duality gap (Slater) |  | 1/2 |
| `SYMPLECTIC` | even-dimensional phase space with a closed 2-form | Hamiltonian flows; Poisson bracket | Liouville volume preservation |  | 1/2 |
| `SURREAL` | games {L|R} with no left option >= any right option | recursive addition, negation, multiplication; simplicity rule | birthday — earlier is simpler is canonical |  | 1/2 |

## Computer Science

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `KLEENE` | regular languages over an alphabet | union, concatenation, star | automaton state count |  | 1/2 |
| `HOARE` | predicates over program states | triples composed sequentially; assignment reasons backwards | partial vs total correctness |  | 1/2 |
| `SEPARATION` | heaps as partial address maps | separating conjunction over DISJOINT regions; frame rule | footprint disjointness |  | 1/2 |
| `LAMBDA` | lambda terms (de Bruijn here) | beta reduction | possession of a normal form |  | 1/2 |
| `DOMAIN` | complete partial orders with bottom = undefined | Scott-continuous functions; least fixed points by iteration | approximation depth from bottom |  | 1/2 |
| `ABSINT` | concrete states vs abstract approximations | alpha (abstract) adjoint to gamma (concretize); widening | precision of the abstraction |  | 1/2 |
| `PROCESS` | labelled transition systems up to bisimulation | prefix, choice, parallel composition with synchronization | bisimulation depth |  | 1/2 |
| `COMPUTABILITY` | partial functions N -> N; machines as data | universal simulation; many-one and Turing reductions | totality / decidability |  | 1/2 |
| `COMPLEXITY` | languages sorted into resource classes | polynomial-time reductions; circuits | polynomial = feasible (Cobham) |  | 1/4 |
| `PROOF_THEORY` | proofs as syntactic trees; sequents | cut elimination; ordinal assignment | the proof-theoretic ordinal |  | 0/4 |
| `MODEL_THEORY` | first-order structures and their theories | Tarskian satisfaction; ultraproducts; elementary maps | cardinality — which first-order logic cannot pin down |  | 1/3 |
| `REVERSE_MATH` | subsystems of second-order arithmetic | proving the AXIOM back from the THEOREM over RCA_0 | the five calibration marks RCA_0 < WKL_0 < ACA_0 < ATR_0 < Pi11-CA_0 |  | 0/2 |
| `MONADS` | endofunctors with return and join | Kleisli composition | the three monad laws |  | 1/2 |
| `PETRI` | markings of a place/transition net | local firing; reachability | place invariants — conservation laws |  | 1/2 |
| `LIVING_MAP` | programs up to contract equivalence on a probe set | contract-preserving transforms; relaxation-parameter choice | the budget and the contract |  | 2/4 |

## Physics

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `DRAS_SCALE` | (coupling, scale, load) | running of the coupling with ln E; beta function | the Landau pole — load diverges as the denominator dies |  | 1/2 |
| `THERMO` | (S, E, N, V) or phase-space distributions | Hamiltonian flow; entropy ascent; bit erasure | k_B T — and k_B T ln 2 per erased bit |  | 1/2 |
| `GR` | Lorentzian manifolds with metric g | covariant derivative; Einstein equations G = 8 pi T | curvature scale; singularities where it diverges |  | 1/4 |
| `QFT` | Fock space — superpositions of any particle number | creation/annihilation; path integral; renormalization group | UV cutoff; renormalizability as finite load per order |  | 1/2 |

## Probability & Evidence

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `KOLMOGOROV` | probability spaces (Omega, F, P) | conditioning; expectation; independence | P(Omega)=1 and sigma-additivity — the whole axiom bill |  | 1/3 |
| `BAYES` | coherent degrees of belief over hypotheses | Bayes updating; Jeffrey conditionalization | coherence — or a Dutch book exists |  | 1/3 |
| `DEMPSTER_SHAFER` | basic probability assignments over SETS of hypotheses | Dempster's combination rule, normalizing conflict away | the belief-plausibility interval |  | 2/3 |
| `POSSIBILITY` | possibility distributions, sup-normalized | Pi maxitive over unions; necessity by duality | normalization: something is fully possible |  | 1/2 |
| `IMPRECISE` | convex sets of probability measures | robust Bayes: update every member; natural extension | the credal set — singleton means classical, everything means ignorance |  | 1/2 |
| `BOUNDARY_LAW` | pairs of hypotheses separated by a gap, under noise | repeated noisy probing; redundancy against error | confidence 1 - delta |  | 1/3 |

## Measurement Interpretations

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `COPENHAGEN` | quantum state before, classical outcome after; nothing between | unitary evolution, then primitive projective collapse | the Heisenberg cut — deliberately unspecified |  | 1/4 |
| `MWI` | one universal wavefunction; branches via decoherence | unitary evolution ONLY — measurement is entanglement | decoherence time — when branches stop interfering |  | 2/4 |
| `BOHM` | wavefunction PLUS actual particle positions | Schrodinger for the wave; the guiding equation for the particles | quantum equilibrium: initial rho = |psi|^2 |  | 1/4 |
| `HISTORIES` | families of projector sequences (histories) | the decoherence functional; probabilities inside consistent families | consistency: off-diagonal decoherence functional = 0 |  | 1/2 |
| `GRW` | wavefunctions subject to spontaneous stochastic localization | Schrodinger plus random Gaussian hits at rate lambda per particle | lambda ~ 1e-16 /s and width ~ 1e-7 m — tuned so micro stays quantum and macro snaps |  | 2/3 |
| `RELATIONAL` | states defined only RELATIVE to an observing system | interactions actualize relative facts | the interaction event |  | 1/3 |

## Generated Atlas

| key | V | G | theta | outside | paid |
|---|---|---|---|---|---|
| `PROC_PAIR` | Q-pairs (v, r) | isolate; Leibniz mix; rate = top.r / bottom.r | dead isolator r=0 refuses; divisor v=0 refuses | Inf, limits, unary D as a property of f, unlistable R | 4/4 |
| `ORIGIN_WRAP` | distinguishable phases of Closure(n) | co_propagate (a+b)%n ; iterate | returns to itself | host-free addition; unbounded Nat without a schema | 3/3 |
| `MODUS_MP` | nine logic carriers (CL2,K3,LP,L3+,...) | MP / MT on designated set | designated values | MP as a law of thought; a token of the rule sitting in V | 3/3 |
| `MODAL_ATLAS` | listed W, listed R, atoms p,q | BOX=all successors DIA=any; filters on R | valid on every world of every passing frame under every val | infinite W; common knowledge as unbounded protocol; PA-completeness | 3/3 |

"""carriers.mathematical — 19 carriers."""

CARRIERS = [
 dict(id=35, key="DUAL_NUM", name="Differential Calculus (Dual Numbers)",
  origin="Leibniz (1684); Clifford (1873); Wengert (1964) autodiff",
  V="dual numbers a + b*eps with eps^2 = 0",
  G="arithmetic extended through eps; the eps-slot carries the derivative",
  theta="machine epsilon",
  insight=("One nilpotent element forces all of differential calculus: "
           "the product rule IS the cross term of (a+b eps)(c+d eps), "
           "the chain rule IS composition. Every autodiff framework is "
           "this algebra wearing a tensor library."),
  forces=[
   dict(claim="product and chain rules match sympy's derivatives "
              "exactly — forced by eps^2=0", check="dual_product_chain_rule")],
  breaks=[
   dict(claim="|x| at 0: one-sided slopes disagree — subgradients, not "
              "a derivative", check="dual_nonsmooth_limit"),
   dict(claim="stochastic paths need the Ito correction",
        cite="see the Ito carrier, where it is measured")],
  useful_for=["backpropagation", "scientific computing", "sensitivity"]),

 dict(id=36, key="COMPLEX", name="Complex Analysis (C-carrier)",
  origin="Cardano (1545); Euler; Cauchy (1821); Riemann (1851)",
  V="C = R^2 with rotation as multiplication",
  G="complex product; Cauchy-Riemann coupling; contour integration",
  theta="radius of analytic continuation",
  insight=("Rotation baked into arithmetic (i^2 = -1 is two quarter-"
           "turns making a negation) buys ferocious rigidity: "
           "differentiable once means analytic forever, and closed "
           "loops integrate to zero unless they trap a singularity."),
  forces=[
   dict(claim="Cauchy-Riemann verified symbolically for z^2 and exp(z)",
        check="complex_cauchy_riemann"),
   dict(claim="closed contour of z^2 vanishes; 1/z picks up exactly "
              "2 pi i", check="complex_contour_theorem")],
  breaks=[
   dict(claim="|z|^2 is real-smooth but not holomorphic — CR fails "
              "symbolically", check="complex_cauchy_riemann"),
   dict(claim="log needs a branch cut", cite="standard; multivaluedness")],
  useful_for=["fluid dynamics", "electromagnetism", "Fourier analysis",
              "zeta and number theory"]),

 dict(id=37, key="NSA", name="Non-Standard Analysis (*R)",
  origin="Abraham Robinson (1966)",
  V="hyperreals: R plus genuine infinitesimals and infinite numbers",
  G="transfer principle; standard-part projection",
  theta="the monad around each real",
  insight=("Infinitesimals rehabilitated by model theory: every "
           "first-order truth about R transfers to *R, so dy/dx becomes "
           "a literal ratio and limits become the algebraic act of "
           "taking the standard part."),
  forces=[
   dict(claim="transfer principle; saturation",
        cite="Robinson 1966 via ultrapowers and compactness; PRESUMED "
             "— the construction needs an ultrafilter, which no "
             "enumeration exhibits. The dual-number carrier is this "
             "library's executable cousin")],
  breaks=[
   dict(claim="the set of infinitesimals is external — unnameable "
              "inside the system", cite="Robinson 1966; PRESUMED")],
  useful_for=["rigorous infinitesimal calculus",
              "hyperfinite probability", "ultraproducts"]),

 dict(id=38, key="PADIC", name="p-adic Numbers (Q_p)",
  origin="Kurt Hensel (1897)",
  V="completion of Q under |x|_p = p^(-v_p(x))",
  G="p-adic valuation and ultrametric distance",
  theta="1/p — the unit ball",
  insight=("Size inverted: divisible-by-p means SMALL. The metric "
           "sharpens to an ultrametric, every triangle is isosceles, "
           "and 1+p+p^2+... converges — to a negative rational."),
  forces=[
   dict(claim="ultrametric and isosceles property on random rationals; "
              "the geometric series of 5 sums to -1/4 in |.|_5",
        check="padic_ultrametric")],
  breaks=[
   dict(claim="Q_p and R are non-isomorphic completions; Ostrowski "
              "says they exhaust the options",
        cite="Ostrowski 1916; PRESUMED")],
  useful_for=["local-global number theory", "lattice cryptography",
              "coding theory"]),

 dict(id=39, key="TROPICAL", name="Tropical Arithmetic (min-plus)",
  origin="Cuninghame-Green (1960s); Maslov (1987)",
  V="R with +infinity; ADD=min, MUL=+",
  G="idempotent semiring operations",
  theta="0, the multiplicative identity",
  insight=("Arithmetic where addition takes the better option and "
           "multiplication accumulates cost: matrix powers become "
           "shortest paths because Bellman's recursion IS tropical "
           "matrix multiplication. Optimization as algebra."),
  forces=[
   dict(claim="semiring laws; tropical matrix power equals "
              "Floyd-Warshall exactly on a random graph",
        check="tropical_shortest_path")],
  breaks=[
   dict(claim="no subtraction: min has no inverse",
        cite="idempotency kills cancellation; definitional")],
  useful_for=["shortest paths", "scheduling", "tropical geometry",
              "phylogenetics"]),

 dict(id=40, key="QUANTUM", name="Quantum Mechanics (Density Matrix)",
  origin="von Neumann (1932); Dirac (1930)",
  V="positive Hermitian rho with trace 1",
  G="unitary conjugation (reversible); measurement update (not)",
  theta="purity Tr(rho^2)",
  insight=("States as operators: unitaries move probability without "
           "creating or destroying it, measurement renormalizes onto "
           "the observed branch, and linearity alone forbids copying "
           "the unknown."),
  forces=[
   dict(claim="unitary evolution preserves trace and purity; Born "
              "weights normalize; no-cloning exhibited on a "
              "non-orthogonal pair", check="quantum_density_matrix")],
  breaks=[
   dict(claim="measurement is irreversible — the carrier changes",
        cite="see the Measurement Interpretations section, where the "
             "readings of this fact are priced separately"),
   dict(claim="non-commuting observables (Heisenberg)",
        cite="[x,p]=ih; standard")],
  useful_for=["quantum computing", "QKD", "error correction"]),

 dict(id=41, key="SHANNON", name="Information Theory (Shannon)",
  origin="Claude Shannon (1948)",
  V="probability distributions; entropies in bits",
  G="entropy, mutual information, KL divergence, capacity",
  theta="channel capacity C",
  insight=("Uncertainty quantified once, correctly: H is the "
           "compression floor, capacity the transmission ceiling, and "
           "the data-processing inequality the law that no massaging of "
           "Y ever tells you more about X."),
  forces=[
   dict(claim="data-processing inequality on 40 random Markov chains; "
              "BSC capacity computed", check="shannon_dpi")],
  breaks=[
   dict(claim="differential entropy can be negative; zero-error theory "
              "is a different beast", cite="Shannon 1948; Korner-Orlitsky "
              "survey; PRESUMED")],
  useful_for=["compression", "error-correcting codes", "crypto floors"]),

 dict(id=42, key="STATMECH", name="Statistical Mechanics (Gibbs/Boltzmann)",
  origin="Boltzmann (1872); Gibbs (1902)",
  V="distributions over microstates",
  G="Hamiltonian flow (volume-preserving); entropy ascent",
  theta="k_B T — the thermal load unit",
  insight=("The bridge from mechanics to thermodynamics is a "
           "constrained maximization: fix mean energy, maximize "
           "entropy, get exp(-E/kT) uniquely. Everything macroscopic is "
           "a derivative of its normalizer."),
  forces=[
   dict(claim="Boltzmann beats every constraint-respecting perturbation "
              "— entropy maximum verified in the exact null space",
        check="statmech_gibbs_maximizes")],
  breaks=[
   dict(claim="microscopic reversibility vs macroscopic arrow "
              "(Loschmidt); fluctuations in small systems",
        cite="Boltzmann's reply and modern fluctuation theorems; "
             "PRESUMED — see the Markov H-theorem check under "
             "Thermodynamics for the measurable core")],
  useful_for=["materials", "reaction rates", "computation thermodynamics"]),

 dict(id=43, key="FISHER", name="Fisher Information (Statistical Manifold)",
  origin="Fisher (1925); Rao (1945); Amari (1985)",
  V="smooth families of distributions",
  G="Fisher metric; natural gradient",
  theta="F itself — sensitivity per parameter",
  insight=("Distinguishability given a geometry: F measures how loudly "
           "the data protests a parameter change, Cramer-Rao makes "
           "1/F the price floor of unbiased estimation, and the natural "
           "gradient is descent that respects the terrain."),
  forces=[
   dict(claim="Gaussian F = 1/sigma^2 computed symbolically; the "
              "sample mean sits exactly on the Cramer-Rao floor",
        check="fisher_cramer_rao_gaussian")],
  breaks=[
   dict(claim="singular models break invertibility",
        cite="Watanabe, singular learning theory; PRESUMED")],
  useful_for=["optimal estimation", "natural-gradient training",
              "TRPO/PPO"]),

 dict(id=55, key="CATEGORY", name="Category Theory (Functors & Naturality)",
  origin="Eilenberg & Mac Lane (1945)",
  V="objects known only through their morphisms",
  G="functors, natural transformations, adjunctions",
  theta="functoriality and naturality squares",
  insight=("Identity through relationship: Yoneda says an object IS its "
           "pattern of incoming maps. The library runs the miniature: "
           "in a finite category, distinct objects have distinct "
           "hom-profiles, and the monad laws compute."),
  forces=[
   dict(claim="Yoneda in miniature: hom-profiles separate all objects "
              "of a finite poset category", check="category_yoneda_finite"),
   dict(claim="monad laws for Maybe and List by complete enumeration",
        check="category_monad_laws")],
  breaks=[
   dict(claim="not every functor has an adjoint; size issues loom",
        cite="Freyd adjoint functor theorem; PRESUMED")],
  useful_for=["universal algebra", "Haskell/Scala types",
              "sheaves and topoi"]),

 dict(id=56, key="GALOIS", name="Galois Theory (Field Extensions)",
  origin="Galois (1832); Dedekind & Weber (1882)",
  V="splitting fields with their automorphism groups",
  G="the order-reversing subgroup/subfield correspondence",
  theta="solvability of the group",
  insight=("Polynomial solvability converted to group structure. The "
           "library enumerates the classic instance completely: "
           "Q(sqrt2,sqrt3) has group C2xC2 and its three subgroups fix "
           "exactly the three intermediate fields — the correspondence, "
           "run rather than recited."),
  forces=[
   dict(claim="all four automorphisms are field homs; group is C2xC2; "
              "three subgroups <-> three intermediate fields, "
              "enumerated", check="galois_biquadratic")],
  breaks=[
   dict(claim="degree >= 5 generically unsolvable (A_5 simple)",
        cite="Abel 1824, Galois 1832; PRESUMED — simplicity of A_5 not "
             "re-derived here")],
  useful_for=["impossibility proofs", "class field theory",
              "elliptic-curve crypto", "BCH codes"]),

 dict(id=57, key="LEBESGUE", name="Lebesgue Measure Theory",
  origin="Lebesgue (1902); Borel (1898)",
  V="sigma-algebras with countably additive measure",
  G="integrate by partitioning the RANGE; Radon-Nikodym densities",
  theta="sigma-finiteness; completeness of L^p",
  insight=("Integration turned sideways: slice function values, not the "
           "domain, and the pathological becomes tame — the indicator "
           "of the rationals integrates to 0 because countable sets "
           "vanish under any epsilon of covering."),
  forces=[
   dict(claim="monotone convergence exhibited; the rationals covered "
              "by total length < any epsilon, exactly",
        check="lebesgue_convergence_instance")],
  breaks=[
   dict(claim="non-measurable sets under AC (Vitali, Banach-Tarski)",
        cite="Vitali 1905; PRESUMED — requires choice, definitionally "
             "beyond construction"),
   dict(claim="conditionally convergent improper integrals lost",
        cite="sin(x)/x on [0,oo); standard")],
  useful_for=["probability foundations", "L^2 Fourier theory",
              "weak PDE solutions", "stochastic integration"]),

 dict(id=58, key="ITO", name="Stochastic Calculus (Ito)",
  origin="Kiyosi Ito (1944, 1951)",
  V="adapted processes on filtered probability spaces",
  G="the Ito integral (left endpoints, non-anticipating); Ito's lemma",
  theta="quadratic variation [W,W]_t = t",
  insight=("Brownian paths carry area at first order — (dW)^2 = dt — so "
           "the chain rule must pay a second-derivative tax. The "
           "library MEASURES it: quadratic variation lands on t and "
           "W^2 - t sits flat, as the correction demands."),
  forces=[
   dict(claim="quadratic variation = t, W^2-t a martingale, isometry — "
              "1500 paths, 4-sigma bounds from measured spread",
        check="ito_quadratic_variation")],
  breaks=[
   dict(claim="the naive chain rule fails; Stratonovich buys it back "
              "at the cost of anticipation",
        cite="Ito 1951; Stratonovich 1966; PRESUMED as the general "
             "theorems — the failing instance is what the check measures")],
  useful_for=["Black-Scholes", "Langevin/Fokker-Planck",
              "Kalman filtering", "stochastic control"]),

 dict(id=59, key="EXTERIOR", name="Exterior Algebra & Differential Forms",
  origin="Grassmann (1844); Cartan (1899); de Rham (1931)",
  V="antisymmetric multilinear k-forms",
  G="wedge product; exterior derivative d",
  theta="d^2 = 0 — the nilpotency identity",
  insight=("Symmetric second partials meet antisymmetric wedges and "
           "cancel identically: d^2=0 is bookkeeping, not physics. "
           "Stokes then unifies every classical integral theorem into "
           "one equation, and the failures of local-to-global exactness "
           "are precisely the holes."),
  forces=[
   dict(claim="d(d omega) = 0 symbolically for a random polynomial "
              "1-form; Stokes on the unit square, exactly",
        check="exterior_d_squared_zero")],
  breaks=[
   dict(claim="closed but non-exact forms live on holes (H^1 of the "
              "circle)", cite="de Rham; the homology carrier computes "
              "the hole count executably")],
  useful_for=["Maxwell in two lines", "GR in form language",
              "de Rham cohomology"]),

 dict(id=60, key="LIE", name="Lie Groups & Lie Algebras",
  origin="Lie (1870s); Killing (1888); Cartan (1894)",
  V="smooth groups; tangent algebra at the identity",
  G="bracket [X,Y]; exponential map",
  theta="non-degeneracy of the Killing form",
  insight=("Continuous symmetry differentiated: the bracket measures "
           "how flows fail to commute, exp reassembles the group from "
           "its germs, and Cartan's list of simple algebras is the "
           "periodic table of symmetry."),
  forces=[
   dict(claim="so(3): antisymmetry + Jacobi for all 27 basis triples, "
              "exactly; exp is a one-parameter homomorphism",
        check="lie_so3_jacobi")],
  breaks=[
   dict(claim="the algebra fixes the group only locally: SO(3) vs "
              "SU(2)", cite="double cover; PRESUMED — global topology "
              "outruns the tangent space")],
  useful_for=["gauge symmetry", "robotics (SO(3)/SE(3))",
              "symmetry reduction of ODEs"]),

 dict(id=61, key="HOMOLOGY", name="Algebraic Topology (Singular Homology)",
  origin="Poincare (1895); Eilenberg-Steenrod (1945)",
  V="chain complexes over spaces",
  G="boundary maps with d.d = 0; induced maps",
  theta="Betti numbers",
  insight=("Holes counted by linear algebra: cycles that bound nothing "
           "are the voids. The library computes them: boundary-of-"
           "boundary is the zero matrix, the circle scores (1,1), the "
           "tetrahedral sphere (1,0,1)."),
  forces=[
   dict(claim="d.d = 0 exactly; Betti numbers of circle and sphere by "
              "rank computation", check="homology_circle_sphere")],
  breaks=[
   dict(claim="homology is not a complete invariant (lens spaces); "
              "higher homotopy sees more",
        cite="Whitehead, lens space classification; PRESUMED")],
  useful_for=["persistent homology / TDA", "topological phases",
              "configuration spaces"]),

 dict(id=62, key="CONVEX", name="Convex Analysis (KKT & Fenchel)",
  origin="Fenchel (1949); Kuhn-Tucker (1951); Rockafellar (1970)",
  V="convex sets and functions",
  G="subgradients; conjugation; Lagrangian duality",
  theta="zero duality gap (Slater)",
  insight=("The geometry where local honesty is global truth: every "
           "minimum is THE minimum, optimality certificates come as "
           "multipliers, and conjugating twice hands the function back "
           "unchanged."),
  forces=[
   dict(claim="KKT solved exactly on a QP: multiplier nonneg, "
              "complementary slackness zero; f** = f for x^2",
        check="convex_kkt_fenchel")],
  breaks=[
   dict(claim="non-convexity demotes KKT to necessary-only",
        cite="standard; local minima return")],
  useful_for=["SVM/LASSO", "conic programming", "compressed sensing",
              "MPC"]),

 dict(id=63, key="SYMPLECTIC", name="Symplectic Geometry (Hamiltonian)",
  origin="Lagrange (1808); Hamilton (1833); Arnold (1974)",
  V="even-dimensional phase space with a closed 2-form",
  G="Hamiltonian flows; Poisson bracket",
  theta="Liouville volume preservation",
  insight=("Mechanics as geometry: the bracket runs the dynamics, "
           "symmetries become conserved quantities by Noether's "
           "dictionary, and phase-space volume is incompressible — "
           "which the discrete symplectic map honors with determinant "
           "exactly one."),
  forces=[
   dict(claim="bracket antisymmetry + Jacobi symbolically; symplectic "
              "Euler Jacobian det = 1 EXACTLY; energy conserved",
        check="symplectic_liouville_poisson")],
  breaks=[
   dict(claim="dissipation cannot be Hamiltonian; no-go for full "
              "quantization (Groenewold-van Hove)",
        cite="Groenewold 1946; PRESUMED")],
  useful_for=["integrable systems", "geometric integrators",
              "canonical quantization", "ray optics"]),

 dict(id=64, key="SURREAL", name="Surreal Numbers (Conway)",
  origin="Conway (1976); Knuth (1974)",
  V="games {L|R} with no left option >= any right option",
  G="recursive addition, negation, multiplication; simplicity rule",
  theta="birthday — earlier is simpler is canonical",
  insight=("Numbers born from nothing by a single recursion, ordered by "
           "one comparison rule. The library runs day 0 through 2: "
           "{0|1}+{0|1}=1 and 1+(-1)=0 fall out of the game order "
           "alone, no field axioms invoked."),
  forces=[
   dict(claim="Conway arithmetic on finite birthdays: half+half=1, "
              "additive inverses cancel, 1+1={1|}",
        check="surreal_birthdays")],
  breaks=[
   dict(claim="No is a proper class — ZFC cannot hold it as one object",
        cite="Conway 1976; PRESUMED")],
  useful_for=["combinatorial game theory", "alternative infinitesimals",
              "the maximal ordered field"]),
]

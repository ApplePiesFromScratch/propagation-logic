"""carriers.physics — 4 carriers."""

CARRIERS = [
 dict(id=51, key="DRAS_SCALE", name="DRAS Scale Carrier (Renormalization Group)",
  origin="Wilson (1971); Callan-Symanzik; DRAS formalism (Pugmire 2026)",
  V="(coupling, scale, load)",
  G="running of the coupling with ln E; beta function",
  theta="the Landau pole — load diverges as the denominator dies",
  insight=("Couplings are functions of the zoom level. The one-loop "
           "running composes as an exact group in ln E, shrinking "
           "couplings are asymptotically free, and the growing branch "
           "hits its pole precisely where the algebra says it must — "
           "decoherence as divergence, measured."),
  forces=[
   dict(claim="group law in ln E exact to 1e-12; asymptotic-freedom "
              "direction confirmed; pole located and hit",
        check="dras_scale_group_law")],
  breaks=[
   dict(claim="Landau pole in QED/phi^4 signals breakdown, not physics",
        cite="Landau 1955; triviality results; PRESUMED beyond the toy")],
  useful_for=["QCD asymptotic freedom", "critical phenomena",
              "effective field theory"]),

 dict(id=52, key="THERMO", name="Thermodynamic Carrier (Entropy / Landauer)",
  origin="Carnot (1824); Clausius; Boltzmann; Landauer (1961); Berut (2012)",
  V="(S, E, N, V) or phase-space distributions",
  G="Hamiltonian flow; entropy ascent; bit erasure",
  theta="k_B T — and k_B T ln 2 per erased bit",
  insight=("Information is physical: forgetting one bit costs at least "
           "kT ln 2 of heat, which is Maxwell's demon's invoice. The "
           "measurable core of the second law — relative entropy to "
           "equilibrium never increasing — is verified here at every "
           "step of every random chain tried."),
  forces=[
   dict(claim="Landauer bill at 300K = 2.87e-21 J, exact arithmetic; "
              "Markov H-theorem held at every step, 30 random chains",
        check="landauer_and_h_theorem")],
  breaks=[
   dict(claim="local entropy dips in small systems (fluctuation "
              "theorems)", cite="Evans-Searles; Jarzynski; PRESUMED")],
  useful_for=["thermodynamics of computation", "demon exorcism",
              "energy floors for AI"]),

 dict(id=53, key="GR", name="General Relativity (Manifold Carrier)",
  origin="Einstein (1915); Riemann (1854)",
  V="Lorentzian manifolds with metric g",
  G="covariant derivative; Einstein equations G = 8 pi T",
  theta="curvature scale; singularities where it diverges",
  insight=("Gravity as geometry: free fall is a straight line in a "
           "curved book-keeping. The daily-life number is computed here "
           "— GPS clocks gain ~38 microseconds a day from the "
           "weak-field arithmetic, or the map drifts kilometers."),
  forces=[
   dict(claim="GPS time dilation: +45.7 gravitational, -7.2 velocity, "
              "net ~38.5 us/day from the weak-field formulas",
        check="gr_gps_time_dilation"),
   dict(claim="Bianchi identity = energy-momentum conservation",
        cite="Einstein 1915; differential-geometric identity; PRESUMED")],
  breaks=[
   dict(claim="singularities: the theory predicts its own edge",
        cite="Penrose 1965, Hawking; PRESUMED"),
   dict(claim="incompatible with QM at the Planck scale",
        cite="the open problem of quantum gravity; PRESUMED")],
  useful_for=["GPS corrections", "black holes", "LIGO", "cosmology"]),

 dict(id=54, key="QFT", name="Quantum Field Theory (Fock Space)",
  origin="Dirac (1927); Feynman, Schwinger, Tomonaga (1940s)",
  V="Fock space — superpositions of any particle number",
  G="creation/annihilation; path integral; renormalization group",
  theta="UV cutoff; renormalizability as finite load per order",
  insight=("Particles as excitations of fields. The free-field engine "
           "is Wick's theorem — correlators are sums over pairings — "
           "and the library computes its smallest instances exactly: "
           "E[x^4] = 3 sigma^4 because three is the number of pairings, "
           "symbolically, combinatorially, and by Monte Carlo."),
  forces=[
   dict(claim="Wick on the Gaussian: 4th and 6th moments match the "
              "(2n-1)!! pairing count, symbolic + MC",
        check="qft_wick_gaussian")],
  breaks=[
   dict(claim="loop divergences need renormalization; gravity is "
              "non-renormalizable", cite="'t Hooft-Veltman; PRESUMED")],
  useful_for=["the Standard Model", "QED precision", "BCS theory"]),
]

"""carriers.interpretations — 6 carriers.

The most citation-heavy section in the library, on purpose: these
carriers differ precisely where experiment does not reach, so their
distinctive claims are PRESUMED philosophy and priced that way. What
they SHARE — the Born statistics — is computed once, exactly, and every
record points at it."""

CARRIERS = [
 dict(id=78, key="COPENHAGEN", name="Copenhagen Interpretation",
  origin="Bohr (1927); Heisenberg (1927)",
  V="quantum state before, classical outcome after; nothing between",
  G="unitary evolution, then primitive projective collapse",
  theta="the Heisenberg cut — deliberately unspecified",
  insight=("Quantum mechanics as a theory of measurement outcomes, with "
           "the between-times question ruled out of order. It runs the "
           "lab perfectly and declines the ontology on principle."),
  forces=[
   dict(claim="the Born statistics — the shared empirical core, "
              "computed exactly on the qubit instance",
        check="born_rule_shared_instance"),
   dict(claim="complementarity: conjugate observables never jointly "
              "definite", cite="Bohr 1928; PRESUMED")],
  breaks=[
   dict(claim="no mechanism or location for the cut (the measurement "
              "problem)", cite="Bell, 'Against Measurement' 1990; PRESUMED"),
   dict(claim="macroscopic superpositions undefined (the cat)",
        cite="Schrodinger 1935; PRESUMED")],
  useful_for=["working-physicist default", "state prep and readout",
              "spectroscopy"]),

 dict(id=79, key="MWI", name="Many-Worlds Interpretation (Everett)",
  origin="Everett (1957); DeWitt (1970)",
  V="one universal wavefunction; branches via decoherence",
  G="unitary evolution ONLY — measurement is entanglement",
  theta="decoherence time — when branches stop interfering",
  insight=("Delete the collapse postulate and keep the books: "
           "measurement entangles, decoherence separates, every outcome "
           "persists in its branch. The library runs the bookkeeping — "
           "norm exactly preserved, Born weights intact on both "
           "branches, nothing collapsed."),
  forces=[
   dict(claim="premeasurement as a unitary: norm preserved, both "
              "outcomes persist with cos^2/sin^2 weights",
        check="mwi_unitarity_no_collapse"),
   dict(claim="shared Born statistics", check="born_rule_shared_instance")],
  breaks=[
   dict(claim="the Born rule must be DERIVED, and the derivations "
              "(Deutsch-Wallace, envariance) remain contested",
        cite="Wallace 2012; Adlam and critics; PRESUMED"),
   dict(claim="branch structure only approximate",
        cite="Zurek pointer bases; PRESUMED")],
  useful_for=["quantum cosmology", "decoherence theory",
              "entanglement without collapse"]),

 dict(id=80, key="BOHM", name="Pilot Wave Theory (de Broglie-Bohm)",
  origin="de Broglie (1927); Bohm (1952)",
  V="wavefunction PLUS actual particle positions",
  G="Schrodinger for the wave; the guiding equation for the particles",
  theta="quantum equilibrium: initial rho = |psi|^2",
  insight=("Determinism restored by doubling the ontology: the wave "
           "guides, the particles ride, and Born statistics follow from "
           "an equilibrium hypothesis the dynamics preserves. Collapse "
           "becomes mere selection of the occupied branch."),
  forces=[
   dict(claim="shared Born statistics (given quantum equilibrium)",
        check="born_rule_shared_instance"),
   dict(claim="equivariance: rho = |psi|^2 preserved for all time",
        cite="Bohm 1952; Durr-Goldstein-Zanghi 1992; PRESUMED")],
  breaks=[
   dict(claim="explicit nonlocality; a preferred foliation in tension "
              "with relativity", cite="Bell's theorem makes the "
              "nonlocality mandatory; PRESUMED"),
   dict(claim="empty branches persist as real",
        cite="Bohm 1952; the ontological bill")],
  useful_for=["EPR/Bell analysis with a mechanism",
              "quantum trajectories intuition"]),

 dict(id=81, key="HISTORIES", name="Consistent Histories",
  origin="Griffiths (1984); Gell-Mann & Hartle (1990); Omnes (1992)",
  V="families of projector sequences (histories)",
  G="the decoherence functional; probabilities inside consistent families",
  theta="consistency: off-diagonal decoherence functional = 0",
  insight=("Probability without observers: a family of histories earns "
           "classical probability exactly when its interference terms "
           "vanish. The library computes a full 16-pair decoherence "
           "functional and watches the condition hold and the "
           "probabilities turn Kolmogorov."),
  forces=[
   dict(claim="off-diagonals exactly zero for the same-basis qubit "
              "family; diagonal probabilities additive and Born",
        check="consistent_histories_qubit")],
  breaks=[
   dict(claim="no rule selects among incompatible consistent "
              "frameworks; cross-framework inference forbidden",
        cite="Griffiths' single-framework rule; Dowker-Kent 1996; "
             "PRESUMED")],
  useful_for=["closed-system QM", "quantum cosmology",
              "decoherence analysis"]),

 dict(id=82, key="GRW", name="Objective Collapse (GRW / Penrose OR)",
  origin="Ghirardi-Rimini-Weber (1986); Penrose (1989)",
  V="wavefunctions subject to spontaneous stochastic localization",
  G="Schrodinger plus random Gaussian hits at rate lambda per particle",
  theta="lambda ~ 1e-16 /s and width ~ 1e-7 m — tuned so micro stays "
        "quantum and macro snaps",
  insight=("Make collapse physics: one tiny per-particle rate, "
           "amplified by particle count. A dust grain's superposition "
           "dies in microseconds while an electron's lives for eons — "
           "and the N-scaling of survival is exactly what the library "
           "simulates."),
  forces=[
   dict(claim="first-hit survival scales as 1/(N lambda) across a "
              "1000x range of N", check="grw_rate_scaling"),
   dict(claim="shared Born statistics FAPP", check="born_rule_shared_instance")],
  breaks=[
   dict(claim="slight energy non-conservation per hit; no complete "
              "relativistic version; no experimental discrimination yet",
        cite="GRW 1986; CSL literature; ongoing optomechanics tests; "
             "PRESUMED and honestly undecided")],
  useful_for=["mesoscopic superposition experiments",
              "measurement-problem dissolution proposals"]),

 dict(id=83, key="RELATIONAL", name="Relational Quantum Mechanics (Rovelli)",
  origin="Rovelli (1996)",
  V="states defined only RELATIVE to an observing system",
  G="interactions actualize relative facts",
  theta="the interaction event",
  insight=("Special relativity's move replayed on the quantum state: no "
           "observer-independent state, only relations. Wigner and his "
           "friend stop contradicting each other because their "
           "descriptions were never required to be one description."),
  forces=[
   dict(claim="shared Born statistics within each observer's account",
        check="born_rule_shared_instance"),
   dict(claim="internal consistency of each perspective",
        cite="Rovelli 1996; PRESUMED")],
  breaks=[
   dict(claim="cross-perspective facts require care; correlations "
              "taken as primitive",
        cite="Frauchiger-Renner adjacent debates; PRESUMED")],
  useful_for=["loop quantum gravity", "quantum reference frames",
              "Bell without absolutes"]),
]

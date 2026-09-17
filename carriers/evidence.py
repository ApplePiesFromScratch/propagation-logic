"""carriers.evidence — 6 carriers."""

CARRIERS = [
 dict(id=73, key="KOLMOGOROV", name="Kolmogorov Probability Theory",
  origin="Kolmogorov (1933)",
  V="probability spaces (Omega, F, P)",
  G="conditioning; expectation; independence",
  theta="P(Omega)=1 and sigma-additivity — the whole axiom bill",
  insight=("Probability as measure: two axioms, and Bayes, total "
           "probability, and monotonicity fall out as arithmetic — "
           "verified here on fifty random finite spaces where nothing "
           "extra could hide."),
  forces=[
   dict(claim="Bayes, total probability, monotonicity as pure "
              "arithmetic of the measure — 50 random spaces",
        check="kolmogorov_axioms_to_bayes")],
  breaks=[
   dict(claim="conditioning on measure-zero events undefined without "
              "regular versions", cite="Kolmogorov 1933; standard"),
   dict(claim="one measure cannot express ignorance — see the "
              "imprecise carrier", cite="motivating Walley 1991")],
  useful_for=["statistics", "stochastic processes", "finance"]),

 dict(id=74, key="BAYES", name="Bayesian Probability (Prior-Posterior)",
  origin="Bayes (1763); Laplace (1812); de Finetti (1937)",
  V="coherent degrees of belief over hypotheses",
  G="Bayes updating; Jeffrey conditionalization",
  theta="coherence — or a Dutch book exists",
  insight=("Belief with a solvency requirement: incoherent credences "
           "are a purchasable loss, and the library constructs the "
           "purchase. Sequential and joint updating provably coincide — "
           "run on thirty random cases — so evidence order cannot be "
           "gamed."),
  forces=[
   dict(claim="sequential = joint updating on 30 random cases; the "
              "Dutch book against P(A)=P(~A)=0.6 constructed: +0.20 "
              "guaranteed", check="bayes_sequential_and_dutch_book"),
   dict(claim="posteriors converge to the truth (Bernstein-von Mises)",
        cite="regularity conditions apply; PRESUMED")],
  breaks=[
   dict(claim="prior sensitivity with scarce data; no universal "
              "uninformative prior", cite="Jeffreys, Bernardo; standard")],
  useful_for=["ML", "diagnosis", "A/B testing", "spam filtering"]),

 dict(id=75, key="DEMPSTER_SHAFER", name="Dempster-Shafer Evidence Theory",
  origin="Dempster (1967); Shafer (1976)",
  V="basic probability assignments over SETS of hypotheses",
  G="Dempster's combination rule, normalizing conflict away",
  theta="the belief-plausibility interval",
  insight=("Ignorance finally distinguishable from uniform uncertainty: "
           "mass on a set means 'one of these, cannot say which'. The "
           "famous failure is computed exactly — two doctors 99% sure "
           "of DIFFERENT diseases combine to certainty in the one "
           "neither believed."),
  forces=[
   dict(claim="Bel <= Pl; vacuous BPA yields [0,1]; classical "
              "probability recovered on singletons",
        check="dempster_shafer_zadeh")],
  breaks=[
   dict(claim="Zadeh's paradox computed: 0.99/0.99 conflict "
              "normalizes to 100% tumor", check="dempster_shafer_zadeh"),
   dict(claim="independence of sources assumed by the rule",
        cite="Shafer 1976; standard caveat")],
  useful_for=["sensor fusion", "expert systems", "forensic combination"]),

 dict(id=76, key="POSSIBILITY", name="Possibility Theory (Zadeh/Dubois-Prade)",
  origin="Zadeh (1978); Dubois & Prade (1988)",
  V="possibility distributions, sup-normalized",
  G="Pi maxitive over unions; necessity by duality",
  theta="normalization: something is fully possible",
  insight=("Additivity swapped for max: the possibility of a union is "
           "its best member, so A and not-A can both be fully possible "
           "at once — which is exactly what not-knowing looks like, and "
           "what a probability measure cannot say."),
  forces=[
   dict(claim="maxitivity enumerated; N(A) = 1 - Pi(~A) duality; the "
              "vacuous distribution expresses ignorance",
        check="possibility_maxitive")],
  breaks=[
   dict(claim="probability-possibility transforms are not unique",
        cite="Dubois-Prade-Sandri 1993; PRESUMED")],
  useful_for=["fuzzy control", "linguistic vagueness",
              "deep-uncertainty risk"]),

 dict(id=77, key="IMPRECISE", name="Imprecise Probability (Credal Sets)",
  origin="Walley (1991); Kuznetsov (1991)",
  V="convex sets of probability measures",
  G="robust Bayes: update every member; natural extension",
  theta="the credal set — singleton means classical, everything means ignorance",
  insight=("When the model itself is uncertain, carry the whole set. "
           "The library constructs the theory's most counterintuitive "
           "honest moment: DILATION, where observing evidence widens "
           "the interval from a point to [0.2, 0.8] — learning that you "
           "know less than you thought."),
  forces=[
   dict(claim="conjugacy P_*(A) + P^*(~A) = 1; dilation constructed "
              "and exhibited", check="imprecise_credal_dilation")],
  breaks=[
   dict(claim="decision theory goes set-valued; inference can be "
              "NP-hard in extreme points",
        cite="Walley 1991; de Campos et al.; PRESUMED")],
  useful_for=["robust statistics", "credal networks",
              "sensitivity analysis"]),

 dict(id=85, key="BOUNDARY_LAW", name="Distinction Cost (The Boundary Law)",
  origin="distinction.py (2026); Chernoff/Hoeffding; Shannon (1948)",
  V="pairs of hypotheses separated by a gap, under noise",
  G="repeated noisy probing; redundancy against error",
  theta="confidence 1 - delta",
  insight=("What a distinction costs to maintain: not the distance "
           "between the values but the looks needed to be sure, which "
           "scales as 1/gap^2. The near-boundary call is the expensive "
           "one — the medical test at threshold, the speed camera at "
           "the limit — and the library measures the exponent."),
  forces=[
   dict(claim="sample count scales as 1/gap^2 (log-log slope ~2 across "
              "a gap halving) and lands the formula's order of "
              "magnitude", check="boundary_law_scaling")],
  breaks=[
   dict(claim="exponents are per-system in native load units; "
              "universality NOT claimed", tier="STIPULATED",
        cite="declared by the source carrier itself"),
   dict(claim="Gaussian noise modeled; heavy tails can change the "
              "exponent", cite="stated scope")],
  useful_for=["sample-size planning", "code-redundancy design",
              "A/B tests near a decision boundary", "bandit exploration"]),
]

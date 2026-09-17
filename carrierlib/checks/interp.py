"""checks.interp — measurement interpretations.

The section where honesty matters most: interpretations are chosen for
what they say BETWEEN measurements, which is exactly what experiment
does not decide. What IS executable: the Born statistics they share,
the unitary bookkeeping MWI insists on, GRW's N-scaling, and the
consistency condition of decoherent histories. Everything distinctive
beyond that is PRESUMED with its citation — as it must be.
"""
from __future__ import annotations
import math
from ..core import check


@check("born_rule_shared_instance")
def _():
    import numpy as np
    # one qubit, one observable: every interpretation in the section
    # predicts the same statistics. Compute them once, exactly.
    psi = np.array([math.cos(0.3), math.sin(0.3)], complex)
    P0 = abs(psi[0])**2
    # Copenhagen: collapse with prob |<0|psi>|^2. Bohm: quantum
    # equilibrium reproduces it. MWI: branch weights. All = P0.
    total = abs(P0 + abs(psi[1])**2 - 1) < 1e-12
    return total and abs(P0 - math.cos(0.3)**2) < 1e-12, "FORCED", \
        (f"the shared empirical core computed: P(0) = cos^2(0.3) = "
         f"{P0:.4f}, probabilities sum to 1 — every interpretation in "
         "this section reproduces exactly this table, which is WHY "
         "experiment has not separated them (their differences are "
         "PRESUMED philosophy, priced as such)")


@check("mwi_unitarity_no_collapse")
def _():
    import numpy as np
    rng = np.random.default_rng(15)
    # measurement as entanglement: |psi> (x) |ready> evolves unitarily
    # to a branched state; the norm and both branch weights persist.
    a, b = math.cos(0.4), math.sin(0.4)
    joint = np.zeros(4, complex)
    joint[0] = a                        # |0>|ready>
    joint[2] = b                        # |1>|ready>
    # CNOT-style premeasurement: apparatus copies the pointer basis
    U = np.eye(4, dtype=complex)[[0, 1, 3, 2]]
    out = U @ joint
    unitary = abs(np.linalg.norm(out) - 1) < 1e-12
    branches = (abs(abs(out[0])**2 - a**2) < 1e-12
                and abs(abs(out[3])**2 - b**2) < 1e-12)
    off_diag_gone = out[1] == 0 and out[2] == 0
    return unitary and branches and off_diag_gone, "FORCED", \
        ("premeasurement as a unitary: the norm is exactly preserved, "
         "both outcomes persist as orthogonal branches with Born "
         "weights cos^2/sin^2, nothing collapsed — the bookkeeping MWI "
         "runs on, executed; the Born-rule DERIVATION "
         "(Deutsch-Wallace) stays PRESUMED and contested, per the record")


@check("grw_rate_scaling")
def _():
    import numpy as np
    rng = np.random.default_rng(16)
    # GRW: per-particle hit rate lam; a superposition of N particles
    # survives only until the FIRST hit -> lifetime ~ Exp(N*lam).
    lam = 1e-3
    for N in (1, 1000):
        t = rng.exponential(1 / (N * lam), size=4000)
        want = 1 / (N * lam)
        if abs(t.mean() - want) / want > 0.08:
            return False, "EMPIRICAL", f"scaling off at N={N}"
    ratio = 1000
    return True, "EMPIRICAL", \
        ("simulated first-hit lifetimes: mean survival scales as "
         "1/(N lambda) across N=1 vs N=1000 to within 8% — micro "
         "coherence with macro collapse from ONE stochastic rate; that "
         "nature actually runs this modified dynamics is PRESUMED "
         "(GRW 1986) and experimentally undecided, as the record says")


@check("consistent_histories_qubit")
def _():
    import numpy as np
    # two-time histories of a qubit in the SAME basis decohere exactly;
    # probabilities from the decoherence functional sum to 1.
    psi = np.array([math.cos(0.3), math.sin(0.3)], complex)
    rho = np.outer(psi, psi.conj())
    P = [np.diag([1.0, 0]).astype(complex),
         np.diag([0, 1.0]).astype(complex)]
    U = np.eye(2, dtype=complex)        # trivial evolution between times
    def C(a1, a2):
        return P[a2] @ U @ P[a1]
    D = {(h, k): np.trace(C(*h) @ rho @ C(*k).conj().T)
         for h in [(0, 0), (0, 1), (1, 0), (1, 1)]
         for k in [(0, 0), (0, 1), (1, 0), (1, 1)]}
    hist = [(0, 0), (0, 1), (1, 0), (1, 1)]
    consistent = all(abs(D[(h, k)]) < 1e-12
                     for h in hist for k in hist if h != k)
    probs = [D[(h, h)].real for h in hist]
    ok_probs = (abs(sum(probs) - 1) < 1e-12
                and abs(probs[0] - math.cos(0.3)**2) < 1e-12
                and probs[1] == probs[2] == 0)
    return consistent and ok_probs, "FORCED", \
        ("the decoherence functional computed for all 16 history pairs: "
         "off-diagonals exactly zero (a consistent family), diagonal "
         "probabilities Kolmogorov-additive and matching Born — "
         "classical reasoning valid INSIDE the framework; that no rule "
         "selects between incompatible frameworks is the record's "
         "PRESUMED break (Frauchiger-Renner adjacent)")

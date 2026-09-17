"""checks.physics — the four physics carriers, priced honestly."""
from __future__ import annotations
import math
from ..core import check


@check("dras_scale_group_law")
def _():
    # G_scale: v' = v / (1 + beta * dlnE), load += |beta * dlnE|.
    # The gradient composes as a group action in dlnE at leading order,
    # and for beta > 0 the running hits a Landau pole in finite dlnE.
    beta = 0.5
    def run(v, dln):                    # exact one-loop-style running
        return v / (1 + beta * v * dln)
    v0 = 0.3
    a = run(run(v0, 0.4), 0.6)
    b = run(v0, 1.0)
    group = abs(a - b) < 1e-12
    # Landau pole for beta<0 convention (coupling GROWS toward the pole):
    g = lambda v, dln: v / (1 - beta * v * dln)
    pole_at = 1 / (beta * v0)           # dlnE where denominator hits 0
    near = g(v0, pole_at * 0.999)
    blown = near > 100 * v0
    # asymptotic freedom direction: coupling shrinks at higher scales
    af = run(v0, 5.0) < v0
    return group and blown and af, "FORCED", \
        (f"one-loop running composes exactly as a group in ln E "
         f"(0.4 then 0.6 = 1.0, to 1e-12); growing-coupling branch "
         f"blows up at the predicted pole ln E = 1/(beta v0) = "
         f"{pole_at:.2f} (value x{near/v0:.0f} just below it); "
         "shrinking branch is asymptotically free — decoherence as divergence")


@check("landauer_and_h_theorem")
def _():
    import numpy as np
    # Landauer: erasing one bit at T costs >= kT ln 2 — arithmetic of
    # the entropy ledger on the two-state instance.
    k, T = 1.380649e-23, 300.0
    dS_bit = k * math.log(2)
    cost = T * dS_bit
    landauer = abs(cost - 2.87e-21) / 2.87e-21 < 0.01
    # H-theorem for Markov chains: relative entropy to the stationary
    # distribution is non-increasing under the chain — checked on 30
    # random chains, every step.
    rng = np.random.default_rng(9)
    ok = True
    for _ in range(30):
        P = rng.dirichlet(np.ones(4), size=4)      # rows sum to 1
        # stationary distribution:
        w, V = np.linalg.eig(P.T)
        pi = np.real(V[:, np.argmin(np.abs(w - 1))])
        pi = np.abs(pi) / np.abs(pi).sum()
        q = rng.dirichlet(np.ones(4))
        def D(a, b):
            m = a > 1e-15
            return float((a[m] * np.log(a[m] / b[m])).sum())
        for _ in range(25):
            q2 = q @ P
            ok &= D(q2, pi) <= D(q, pi) + 1e-10
            q = q2
    return landauer and ok, "EMPIRICAL", \
        ("kT ln2 at 300K = 2.87e-21 J per erased bit (the arithmetic, "
         "exact); relative entropy to stationarity was non-increasing "
         "at EVERY step of 25 steps x 30 random 4-state Markov chains — "
         "the H-theorem, measured where it is a theorem")


@check("gr_gps_time_dilation")
def _():
    # The number GR is famous for earning daily: GPS clock drift.
    # Gravitational blueshift of the satellite clock minus special-
    # relativistic time dilation, in microseconds per day.
    G = 6.67430e-11
    M = 5.9722e24
    c = 299792458.0
    R_earth = 6.371e6
    r_orbit = 2.6571e7                  # GPS semi-major axis (m)
    v = math.sqrt(G * M / r_orbit)      # orbital speed
    grav = (G * M / c**2) * (1 / R_earth - 1 / r_orbit)   # clock runs fast
    vel = 0.5 * v**2 / c**2                                # clock runs slow
    net_us_day = (grav - vel) * 86400 * 1e6
    ok = 37.0 < net_us_day < 40.0
    return ok, "FORCED", \
        (f"weak-field GR arithmetic: gravitational +{grav*86400*1e6:.1f} "
         f"us/day, velocity -{vel*86400*1e6:.1f} us/day, net "
         f"+{net_us_day:.1f} us/day — the ~38 us/day GPS must correct "
         "or drift ~11 km/day; field equations themselves PRESUMED (Einstein 1915)")


@check("qft_wick_gaussian")
def _():
    import numpy as np
    import sympy as sp
    # Wick's theorem on the simplest instance: for a centered Gaussian,
    # E[x^4] = 3 sigma^4 (three pairings), E[x^6] = 15 sigma^6.
    x, s = sp.symbols("x sigma", positive=True)
    p = sp.exp(-x**2 / (2 * s**2)) / (s * sp.sqrt(2 * sp.pi))
    m4 = sp.simplify(sp.integrate(x**4 * p, (x, -sp.oo, sp.oo)))
    m6 = sp.simplify(sp.integrate(x**6 * p, (x, -sp.oo, sp.oo)))
    exact = (sp.simplify(m4 - 3 * s**4) == 0
             and sp.simplify(m6 - 15 * s**6) == 0)
    # and the pairing count IS the combinatorics: (2n-1)!! pairings
    dfact = lambda n: math.prod(range(n, 0, -2))
    combinatorial = dfact(3) == 3 and dfact(5) == 15
    # Monte Carlo agreement:
    rng = np.random.default_rng(11)
    z = rng.normal(0, 2.0, size=400000)
    mc = abs((z**4).mean() - 3 * 16) / (3 * 16) < 0.02
    return exact and combinatorial and mc, "FORCED", \
        ("Wick on the Gaussian: E[x^4]=3 sigma^4 and E[x^6]=15 sigma^6 "
         "integrated symbolically, exactly matching the (2n-1)!! pairing "
         "count, cross-checked by Monte Carlo to 2% — free-field "
         "correlators are pairings; interacting QFT (LSZ, "
         "renormalization) PRESUMED (Feynman/Schwinger/Tomonaga)")

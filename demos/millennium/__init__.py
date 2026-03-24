"""
demos/millennium — Propagation Logic and the Millennium Problems

The Millennium Problems are the seven problems identified by the Clay
Mathematics Institute in 2000. PL provides a unified structural
analysis of each: every problem, when re-described in propagation
terms, reduces to a question about load, coherence, gradient demand,
or fixed points of the mechanism.

This is not a claim that PL solves these problems. It is a claim that
the PL framing reveals the structural skeleton each problem shares
with the others — and with Gödel incompleteness (Section 8.4) and the
paradoxes of Section 10. The mechanism is prior to the cut that
produces the classical formulations. The Millennium Problems are
statements about boundary conditions visible only from inside their
respective carrier settings.

Files:
  riemann.py       — Riemann Hypothesis: zeros on the critical line
  p_vs_np.py       — P vs NP: load asymmetry in computation
  navier_stokes.py — Navier-Stokes: self-referential fluid propagation
  yang_mills.py    — Yang-Mills mass gap: minimum excited-state load
  hodge.py         — Hodge Conjecture: algebraic reachability of harmonics
  bsd.py           — Birch-Swinnerton-Dyer: rank as propagation dimension
  run_all.py       — Run all six demos

Poincare Conjecture (solved by Perelman, 2003):
  Ricci flow is a reconfiguration gradient field. A simply-connected
  3-manifold is one with zero topological load. Ricci flow reduces any
  such manifold to the minimum-load (spherical) state. Perelman's proof
  shows that reconfiguration always reaches coherence in this carrier.
  No separate demo — the result is proven.
"""

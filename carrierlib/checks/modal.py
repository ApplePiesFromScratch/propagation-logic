"""checks.modal — every axiom decided over ALL frames up to 3 worlds."""
from __future__ import annotations
from ..core import check
from ..finite import (modal_forced, reflexive, transitive, symmetric,
                      serial, irreflexive, equivalence, any_frame,
                      ltl_valid)

P, Q = ('p', 0), ('p', 1)
N = lambda f: ('nec', f)
Ps = lambda f: ('pos', f)
IMP = lambda a, b: ('imp', a, b)
AND = lambda a, b: ('and', a, b)
NOT = lambda a: ('not', a)

K_AX = IMP(N(IMP(P, Q)), IMP(N(P), N(Q)))
T_AX = IMP(N(P), P)
FOUR = IMP(N(P), N(N(P)))
FIVE = IMP(Ps(P), N(Ps(P)))
B_AX = IMP(P, N(Ps(P)))
LOB = IMP(N(IMP(N(P), P)), N(P))
DUAL = IMP(Ps(P), NOT(N(NOT(P))))


@check("K_axiom_all_frames")
def _():
    ok, _ = modal_forced(K_AX, any_frame)
    ok2, _ = modal_forced(DUAL, any_frame, nprops=1)
    dist, _ = modal_forced(IMP(N(AND(P, Q)), AND(N(P), N(Q))), any_frame)
    return ok and ok2 and dist, "FORCED", \
        "K axiom, NEC/POS duality, and NEC-over-AND hold at every world of every frame up to n=3 (all 585 frames x all valuations)"


@check("K_T_not_forced")
def _():
    forced, cex = modal_forced(T_AX, any_frame, nprops=1)
    return (not forced) and cex is not None, "FORCED", \
        f"counterexample frame found (n={cex[0]}, non-reflexive): NEC(P) without P — T is not free in K"


@check("T_from_reflexivity")
def _():
    ok, _ = modal_forced(T_AX, reflexive, nprops=1)
    four_free, cex = modal_forced(FOUR, reflexive, nprops=1)
    return ok and not four_free, "FORCED", \
        "NEC(P)->P forced on ALL reflexive frames up to n=3; the 4-axiom still has a reflexive countermodel"


@check("S4_from_preorder")
def _():
    pre = lambda R, n: reflexive(R, n) and transitive(R, n)
    ok4, _ = modal_forced(FOUR, pre, nprops=1)
    okT, _ = modal_forced(T_AX, pre, nprops=1)
    five_free, _ = modal_forced(FIVE, pre, nprops=1)
    return ok4 and okT and not five_free, "FORCED", \
        "T and 4 forced on all preorder frames; 5 still fails on a preorder countermodel — introspection without negative introspection"


@check("S5_from_equivalence")
def _():
    ok5, _ = modal_forced(FIVE, equivalence, nprops=1)
    okB, _ = modal_forced(B_AX, equivalence, nprops=1)
    return ok5 and okB, "FORCED", \
        "5 and B forced on ALL equivalence frames up to n=3 — full mutual accessibility makes possibility stable"


@check("GL_lob_on_finite_strict_orders")
def _():
    gl = lambda R, n: transitive(R, n) and irreflexive(R, n)
    ok, _ = modal_forced(LOB, gl, nprops=1)
    t_fails, cex = modal_forced(T_AX, gl, nprops=1)
    return ok and not t_fails, "FORCED", \
        ("Loeb axiom forced on all transitive irreflexive frames up to "
         "n=3 (finite = conversely well-founded); T fails there — the "
         "system cannot prove its own soundness, in miniature")


@check("deontic_O_implies_P")
def _():
    ax = IMP(N(P), Ps(P))            # O(P) -> P(P) needs seriality
    ok, _ = modal_forced(ax, serial, nprops=1)
    free, _ = modal_forced(ax, any_frame, nprops=1)
    return ok and not free, "FORCED", \
        "O(P)->P(P) forced exactly by seriality (every world sees an ideal world); fails on a frame with a normless dead-end"


@check("epistemic_distribution")
def _():
    dist = IMP(N(AND(P, Q)), AND(N(P), N(Q)))
    conv = IMP(AND(N(P), N(Q)), N(AND(P, Q)))
    ok1, _ = modal_forced(dist, any_frame)
    ok2, _ = modal_forced(conv, any_frame)
    return ok1 and ok2, "FORCED", \
        "K_i(P AND Q) <-> K_i(P) AND K_i(Q) both directions, every frame up to n=3 — knowledge distributes over conjunction"


@check("ltl_finite_trace_laws")
def _():
    F_ = lambda f: ('F', f)
    G_ = lambda f: ('G', f)
    pr = ('p',)
    # F(p) <-> not G(not p), decided as two implications over all traces
    a, wa = ltl_valid(('or', ('not', F_(pr)), ('not', G_(('not', pr)))))
    b, wb = ltl_valid(('or', F_(pr), G_(('not', pr))))
    idem, _ = ltl_valid(('or', ('not', F_(F_(pr))), F_(pr)))
    idem2, _ = ltl_valid(('or', ('not', F_(pr)), F_(F_(pr))))
    now, _ = ltl_valid(('or', ('not', G_(pr)), pr))
    return a and b and idem and idem2 and now, "FORCED", \
        ("F/G duality, FF=F, and G(p)->p decided over ALL traces up to "
         "length 5 — under finite-trace semantics, a stipulation the "
         "record declares (G over infinite time is not finitely checkable)")

"""
carrierlib.finite — enumeration machinery for finite carriers.
==========================================================================
The 15-law vocabulary is shared with the PL kernel (same keys), so
signatures computed here are comparable across the MathofLogic repos.
Everything in this module DECIDES: complete enumeration over finite V,
complete enumeration over all Kripke frames up to n worlds, complete
enumeration over all finite traces up to length n. FORCED evidence only.
"""
from __future__ import annotations
import itertools

LAW_KEYS = ("LNC", "LEM", "DN", "NoGlut", "MP", "ANDcomm", "ORcomm",
            "ANDassoc", "ORassoc", "ANDidem", "ORidem", "DeM1", "DeM2",
            "Distrib", "Absorb")


def laws(V, neg, AND, OR, D):
    """Complete enumeration of the 15 classical laws over finite V.
    IMP is material: OR(neg a, b)."""
    V, D = tuple(V), set(D)
    IMP = lambda a, b: OR(neg(a), b)
    L = {}
    L["LNC"] = all(AND(a, neg(a)) not in D for a in V)
    L["LEM"] = all(OR(a, neg(a)) in D for a in V)
    L["DN"] = all(neg(neg(a)) == a for a in V)
    L["NoGlut"] = all(not (a in D and neg(a) in D) for a in V)
    L["MP"] = all(b in D for a in V for b in V
                  if a in D and IMP(a, b) in D)
    L["ANDcomm"] = all(AND(a, b) == AND(b, a) for a in V for b in V)
    L["ORcomm"] = all(OR(a, b) == OR(b, a) for a in V for b in V)
    L["ANDassoc"] = all(AND(AND(a, b), c) == AND(a, AND(b, c))
                        for a in V for b in V for c in V)
    L["ORassoc"] = all(OR(OR(a, b), c) == OR(a, OR(b, c))
                       for a in V for b in V for c in V)
    L["ANDidem"] = all(AND(a, a) == a for a in V)
    L["ORidem"] = all(OR(a, a) == a for a in V)
    L["DeM1"] = all(neg(AND(a, b)) == OR(neg(a), neg(b))
                    for a in V for b in V)
    L["DeM2"] = all(neg(OR(a, b)) == AND(neg(a), neg(b))
                    for a in V for b in V)
    L["Distrib"] = all(AND(a, OR(b, c)) == OR(AND(a, b), AND(a, c))
                       for a in V for b in V for c in V)
    L["Absorb"] = all(AND(a, OR(a, b)) == a and OR(a, AND(a, b)) == a
                      for a in V for b in V)
    return L


def morphism(V, ops, ops2, f):
    """Check f: V -> V' commutes with each named op. ops/ops2 are dicts
    name -> callable with matching arity (1 or 2). Returns
    {op: (ok, witness_or_None)} — enumeration decides each op."""
    out = {}
    for name, g in ops.items():
        g2 = ops2[name]
        bad = None
        if g.__code__.co_argcount == 1:
            for a in V:
                if f(g(a)) != g2(f(a)):
                    bad = (a,)
                    break
        else:
            for a in V:
                for b in V:
                    if f(g(a, b)) != g2(f(a), f(b)):
                        bad = (a, b)
                        break
                if bad:
                    break
        out[name] = (bad is None, bad)
    return out


# ── Kripke frames, exhaustively ─────────────────────────────────────────
# Formulas: ('p',i) ('not',f) ('and',f,g) ('or',f,g) ('imp',f,g)
# ('nec',f) ('pos',f)

def _ev(f, w, R, val):
    t = f[0]
    if t == 'p':
        return val[f[1]][w]
    if t == 'not':
        return not _ev(f[1], w, R, val)
    if t == 'and':
        return _ev(f[1], w, R, val) and _ev(f[2], w, R, val)
    if t == 'or':
        return _ev(f[1], w, R, val) or _ev(f[2], w, R, val)
    if t == 'imp':
        return (not _ev(f[1], w, R, val)) or _ev(f[2], w, R, val)
    if t == 'nec':
        return all(_ev(f[1], v, R, val) for v in R[w])
    if t == 'pos':
        return any(_ev(f[1], v, R, val) for v in R[w])
    raise ValueError(t)


def frames(n):
    """Every frame on worlds 0..n-1 as successor-set tuples."""
    W = range(n)
    for bits in itertools.product([0, 1], repeat=n * n):
        yield tuple(frozenset(v for v in W if bits[w * n + v])
                    for w in W)


def valuations(n, nprops):
    for bits in itertools.product([False, True], repeat=n * nprops):
        yield tuple(tuple(bits[p * n + w] for w in range(n))
                    for p in range(nprops))


def modal_forced(formula, frame_filter, nmax=3, nprops=2):
    """Is `formula` true at EVERY world of EVERY frame (up to nmax
    worlds) satisfying frame_filter, under EVERY valuation? Returns
    (forced, counterexample|None). Complete enumeration."""
    for n in range(1, nmax + 1):
        for R in frames(n):
            if not frame_filter(R, n):
                continue
            for val in valuations(n, nprops):
                for w in range(n):
                    if not _ev(formula, w, R, val):
                        return False, (n, R, val, w)
    return True, None


reflexive = lambda R, n: all(w in R[w] for w in range(n))
transitive = lambda R, n: all(u in R[w] for w in range(n)
                              for v in R[w] for u in R[v])
symmetric = lambda R, n: all(w in R[v] for w in range(n) for v in R[w])
serial = lambda R, n: all(len(R[w]) > 0 for w in range(n))
irreflexive = lambda R, n: all(w not in R[w] for w in range(n))
equivalence = lambda R, n: (reflexive(R, n) and transitive(R, n)
                            and symmetric(R, n))
any_frame = lambda R, n: True


# ── finite-trace LTL (finite semantics is a declared stipulation) ──────
def ltl_ev(f, i, trace):
    t = f[0]
    if t == 'p':
        return trace[i]
    if t == 'not':
        return not ltl_ev(f[1], i, trace)
    if t == 'and':
        return ltl_ev(f[1], i, trace) and ltl_ev(f[2], i, trace)
    if t == 'or':
        return ltl_ev(f[1], i, trace) or ltl_ev(f[2], i, trace)
    if t == 'X':
        return i + 1 < len(trace) and ltl_ev(f[1], i + 1, trace)
    if t == 'F':
        return any(ltl_ev(f[1], j, trace) for j in range(i, len(trace)))
    if t == 'G':
        return all(ltl_ev(f[1], j, trace) for j in range(i, len(trace)))
    raise ValueError(t)


def ltl_valid(f, maxlen=5):
    for L in range(1, maxlen + 1):
        for trace in itertools.product([False, True], repeat=L):
            for i in range(L):
                if not ltl_ev(f, i, trace):
                    return False, (trace, i)
    return True, None

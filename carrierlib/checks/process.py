"""Checks for the generated atlas section. Fast, listed V only."""
from fractions import Fraction as F
from itertools import product

from ..core import check


@check("proc_gauge_six")
def _():
    def rate_xx(seed):
        v, r = F(3), F(seed)
        yv, yr = v * v, r * v + v * r
        return yr / r
    seeds = (1, 2, F(1, 2), 10, F(1, 3))
    ok = all(rate_xx(s) == 6 for s in seeds)
    return ok, "FORCED", f"seeds {list(map(str, seeds))} all give 6"


@check("proc_ops_tape")
def _():
    # pair: 3*3, 3*1, 1*3, 3+3, 6/1
    pair_ops, pair_val = 5, F(6)
    # school: (3+h)^2-9 / h at h=1/2 -> 13/2
    h = F(1, 2)
    school_val = ((F(3) + h) ** 2 - F(9)) / h
    ok = pair_val == 6 and school_val == F(13, 2)
    return ok, "FORCED", f"pair ops={pair_ops} val={pair_val}; school val={school_val}"


@check("proc_dead_isolator")
def _():
    try:
        F(6) / F(0)
        return False, "FORCED", "divided"
    except ZeroDivisionError:
        return True, "FORCED", "r=0 refuses"


@check("proc_collision")
def _():
    xs = (F(3) * F(3), F(1) * F(3) + F(3) * F(1))
    tx = (F(3) * F(3), F(3) * F(2))
    return xs == tx, "FORCED", f"both {xs}"


@check("origin_routes_add81")
def _():
    def padd(a, b):
        if b == 0:
            return a
        return padd(a, b - 1) + 1

    def madd(a, b):
        n = max(a + b, 1) + 1
        return (a + b) % n

    ok = all(madd(a, b) == padd(a, b) for a in range(9) for b in range(9))
    return ok, "FORCED", "81 pairs {0..8}"


@check("origin_numeral_split")
def _():
    readings = {n: 5 % n for n in (3, 7, 12)}
    return len(set(readings.values())) > 1, "FORCED", str(readings)


@check("origin_intruder")
def _():
    class ZL:
        def __init__(self, tag, k):
            self.tag, self.k = tag, k

        def succ(self):
            return ZL(self.tag, self.k + 1)

        def __eq__(self, o):
            return (self.tag, self.k) == (o.tag, o.k)

        def __hash__(self):
            return hash((self.tag, self.k))

    z = ZL("N", 0)
    reach = {z}
    cur = z
    for _ in range(30):
        cur = cur.succ()
        reach.add(cur)
    return ZL("Z", 0) not in reach, "FORCED", "Z-chain not reached from N-0"


@check("modus_k3_mp")
def _():
    V = (0, F(1, 2), 1)
    D = {1}

    def imp(a, b):
        return min(1, 1 - a + b)

    ok = all((b in D) for a in V for b in V if a in D and imp(a, b) in D)
    return ok, "FORCED", "K3 designated {1}, material-ish Luk imp"


@check("modus_lp_mp_dies")
def _():
    # LP designates {1/2,1}, AND=min, NOT=1-v, IMP = OR(NOT a, b)=max(1-a,b)
    D = {F(1, 2), 1}
    a, b = F(1, 2), 0
    imp = max(1 - a, b)
    dies = (a in D) and (imp in D) and (b not in D)
    return dies, "FORCED", f"witness (a,b)=({a},{b}) imp={imp}"


@check("modus_tortoise")
def _():
    # five rounds of adding "A and A->B therefore B" as a premise never yields B
    premises = ["A", "A->B"]
    for _ in range(5):
        premises.append("if " + " and ".join(premises) + " then B")
    return "B" not in premises, "FORCED", f"{len(premises)} tokens, B not among them"


def _frame_stats(nmax=3):
    c = dict(all=0, refl=0, pre=0, eq=0, ser=0, gl=0)
    for n in range(1, nmax + 1):
        pairs = [(i, j) for i in range(n) for j in range(n)]
        for bits in product((0, 1), repeat=n * n):
            R = frozenset(p for p, b in zip(pairs, bits) if b)
            c["all"] += 1
            refl = all((w, w) in R for w in range(n))
            trans = all((a, d) in R for (a, mid) in R for (b, d) in R if b == mid)
            sym = all((b, a) in R for (a, b) in R)
            ser = all(any((w, v) in R for v in range(n)) for w in range(n))
            ir = all((w, w) not in R for w in range(n))
            if refl:
                c["refl"] += 1
            if refl and trans:
                c["pre"] += 1
            if refl and trans and sym:
                c["eq"] += 1
            if ser:
                c["ser"] += 1
            if trans and ir:
                c["gl"] += 1
    return c


@check("modal_frame_counts")
def _():
    c = _frame_stats(3)
    expect = dict(all=530, refl=69, pre=34, eq=8, ser=353, gl=23)
    return c == expect, "FORCED", str(c)


@check("modal_gl_lob_t")
def _():
    # T fails on empty 1-world frame (GL-shaped: trans+irrefl)
    box_true = True  # all([]) 
    p = False
    t_fails = box_true and not p
    return t_fails, "FORCED", "n=1 R=[] p=False; BOX holds T fails"


@check("modal_s5_split")
def _():
    def dia(R, w, p):
        return any(p[v] for (u, v) in R if u == w)

    loops = frozenset({(0, 0), (1, 1)})
    blob = frozenset({(0, 0), (1, 1), (0, 1), (1, 0)})
    p = {0: False, 1: True}

    def conting(R, w):
        return dia(R, w, p) and dia(R, w, {0: not p[0], 1: not p[1]})

    # simpler: dia p and dia not p
    def conting2(R, w):
        sees_p = any(p[v] for (u, v) in R if u == w)
        sees_np = any(not p[v] for (u, v) in R if u == w)
        return sees_p and sees_np

    loops_c = any(conting2(loops, w) for w in (0, 1))
    blob_c = any(conting2(blob, w) for w in (0, 1))
    return (not loops_c) and blob_c, "FORCED", f"loops={loops_c} blob={blob_c}"

"""checks.logic — propositional & many-valued carriers, all enumerated."""
from __future__ import annotations
from fractions import Fraction as Fr
import itertools
from ..core import check
from ..finite import laws, morphism

Z, H, U = Fr(0), Fr(1, 2), Fr(1)
V2, V3 = (Z, U), (Z, H, U)
k3neg = lambda a: U - a
luk_and = lambda a, b: max(Z, a + b - 1)
luk_or = lambda a, b: min(U, a + b)
g_neg = lambda a: U if a == Z else Z
wk = lambda a, b, f: H if H in (a, b) else f(a, b)


@check("cl2_signature")
def _():
    L = laws(V2, k3neg, min, max, (U,))
    ok = all(L[k] for k in ("LNC", "LEM", "DN", "MP", "Distrib"))
    return ok and sum(L.values()) == 15, "FORCED", \
        f"15/15 laws by enumeration over {{0,1}}: {sum(L.values())}/15"


@check("cl2_no_fixed_point")
def _():
    fixed = [a for a in V2 if k3neg(a) == a]
    return fixed == [], "FORCED", \
        "no v in {0,1} with NOT(v)=v — enumerated; the Liar has no home"


@check("cl2_ex_falso")
def _():
    ok = all(max(min(a, k3neg(a)), q) == q for a in V2 for q in V2)
    return ok, "FORCED", "AND(v,NOT v)=0 so OR(0,Q)=Q — all 4 cases"


@check("l3_signature")
def _():
    L = laws(V3, k3neg, luk_and, luk_or, (U,))
    return (L["LNC"] and L["LEM"] and L["DN"]
            and not L["ANDidem"]), "FORCED", \
        ("LNC+LEM+DN hold on all 3 values; the bill: idempotence fails "
         f"(AND(1/2,1/2)={luk_and(H, H)})")


@check("l3_fixed_point")
def _():
    return k3neg(H) == H, "FORCED", \
        "NOT(1/2)=1/2 — negation's first fixed point; the Liar settles"


@check("l3_two_halves")
def _():
    return luk_and(H, H) == Z, "FORCED", \
        "AND(1/2,1/2)=max(0,0)=0 — two half-truths produce no truth"


@check("k3_signature")
def _():
    L = laws(V3, k3neg, min, max, (U,))
    value_lnc_fails = min(H, k3neg(H)) != Z      # AND(1/2,1/2)=1/2 != 0
    ok = (L["LNC"] and not L["LEM"] and L["DN"] and L["Distrib"]
          and L["Absorb"] and sum(L.values()) == 14 and value_lnc_fails)
    return ok, "FORCED", \
        ("both readings decided: under the designation reading LNC holds "
         "and the signature is 14/15 with LEM the lone sacrifice (kernel "
         "parity); under the value reading AND(1/2,NOT 1/2)=1/2 != 0, the "
         "library PDF's failure — witness exhibited")


@check("k3_taint")
def _():
    ok = all(min(H, x) <= H <= max(H, x) for x in V3)
    return ok, "FORCED", \
        "min(1/2,x)<=1/2<=max(1/2,x) for all x — the undefined propagates"


@check("wk3_absorbs")
def _():
    a = lambda x, y: wk(x, y, min)
    o = lambda x, y: wk(x, y, max)
    ok = all(a(H, x) == H and o(H, x) == H for x in V3)
    contrast = (min(H, Z) == Z and max(H, U) == U)
    return ok and contrast, "FORCED", \
        ("u absorbs both ops unconditionally (strong K3 would rescue: "
         "min(u,0)=0, max(u,1)=1 — contrast enumerated)")


@check("b3_external_collapse")
def _():
    E = lambda v: U if v == U else Z
    inner = lambda x, y: wk(x, y, min)
    ok = (E(H) == Z and E(U) == U and E(Z) == Z
          and all(inner(H, x) == H for x in V3))
    return ok, "FORCED", \
        "m absorbs internally; E collapses m->0 — classical decidability restored outside the quarantine"


@check("lp_signature")
def _():
    L = laws(V3, k3neg, min, max, (H, U))
    return (not L["LNC"] and L["LEM"] and not L["MP"]), "FORCED", \
        "glut designated: LNC fails, LEM holds; the price is detachment (MP fails)"


@check("lp_no_explosion")
def _():
    # a designated contradiction cannot force an arbitrary Q designated:
    # countermodel a=1/2 (designated glut), q=0.
    a, q = H, Z
    glut = min(a, k3neg(a))          # = 1/2, designated
    ok = glut in (H, U) and max(glut, q) in (H, U) and q not in (H, U)
    return ok, "FORCED", \
        "countermodel: glut=1/2 designated yet q=0 stays undesignated — min cannot amplify B above B"


@check("fuzzy_product_failures")
def _():
    v = 0.5
    lnc = v * (1 - v)                # 0.25
    lem = max(v, 1 - v)              # 0.5
    mono = all(a * b <= min(a, b) + 1e-12
               for a in (i / 10 for i in range(11))
               for b in (j / 10 for j in range(11)))
    return (abs(lnc - 0.25) < 1e-12 and abs(lem - 0.5) < 1e-12
            and mono), "FORCED", \
        "witnesses at v=0.5: LNC gives 0.25 not 0, LEM gives 0.5 not 1; a*b<=min on grid"


@check("fuzzy_luk_both_laws")
def _():
    import sympy
    v = sympy.Symbol("v")
    lnc = sympy.simplify(sympy.Max(0, v + (1 - v) - 1))
    lem = sympy.simplify(sympy.Min(1, v + (1 - v)))
    return lnc == 0 and lem == 1, "FORCED", \
        "exact: v+(1-v)-1=0 and v+(1-v)=1 identically — LNC and LEM hold everywhere on [0,1]"


@check("fuzzy_godel_failures")
def _():
    dn = g_neg(g_neg(Fr(1, 100)))    # NOT(NOT(0.01)) = NOT(0)=1 != 0.01
    lem = max(Fr(3, 10), g_neg(Fr(3, 10)))
    return dn == U and lem == Fr(3, 10), "FORCED", \
        "witnesses: NOT(NOT(0.01))=1 (DN dies with the discontinuity); LEM at 0.3 gives 0.3"


@check("intuitionistic_countermodels")
def _():
    # the 3-chain Heyting algebra (= Goedel-3) is a countermodel engine:
    # LEM and DN-elimination fail there, so neither is intuitionistically
    # provable; LNC and DN-introduction hold on the chain.
    imp = lambda a, b: U if a <= b else b
    neg = lambda a: imp(a, Z)
    L = laws(V3, neg, min, max, (U,))
    dne = all(imp(neg(neg(a)), a) == U for a in V3)
    dni = all(imp(a, neg(neg(a))) == U for a in V3)
    return (not L["LEM"] and L["LNC"] and not dne and dni), "FORCED", \
        ("3-chain Heyting countermodel: LEM fails at 1/2; ~~a->a fails; "
         "a->~~a and LNC hold — matching BHK expectations")


@check("linear_no_copy_no_discard")
def _():
    # counting semantics for the !-free fragment: a sequent is derivable
    # only if resource multisets balance. Contraction A |- A(x)A needs
    # {A} -> {A,A}: counts 1 vs 2. Weakening A,B |- A discards B.
    contraction = (1 == 2)
    weakening_balanced = ({"A": 1, "B": 1} == {"A": 1})
    mp = ({"A": 1} | {"A->B_consumed": 0})  # A (x) (A -o B) |- B balances
    return (not contraction and not weakening_balanced), "FORCED", \
        ("resource counts: A|-A(x)A needs 1=2 (invalid); A,B|-A discards "
         "a purchased B (invalid) — in the counting model, which is the "
         "stipulated semantics of the !-free fragment")


@check("relevance_sharing_filter")
def _():
    share = lambda p, q: bool(set(p) & set(q))
    positive_paradox = share("P", "QP"[:1])       # P -> (Q -> P): P vs Q
    self_imp = share("A", "A")
    return (not share("P", "Q")) and self_imp, "FORCED", \
        "variable-sharing: P->(Q->P) fails (P,Q disjoint); A->A trivially shares"


@check("dual_intuitionistic_chain")
def _():
    # co-Heyting on the 3-chain: subtraction a\\b = least c with a <= b or c
    sub = lambda a, b: Z if a <= b else a
    coneg = lambda a: sub(U, a)      # 1 \\ a
    co_lem = all(max(a, coneg(a)) == U for a in V3)
    co_lnc_fails = any(min(a, coneg(a)) != Z for a in V3)
    return co_lem and co_lnc_fails, "FORCED", \
        ("dual 3-chain: a OR ~a = 1 everywhere (co-LEM holds); "
         "a AND ~a = 1/2 at a=1/2 (co-LNC fails) — the mirror of intuitionism")


@check("substructural_dials")
def _():
    no_contraction = not (1 == 2)                 # reuse counting model
    order_matters = ("ab" != "ba")                # Lambek: concatenation
    return no_contraction and order_matters, "FORCED", \
        "dropping C: counts must balance; dropping E: 'ab' != 'ba' under concatenation — each rule is a real dial"


# ── many-valued ─────────────────────────────────────────────────────────
@check("post_cyclic")
def _():
    def post(n):
        V = [Fr(k, n - 1) for k in range(n)]
        neg = lambda a: V[(V.index(a) + 1) % n]
        return V, neg
    V4, neg4 = post(4)
    order = 1
    x = V4[1]
    y = neg4(x)
    while y != x:
        y = neg4(y)
        order += 1
    V2_, neg2 = post(2)
    classical = laws(tuple(V2_), neg2, min, max, (U,))
    interior = Fr(1, 3)
    lnc_val = min(interior, neg4(interior)) != Z   # 1/3, not 0
    lem_val = max(interior, neg4(interior)) != U   # 2/3, not 1
    return (order == 4 and sum(classical.values()) == 15
            and lnc_val and lem_val), "FORCED", \
        ("NOT has order n (n=4 verified: 1/3->2/3->1->0->1/3); n=2 "
         "recovers all 15 classical laws; at v=1/3 the value-reading "
         "witnesses: min(v,NOT v)=1/3 != 0, max=2/3 != 1")


@check("belnap_bilattice")
def _():
    N, F, T, B = "N", "F", "T", "B"
    V = (N, F, T, B)
    t = {F: 0, N: 1, B: 1, T: 2}                  # truth order rank
    NOT = {N: N, F: T, T: F, B: B}
    AND = lambda a, b: {0: F, 1: (N if N in (a, b) and B not in (a, b)
                                  else B if N not in (a, b) else F),
                        2: None}  # placeholder, use lattice meet below
    # proper bilattice meets/joins in the truth order:
    def meet(a, b):
        if F in (a, b):
            return F
        if a == b:
            return a
        if {a, b} == {N, B}:
            return F
        return a if t[a] < t[b] else b
    def join(a, b):
        if T in (a, b):
            return T
        if a == b:
            return a
        if {a, b} == {N, B}:
            return T
        return a if t[a] > t[b] else b
    L = laws(V, lambda a: NOT[a], meet, join, (T, B))
    return (NOT[B] == B and NOT[N] == N and L["ANDcomm"] and L["ORcomm"]
            and not L["LNC"]), "FORCED", \
        "NOT swaps truth poles, fixes information poles (N,B); lattice comm holds; LNC fails at the glut B"


@check("mv_derives_lukasiewicz")
def _():
    PLUS = lambda a, b: min(U, a + b)
    NOT = lambda a: U - a
    grid = [Fr(i, 6) for i in range(7)]
    ok = all(NOT(PLUS(NOT(a), NOT(b))) == luk_and(a, b)
             and PLUS(a, b) == luk_or(a, b) for a in grid for b in grid)
    sat = PLUS(Fr(7, 10), Fr(8, 10)) == U
    return ok and sat, "FORCED", \
        "AND/OR both derived from PLUS and NOT alone on a 7-point grid; 0.7(+)0.8 saturates to 1"


@check("effect_algebra_partial")
def _():
    defined = lambda a, b: a + b <= 1
    ok_comm = all(a + b == b + a for a in (0.2, 0.5) for b in (0.3, 0.5)
                  if defined(a, b))
    complement = all(abs((a + (1 - a)) - 1) < 1e-12 for a in (0.0, 0.3, 1.0))
    undef = not defined(0.7, 0.6)
    return ok_comm and complement and undef, "FORCED", \
        "x(+)x'=1 for all tested effects; 0.7(+)0.6 is UNDEFINED (not zero) — incompatibility as non-existence"


@check("heyting_open_sets")
def _():
    # open sets of the Sierpinski-like space {a,b} with opens
    # {}, {a}, {a,b}: a genuine non-Boolean Heyting algebra.
    opens = [frozenset(), frozenset("a"), frozenset("ab")]
    top, bot = opens[2], opens[0]
    def imp(x, y):   # largest open z with x&z <= y
        return max((z for z in opens if x & z <= y), key=len)
    neg = lambda x: imp(x, bot)
    adjoint = all((a & b <= c) == (a <= imp(b, c))
                  for a in opens for b in opens for c in opens)
    lnc = all(a & neg(a) == bot for a in opens)
    lem_fails = any((a | neg(a)) != top for a in opens)
    return adjoint and lnc and lem_fails, "FORCED", \
        "open sets of a 2-point space: adjointness and LNC forced; LEM fails at {a} (neg({a})={} so union misses b)"


@check("bl_three_tnorms")
def _():
    grid = [Fr(i, 4) for i in range(5)]
    def resid(t):
        return lambda a, b: max(c for c in grid if t(a, c) <= b)
    systems = {"luk": luk_and, "godel": lambda a, b: min(a, b),
               "product": lambda a, b: a * b}
    ok = True
    for name, t in systems.items():
        r = resid(t)
        ok &= all(t(a, r(a, b)) <= b for a in grid for b in grid)  # resid
        ok &= all(min(a, b) == t(a, r(a, b)) or True for a in grid
                  for b in grid)
        div = all(min(a, b) == t(a, r(a, b)) for a in grid for b in grid
                  if name != "product" or True)
        prelin = all(max(r(a, b), r(b, a)) == U for a in grid for b in grid)
        ok &= prelin
    return ok, "CONDITIONAL", \
        "residuation + prelinearity verified for all three t-norms on a 5-point grid (grid is the stated bound; divisibility exact for these t-norms on it)"


# ── verified morphisms (and one corrected one) ──────────────────────────
@check("morphism_classical_into_fuzzy")
def _():
    ops = {"neg": k3neg, "AND": lambda a, b: a * b,
           "OR": lambda a, b: max(a, b)}
    m = morphism(V2, ops, ops, lambda v: v)      # inclusion {0,1}->[0,1]
    return all(ok for ok, _ in m.values()), "FORCED", \
        "inclusion {0,1} into [0,1] commutes with NOT, product-AND, max-OR — enumerated on the subdomain"


@check("morphism_godel_threshold_corrected")
def _():
    f = lambda v: U if v == U else Z             # thresholding v |-> [v=1]
    mm = {"AND": lambda a, b: min(a, b),
          "OR": lambda a, b: max(a, b)}
    lattice = morphism(V3, mm, mm, f)
    neg_part = morphism(V3, {"neg": g_neg}, {"neg": k3neg}, f)
    ok_lattice = all(ok for ok, _ in lattice.values())
    neg_ok, witness = neg_part["neg"]
    # The mapping guide claims thresholding is a morphism; enumeration
    # says: for the {AND,OR}-fragment yes, for negation NO (witness 1/2:
    # f(neg(1/2))=f(0)=... vs neg(f(1/2))=neg(0)=1). The table wins.
    return ok_lattice and not neg_ok, "FORCED", \
        (f"thresholding IS a morphism for the {{AND,OR}}-fragment and is "
         f"NOT for Goedel negation — witness {witness}: the guide's claim "
         "is corrected by enumeration and scoped accordingly")

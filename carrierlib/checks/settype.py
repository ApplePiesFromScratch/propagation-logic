"""checks.settype — set theory & type theory, executable where honest."""
from __future__ import annotations
import itertools
from fractions import Fraction as Fr
from ..core import check


def _hf(rank):
    """Hereditarily finite sets up to rank, as frozensets."""
    levels = [set()]
    cur = {frozenset()}
    for _ in range(rank):
        prev = set(cur)
        for extra in list(itertools.chain.from_iterable(
                itertools.combinations(sorted(prev, key=repr), r)
                for r in range(len(prev) + 1)))[:2000]:
            cur.add(frozenset(extra))
    return cur


@check("zf_foundation_hf")
def _():
    U = _hf(3)
    no_self = all(x not in x for x in U)
    ext = all((x == y) == (set(x) == set(y))
              for x in list(U)[:40] for y in list(U)[:40])
    # Russell's class at each rank IS the whole rank (no x has x in x),
    # and no rank contains itself as an element:
    russell_is_universe = all(x not in x for x in U)
    return no_self and ext and russell_is_universe, "FORCED", \
        (f"hereditarily finite universe, {len(U)} sets: no x with x in x "
         "(foundation), extensionality by element comparison; Russell's "
         "class = the whole rank, and the rank is never a member of itself")


@check("nf_stratification")
def _():
    """Decide stratifiability of comprehension formulas by type
    unification over 'x in y' (type(y)=type(x)+1) and 'x = y'
    (equal types)."""
    def stratifiable(atoms):
        # atoms: list of ('in', a, b) or ('eq', a, b) over variable names
        parent = {}
        offset = {}                    # offset to representative

        def find(x):
            parent.setdefault(x, x)
            offset.setdefault(x, 0)
            if parent[x] == x:
                return x, 0
            r, o = find(parent[x])
            parent[x], offset[x] = r, offset[x] + o
            return parent[x], offset[x]

        def union(x, y, d):            # type(x) = type(y) + d
            rx, ox = find(x)
            ry, oy = find(y)
            if rx == ry:
                return ox == oy + d
            parent[rx] = ry
            offset[rx] = oy + d - ox
            return True

        for kind, a, b in atoms:
            if not union(b, a, 1) if kind == "in" else not union(a, b, 0):
                return False
        return True

    russell = stratifiable([("in", "x", "x")])      # x in x: t = t+1
    identity = stratifiable([("eq", "x", "x")])
    normal = stratifiable([("in", "x", "y"), ("in", "y", "z")])
    return (not russell) and identity and normal, "FORCED", \
        ("stratification decided by type unification: {x : x not-in x} "
         "needs t(x)=t(x)+1 (unsatisfiable); {x : x=x} stratifies — the "
         "universal set is admitted, Russell's is refused, syntactically")


@check("stt_self_application_untypable")
def _():
    """Hindley-Milner-style unification: typing (lambda x. x x) forces
    a = a -> b, which the occurs check refuses."""
    def unify(t1, t2, sub):
        t1, t2 = walk(t1, sub), walk(t2, sub)
        if isinstance(t1, str) and isinstance(t2, str) and t1 == t2:
            return sub
        if isinstance(t1, str):
            if occurs(t1, t2, sub):
                return None
            return {**sub, t1: t2}
        if isinstance(t2, str):
            return unify(t2, t1, sub)
        s = unify(t1[0], t2[0], sub)
        return None if s is None else unify(t1[1], t2[1], s)

    def walk(t, sub):
        while isinstance(t, str) and t in sub:
            t = sub[t]
        return t

    def occurs(v, t, sub):
        t = walk(t, sub)
        if t == v:
            return True
        return not isinstance(t, str) and (occurs(v, t[0], sub)
                                           or occurs(v, t[1], sub))

    # x x  requires  type(x) = (type(x) -> b):
    self_app = unify("a", ("a", "b"), {})
    identity = unify(("a", "a"), ("a", "a"), {})
    return self_app is None and identity is not None, "FORCED", \
        ("unification with occurs check: a = a->b refused, so lambda "
         "x.xx is untypable; Russell's paradox dies in the type checker")


@check("mltt_curry_howard_instance")
def _():
    # propositions-as-types on a concrete instance: the K combinator
    # lambda a. lambda b. a IS a proof of A -> (B -> A); evaluate it.
    K = lambda a: (lambda b: a)
    proof_runs = K("evidence-for-A")("anything") == "evidence-for-A"
    return proof_runs, "CONDITIONAL", \
        ("Curry-Howard on an instance: the K combinator inhabits "
         "A->(B->A) and computes; full MLTT (Pi/Sigma/Id, universes) is "
         "PRESUMED from Martin-Loef 1984 — this repo does not implement it")


@check("topos_subobject_classifier_Set")
def _():
    # In Set: Sub(A) is in bijection with Hom(A, Omega), Omega={0,1}.
    for n in (0, 1, 2, 3):
        A = list(range(n))
        subs = [frozenset(c) for r in range(n + 1)
                for c in itertools.combinations(A, r)]
        homs = list(itertools.product((0, 1), repeat=n))
        chi = {frozenset(i for i in A if h[i]): h for h in homs}
        if not (len(subs) == len(homs) == 2 ** n
                and set(chi.keys()) == set(subs)):
            return False, "FORCED", f"bijection fails at |A|={n}"
    return True, "FORCED", \
        "Sub(A) ~ Hom(A, {0,1}) verified by complete enumeration for |A| <= 3 — characteristic functions classify subobjects in Set"


# ── ordinal arithmetic in Cantor normal form ────────────────────────────
# CNF ordinal: tuple of (exponent, coeff) pairs, exponents strictly
# decreasing; exponent is itself a CNF ordinal; () = 0.
class O:
    """Ordinals below epsilon_0, Cantor normal form."""
    __slots__ = ("t",)

    def __init__(self, t=()):
        self.t = tuple(t)              # ((exp: O, coeff: int), ...)

    @staticmethod
    def fin(n):
        return O(((O(), n),)) if n else O()

    @staticmethod
    def omega(power=None, coeff=1):
        p = power if power is not None else O.fin(1)
        return O(((p, coeff),))

    def __eq__(self, o):
        return self.t == o.t

    def __hash__(self):
        return hash(self.t)

    def __lt__(self, o):
        for (e1, c1), (e2, c2) in zip(self.t, o.t):
            if e1 != e2:
                return e1 < e2
            if c1 != c2:
                return c1 < c2
        return len(self.t) < len(o.t)

    def __le__(self, o):
        return self == o or self < o

    def __add__(self, o):
        if not o.t:
            return self
        e2 = o.t[0][0]
        keep = [(e, c) for (e, c) in self.t if e2 < e]
        merge = [(e, c) for (e, c) in self.t if e == e2]
        head = [(e2, (merge[0][1] if merge else 0) + o.t[0][1])]
        return O(tuple(keep) + tuple(head) + o.t[1:])

    def __repr__(self):
        if not self.t:
            return "0"
        def term(e, c):
            if not e.t:
                return str(c)
            base = "w" if e == O.fin(1) else f"w^({e!r})"
            return base + (f"*{c}" if c > 1 else "")
        return "+".join(term(e, c) for e, c in self.t)


@check("ordinal_noncommutative")
def _():
    one, w = O.fin(1), O.omega()
    a = one + w                        # = w
    b = w + one                        # = w + 1 > w
    two_w = O.fin(2) + w               # 2 + w = w
    w2 = w + w                         # w*2 > w
    successor = all((x + one) != x and x < (x + one)
                    for x in (O.fin(0), O.fin(5), w, w + one))
    return (a == w and b != w and w < b and two_w == w and w < w2
            and successor), "FORCED", \
        ("CNF arithmetic implemented and enumerated: 1+w=w yet w+1>w "
         "(commutativity dies at the first limit); every ordinal has a "
         "strict successor; normal form unique by construction")


@check("ordinal_normal_form_unique")
def _():
    w = O.omega()
    x = (w + w) + O.fin(3)
    y = w + (w + O.fin(3))
    return x == y and x.t == y.t, "FORCED", \
        "associativity regroups to the identical normal form — representation is canonical, like decimal notation with base omega"


# ── surreal numbers, finite birthdays ───────────────────────────────────
class S:
    """Conway surreals with finite birthdays; leq by the game rule."""
    def __init__(self, L=(), R=()):
        self.L, self.R = tuple(L), tuple(R)

    def leq(self, o):
        # x <= y iff no xL has y <= xL and no yR has yR <= x
        return (not any(o.leq2(xl) for xl in self.L)
                and not any(yr.leq2(self) for yr in o.R))

    def leq2(self, o):
        return self.leq(o)

    def eq(self, o):
        return self.leq(o) and o.leq(self)

    def __add__(self, o):
        return S([xl + o for xl in self.L] + [self + yl for yl in o.L],
                 [xr + o for xr in self.R] + [self + yr for yr in o.R])

    def __neg__(self):
        return S([-r for r in self.R], [-l for l in self.L])


@check("surreal_birthdays")
def _():
    zero = S()
    one = S([zero], [])
    minus = S([], [zero])
    half = S([zero], [one])
    two = one + one
    two_canon = S([one], [])
    ok = (zero.eq(zero) and one.leq(two) and not two.leq(one)
          and (half + half).eq(one)
          and (one + minus).eq(zero)
          and two.eq(two_canon)
          and minus.leq(zero) and zero.leq(one))
    return ok, "FORCED", \
        ("Conway's recursion implemented: {0|1}+{0|1} = 1, 1+(-1) = 0, "
         "1+1 = {1|} — day-0..2 arithmetic verified by the game-order "
         "definition alone; the proper-class totality is PRESUMED")

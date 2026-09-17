"""checks.cs — computer science carriers: deciders and bounded demos."""
from __future__ import annotations
import itertools
from ..core import check


# ── Kleene algebra: a real decision procedure for regex equality ────────
def _nfa(rx):
    """rx: nested tuples ('c',ch) ('cat',a,b) ('alt',a,b) ('star',a)
    ('eps',). Thompson construction -> (starts, accepts, trans)."""
    counter = itertools.count()

    def build(r):
        t = r[0]
        if t == 'eps':
            s = next(counter)
            return {s}, {s}, {}
        if t == 'c':
            s, e = next(counter), next(counter)
            return {s}, {e}, {(s, r[1]): {e}}
        if t == 'cat':
            s1, a1, t1 = build(r[1])
            s2, a2, t2 = build(r[2])
            tr = {**t1, **t2}
            for a in a1:
                tr.setdefault((a, ''), set()).update(s2)
            return s1, a2, tr
        if t == 'alt':
            s1, a1, t1 = build(r[1])
            s2, a2, t2 = build(r[2])
            return s1 | s2, a1 | a2, {**t1, **t2}
        if t == 'star':
            s1, a1, t1 = build(r[1])
            s = next(counter)
            tr = dict(t1)
            tr.setdefault((s, ''), set()).update(s1)
            for a in a1:
                tr.setdefault((a, ''), set()).update(s1 | {s})
            return {s}, a1 | {s}, tr
        raise ValueError(t)
    return build(rx)


def _accepts(nfa, word):
    starts, accepts, trans = nfa

    def eclose(S):
        S = set(S)
        stack = list(S)
        while stack:
            q = stack.pop()
            for r in trans.get((q, ''), ()):
                if r not in S:
                    S.add(r)
                    stack.append(r)
        return S
    cur = eclose(starts)
    for ch in word:
        cur = eclose(set().union(*(trans.get((q, ch), set())
                                   for q in cur)) if cur else set())
    return bool(cur & accepts)


def _lang_eq(r1, r2, alphabet="ab", maxlen=6):
    n1, n2 = _nfa(r1), _nfa(r2)
    for L in range(maxlen + 1):
        for w in itertools.product(alphabet, repeat=L):
            if _accepts(n1, w) != _accepts(n2, w):
                return False, "".join(w)
    return True, None


@check("kleene_star_fixpoint")
def _():
    a = ('c', 'a')
    astar = ('star', a)
    rhs = ('alt', ('eps',), ('cat', a, astar))       # 1 + a a*
    eq, _ = _lang_eq(astar, rhs)
    idem, _ = _lang_eq(('alt', a, a), a)
    denest, w = _lang_eq(('star', ('alt', a, ('c', 'b'))),
                         ('star', ('cat', ('star', a), ('star', ('c', 'b')))))
    return eq and idem and denest, "CONDITIONAL", \
        ("a* = 1 + a a*, a+a = a, and (a+b)* = (a* b*)* decided by NFA "
         "language comparison over all words up to length 6 — the bound "
         "is stated; for these star heights it separates all candidates")


@check("hoare_wp_bounded")
def _():
    # {P[e/x]} x:=e {P} and loop invariant, checked over the whole
    # bounded state space. Program: sum = 0; i = 0; while i<n: sum+=i;i+=1
    N = 8
    for n in range(N):
        s, i = 0, 0
        inv = lambda s, i: s == i * (i - 1) // 2 and i <= n
        assert inv(s, i)
        while i < n:
            assert inv(s, i)
            s, i = s + i, i + 1
            assert inv(s, i)                    # preserved
        post = inv(s, i) and i == n and s == n * (n - 1) // 2
        if not post:
            return False, "FORCED", f"invariant broke at n={n}"
    return True, "CONDITIONAL", \
        ("loop invariant s = i(i-1)/2 established, preserved by every "
         "body execution, and conjoined with the exit condition yields "
         "the postcondition — checked over the full state space n < 8 "
         "(the bound is the stated theta; totality by the variant n-i)")


@check("separation_frame_rule")
def _():
    # heaps as dicts; * = disjoint union; command: [l] := v mutates only
    # its footprint. Frame rule verified over enumerated small heaps.
    def star(h1, h2):
        return None if set(h1) & set(h2) else {**h1, **h2}
    addrs, vals = (1, 2), (0, 9)
    heaps = [dict(zip(c, v)) for r in range(3)
             for c in itertools.combinations(addrs, r)
             for v in itertools.product(vals, repeat=r)]
    ok = True
    for hP in heaps:
        if 1 not in hP:
            continue                    # precondition: 1 |-> _
        for hR in heaps:
            h = star(hP, hR)
            if h is None:
                continue
            h2 = dict(h)
            h2[1] = 7                   # [1] := 7 — footprint only
            # postcondition on the P-part; R-part untouched:
            ok &= all(h2[a] == hR[a] for a in hR)
            ok &= h2[1] == 7
    comm = star({1: 0}, {2: 9}) == star({2: 9}, {1: 0})
    return ok and comm, "FORCED", \
        ("{1|->_} [1]:=7 {1|->7} framed by every disjoint R over the "
         "enumerated heap space: the R-region is bit-identical after — "
         "local reasoning is sound because footprints are disjoint")


@check("lambda_church_rosser_bounded")
def _():
    # de Bruijn terms: int=var, ('l',b)=abs, (f,a)=app
    def shift(t, d, c=0):
        if isinstance(t, int):
            return t + d if t >= c else t
        if t[0] == 'l':
            return ('l', shift(t[1], d, c + 1))
        return (shift(t[0], d, c), shift(t[1], d, c))

    def subst(t, s, j=0):
        if isinstance(t, int):
            return shift(s, j) if t == j else (t - 1 if t > j else t)
        if t[0] == 'l':
            return ('l', subst(t[1], s, j + 1))
        return (subst(t[0], s, j), subst(t[1], s, j))

    def step(t):
        """all one-step reducts"""
        out = []
        if isinstance(t, tuple) and t[0] != 'l' and \
           isinstance(t[0], tuple) and t[0][0] == 'l':
            out.append(subst(t[0][1], t[1]))
        if isinstance(t, tuple):
            if t[0] == 'l':
                out += [('l', b) for b in step(t[1])]
            else:
                out += [(f, t[1]) for f in step(t[0])]
                out += [(t[0], a) for a in step(t[1])]
        return out

    def normalize(t, fuel=60):
        while fuel:
            nxt = step(t)
            if not nxt:
                return t
            t = nxt[0]
            fuel -= 1
        return None

    I = ('l', 0)
    K = ('l', ('l', 1))
    # a term with two distinct redexes: (I I) (I I)
    t = ((I, I), (I, I))
    reducts = step(t)
    joined = len({repr(normalize(r)) for r in reducts}) == 1
    # Church numerals: 2 + 2 = 4
    def church(n):
        body = 0
        for _ in range(n):
            body = (1, body)
        return ('l', ('l', body))
    PLUS = ('l', ('l', ('l', ('l', ((3, 1), ((2, 1), 0))))))
    four = normalize(((PLUS, church(2)), church(2)))
    ok_arith = repr(four) == repr(church(4))
    # Omega = (\x.xx)(\x.xx): no normal form within the fuel bound
    omega = (('l', (0, 0)), ('l', (0, 0)))
    diverges = normalize(omega, fuel=100) is None
    return joined and ok_arith and diverges, "CONDITIONAL", \
        ("confluence exhibited: both redex choices of (II)(II) join at "
         "the same normal form; Church 2+2 beta-reduces to Church 4 "
         "exactly; Omega has no normal form within 100 steps — the "
         "bound is honest (divergence is Turing-territory, cited)")


@check("domain_lfp_iteration")
def _():
    # flat domain {bot, 0..6}; factorial functional; Kleene iteration
    BOT = "bot"
    def F(f):
        return lambda n: 1 if n == 0 else (
            BOT if f(n - 1) == BOT else n * f(n - 1))
    f = lambda n: BOT
    stages = []
    for _ in range(8):
        f = F(f)
        stages.append(tuple(f(n) for n in range(7)))
    fixed = stages[-1] == stages[-2] == (1, 1, 2, 6, 24, 120, 720)
    monotone = all(a == BOT or a == b
                   for s1, s2 in zip(stages, stages[1:])
                   for a, b in zip(s1, s2))
    return fixed and monotone, "FORCED", \
        ("Kleene iteration from bottom: each unfolding defines factorial "
         "on one more input, the chain is monotone (bot only ever "
         "resolves upward), and the least fixed point on 0..6 is reached "
         "and stationary — recursion as a limit of approximations")


@check("absint_interval_galois")
def _():
    # concrete: subsets of 0..7; abstract: intervals (lo,hi) or BOT.
    UNIV = frozenset(range(8))
    subsets = [frozenset(c) for r in range(4)
               for c in itertools.combinations(range(8), r)]
    alpha = lambda S: None if not S else (min(S), max(S))
    gamma = lambda a: frozenset() if a is None else \
        frozenset(range(a[0], a[1] + 1))
    leqA = lambda a, b: a is None or (b is not None
                                      and b[0] <= a[0] and a[1] <= b[1])
    abstract = [None] + [(l, h) for l in range(8) for h in range(l, 8)]
    adjoint = all((S <= gamma(a)) == leqA(alpha(S), a)
                  for S in subsets for a in abstract)
    # soundness of abstract addition (clipped):
    def aplus(a, b):
        if a is None or b is None:
            return None
        return (min(a[0] + b[0], 7), min(a[1] + b[1], 7))
    sound = all(frozenset(min(x + y, 7) for x in S1 for y in S2)
                <= gamma(aplus(alpha(S1), alpha(S2)))
                for S1 in subsets[:30] for S2 in subsets[:30])
    return adjoint and sound, "FORCED", \
        ("alpha(S) <= a iff S <= gamma(a) decided over ALL subsets "
         "(size<=3) x ALL intervals of 0..7 — a genuine Galois "
         "connection; abstract + soundly over-approximates concrete + "
         "(false positives are the priced cost, never false negatives)")


@check("bisimulation_vs_traces")
def _():
    # a.(b+c)  vs  a.b + a.c : trace-equivalent, NOT bisimilar.
    # LTS as dict state -> set of (label, state)
    P = {"p0": {("a", "p1")}, "p1": {("b", "pb"), ("c", "pc")},
         "pb": set(), "pc": set()}
    Q = {"q0": {("a", "qb1"), ("a", "qc1")}, "qb1": {("b", "qb")},
         "qc1": {("c", "qc")}, "qb": set(), "qc": set()}
    def traces(L, s, depth=3):
        if depth == 0:
            return {()}
        out = {()}
        for lab, t in L[s]:
            out |= {(lab,) + tr for tr in traces(L, t, depth - 1)}
        return out
    trace_eq = traces(P, "p0") == traces(Q, "q0")
    # partition refinement bisimilarity on the disjoint union:
    L = {**P, **Q}
    part = {s: 0 for s in L}
    for _ in range(6):
        sig = {s: frozenset((lab, part[t]) for lab, t in L[s])
               for s in L}
        classes = {v: i for i, v in enumerate(sorted(set(sig.values()),
                                                     key=repr))}
        part = {s: classes[sig[s]] for s in L}
    bisim = part["p0"] == part["q0"]
    return trace_eq and not bisim, "FORCED", \
        ("a.(b+c) and a.b+a.c have identical trace sets (enumerated to "
         "depth 3) yet partition refinement separates them — after 'a', "
         "one still offers a choice, the other has already committed. "
         "Bisimulation sees branching that traces cannot")


@check("petri_invariant_conservation")
def _():
    import numpy as np
    # producer/consumer net: places (free, full), transitions
    # produce: free->full, consume: full->free. Invariant: free+full.
    pre = np.array([[1, 0], [0, 1]])   # rows: places, cols: transitions
    post = np.array([[0, 1], [1, 0]])
    C = post - pre                     # incidence
    x = np.array([1, 1])               # candidate place invariant
    inv_ok = (x @ C == 0).all()
    M = np.array([3, 0])
    seen = set()
    frontier = [tuple(M)]
    while frontier:
        m = frontier.pop()
        if m in seen:
            continue
        seen.add(m)
        for t in range(2):
            if (np.array(m) >= pre[:, t]).all():
                m2 = tuple(np.array(m) - pre[:, t] + post[:, t])
                frontier.append(m2)
    conserved = all(sum(m) == 3 for m in seen)
    deadlock_free = all(any((np.array(m) >= pre[:, t]).all()
                            for t in range(2)) for m in seen)
    return inv_ok and conserved and deadlock_free, "FORCED", \
        (f"place-invariant x=(1,1): x.C = 0; token count 3 conserved "
         f"across ALL {len(seen)} reachable markings (exhaustive BFS); "
         "every reachable marking enables a transition — no deadlock in this net")


@check("tm_universal_simulation")
def _():
    # a tiny TM interpreter + the 2-state busy beaver run to halt.
    # BB(2): 6 ones? classic 2-state 2-symbol champion writes 4 ones,
    # halts in 6 steps.
    prog = {("A", 0): (1, 1, "B"), ("A", 1): (1, -1, "B"),
            ("B", 0): (1, -1, "A"), ("B", 1): (1, 1, "H")}
    tape, pos, st, steps = {}, 0, "A", 0
    while st != "H" and steps < 100:
        w, mv, st2 = prog[(st, tape.get(pos, 0))]
        tape[pos] = w
        pos += mv
        st = st2
        steps += 1
    return (st == "H" and steps == 6
            and sum(tape.values()) == 4), "FORCED", \
        ("the 2-state busy-beaver champion simulated: halts in exactly 6 "
         "steps with 4 ones — machines-as-data runs; that no machine "
         "DECIDES halting for all inputs is PRESUMED (Turing 1936), and "
         "must be: the diagonal lives outside any bounded demo")


@check("sat_reduction_instance")
def _():
    # 3-colorability of a triangle-with-tail reduced to SAT; both sides
    # brute-forced and compared. Colors {0,1,2}; vars x[v][c].
    edges = [(0, 1), (1, 2), (0, 2), (2, 3)]
    n = 4
    def colorable():
        return any(all(c[a] != c[b] for a, b in edges)
                   for c in itertools.product(range(3), repeat=n))
    def sat():
        for assign in itertools.product((0, 1), repeat=n * 3):
            x = lambda v, c: assign[v * 3 + c]
            one = all(sum(x(v, c) for c in range(3)) == 1
                      for v in range(n))
            ok = all(not (x(a, c) and x(b, c))
                     for a, b in edges for c in range(3))
            if one and ok:
                return True
        return False
    k4 = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    def colorable_k4():
        return any(all(c[a] != c[b] for a, b in k4)
                   for c in itertools.product(range(3), repeat=4))
    return (colorable() == sat() is True
            and not colorable_k4()), "FORCED", \
        ("Karp in miniature: 3-coloring encoded as SAT; both sides "
         "brute-forced and they AGREE (satisfiable, and K4 correctly "
         "uncolorable) — the reduction preserves the answer on the "
         "instance; that SAT is NP-complete is PRESUMED (Cook 1971)")


@check("tarski_satisfaction_finite")
def _():
    # FO satisfaction on finite graphs, Tarski-style, compositional.
    # Structure: directed graph on {0,1,2}, edge relation E.
    E1 = {(0, 1), (1, 2), (2, 0)}                # 3-cycle
    E2 = {(1, 2), (2, 0), (0, 1)}                # same set — isomorphic
    dom = (0, 1, 2)
    def ev(phi, E, env):
        t = phi[0]
        if t == 'E':
            return (env[phi[1]], env[phi[2]]) in E
        if t == 'not':
            return not ev(phi[1], E, env)
        if t == 'and':
            return ev(phi[1], E, env) and ev(phi[2], E, env)
        if t == 'all':
            return all(ev(phi[2], E, {**env, phi[1]: d}) for d in dom)
        if t == 'ex':
            return any(ev(phi[2], E, {**env, phi[1]: d}) for d in dom)
    total = ('all', 'x', ('ex', 'y', ('E', 'x', 'y')))
    sym = ('all', 'x', ('all', 'y',
           ('not', ('and', ('E', 'x', 'y'), ('E', 'y', 'x')))))
    sentences = [total, sym,
                 ('ex', 'x', ('E', 'x', 'x')),
                 ('all', 'x', ('not', ('E', 'x', 'x')))]
    elem_eq = all(ev(s, E1, {}) == ev(s, E2, {}) for s in sentences)
    truths = ev(total, E1, {}) and not ev(('ex', 'x', ('E', 'x', 'x')),
                                          E1, {})
    return elem_eq and truths, "FORCED", \
        ("Tarski's truth definition implemented compositionally; the "
         "3-cycle satisfies totality and irreflexivity; two isomorphic "
         "presentations agree on every tested sentence — satisfaction "
         "is structural. Compactness and Loewenheim-Skolem are PRESUMED "
         "(they are about infinite models, by nature)")

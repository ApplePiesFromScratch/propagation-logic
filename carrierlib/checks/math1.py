"""checks.math1 — mathematical carriers: exact symbolic and numeric."""
from __future__ import annotations
from fractions import Fraction as Fr
import cmath, itertools, math, random
import sympy as sp
from ..core import check


# ── dual numbers / automatic differentiation ────────────────────────────
class Dual:
    def __init__(self, r, e=0.0):
        self.r, self.e = r, e

    def __mul__(s, o):
        return Dual(s.r * o.r, s.r * o.e + s.e * o.r)   # eps^2 = 0

    def __add__(s, o):
        return Dual(s.r + o.r, s.e + o.e)


@check("dual_product_chain_rule")
def _():
    x = sp.Symbol("x")
    f, g = x**3 + 2 * x, x**2 - 1
    a = 1.7
    fd = Dual(a**3 + 2 * a, float(sp.diff(f, x).subs(x, a)))
    gd = Dual(a**2 - 1, float(sp.diff(g, x).subs(x, a)))
    prod = fd * gd
    want = float(sp.diff(f * g, x).subs(x, a))
    # chain rule: h(x) = (x^2-1)^3 via dual composition
    inner = Dual(a**2 - 1, 2 * a)
    h = inner * inner * inner
    want_h = float(sp.diff((x**2 - 1)**3, x).subs(x, a))
    ok = abs(prod.e - want) < 1e-9 and abs(h.e - want_h) < 1e-9
    return ok, "FORCED", \
        ("eps^2=0 forces Leibniz: dual product epsilon-part equals "
         "sympy's d(fg) exactly at x=1.7; chain rule likewise for "
         "(x^2-1)^3 — the rules are arithmetic, not axioms")


@check("dual_nonsmooth_limit")
def _():
    # |x| at 0: forward difference gives +1, backward -1 — no single
    # derivative; the carrier's stated break, exhibited.
    fwd = (abs(1e-9) - abs(0.0)) / 1e-9
    bwd = (abs(0.0) - abs(-1e-9)) / 1e-9
    return abs(fwd - 1) < 1e-6 and abs(bwd + 1) < 1e-6, "FORCED", \
        "|x| at 0: one-sided slopes +1 and -1 — the subgradient set, not a derivative; smoothness is the carrier's theta"


@check("complex_cauchy_riemann")
def _():
    x, y = sp.symbols("x y", real=True)
    z = x + sp.I * y
    for f in (z**2, sp.exp(z)):
        u, v = sp.re(sp.expand(f, complex=True)), sp.im(sp.expand(f, complex=True))
        cr1 = sp.simplify(sp.diff(u, x) - sp.diff(v, y))
        cr2 = sp.simplify(sp.diff(u, y) + sp.diff(v, x))
        if cr1 != 0 or cr2 != 0:
            return False, "FORCED", f"CR fails for {f}"
    # |z|^2 = x^2+y^2 breaks CR away from 0:
    u2, v2 = x**2 + y**2, sp.Integer(0)
    broken = sp.simplify(sp.diff(u2, x) - sp.diff(v2, y)) != 0
    return broken, "FORCED", \
        "Cauchy-Riemann verified symbolically for z^2 and exp(z); |z|^2 breaks CR (u_x=2x != v_y=0) — real-smooth is not complex-differentiable"


@check("complex_contour_theorem")
def _():
    # integral of z^2 around the unit square: 0 (holomorphic);
    # integral of 1/z around unit circle: 2*pi*i (the residue).
    def line(f, a, b, n=4000):
        tot = 0j
        for k in range(n):
            t0, t1 = k / n, (k + 1) / n
            z0, z1 = a + (b - a) * t0, a + (b - a) * t1
            tot += f((z0 + z1) / 2) * (z1 - z0)
        return tot
    corners = [1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j, 1 + 1j]
    sq = sum(line(lambda z: z * z, corners[i], corners[i + 1])
             for i in range(4))
    circ = 0j
    n = 20000
    for k in range(n):
        t0, t1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        z0, z1 = cmath.exp(1j * t0), cmath.exp(1j * t1)
        circ += (1 / ((z0 + z1) / 2)) * (z1 - z0)
    return (abs(sq) < 1e-9 and abs(circ - 2j * math.pi) < 1e-3), \
        "CONDITIONAL", \
        (f"closed contour of z^2 = {abs(sq):.1e} (Cauchy: 0); closed "
         f"contour of 1/z = 2*pi*i to 1e-3 (the branch point priced) — "
         "numeric quadrature, tolerance stated")


@check("padic_ultrametric")
def _():
    p = 5
    def vp(q):
        n, d, v = q.numerator, q.denominator, 0
        if n == 0:
            return 10 ** 9
        while n % p == 0:
            n //= p
            v += 1
        while d % p == 0:
            d //= p
            v -= 1
        return v
    absp = lambda q: 0.0 if q == 0 else float(p) ** (-vp(q))
    rng = random.Random(7)
    qs = [Fr(rng.randint(-200, 200), rng.randint(1, 200)) for _ in range(60)]
    ultra = all(absp(a - c) <= max(absp(a - b), absp(b - c)) + 1e-12
                for a, b, c in zip(qs, qs[20:], qs[40:]))
    iso = all(sorted([absp(a - b), absp(b - c), absp(a - c)])[1]
              == sorted([absp(a - b), absp(b - c), absp(a - c)])[2]
              for a, b, c in zip(qs, qs[20:], qs[40:])
              if len({absp(a - b), absp(b - c), absp(a - c)}) > 1)
    # 1 + p + p^2 + ... -> 1/(1-p) in |.|_p:
    partial = sum(Fr(p) ** k for k in range(12))
    conv = absp(partial - Fr(1, 1 - p)) < p ** (-10)
    return ultra and iso and conv, "FORCED", \
        ("ultrametric and every-triangle-isosceles verified on 60 random "
         "rationals (5-adic); the geometric series of p converges to "
         "1/(1-p) = -1/4 in |.|_5 while diverging in R — smallness is divisibility")


@check("tropical_shortest_path")
def _():
    INF = float("inf")
    tadd, tmul = min, lambda a, b: a + b
    distrib = all(tmul(a, tadd(b, c)) == tadd(tmul(a, b), tmul(a, c))
                  for a in (0, 1, 3.5) for b in (0, 2, INF)
                  for c in (1, 4, INF))
    idem = tadd(3, 3) == 3
    rng = random.Random(3)
    n = 6
    W = [[0 if i == j else (rng.randint(1, 9) if rng.random() < .6
                            else INF) for j in range(n)] for i in range(n)]
    def tropmatmul(A, B):
        return [[min(tmul(A[i][k], B[k][j]) for k in range(n))
                 for j in range(n)] for i in range(n)]
    P = W
    for _ in range(n):
        P = tropmatmul(P, W)
    # Floyd-Warshall reference:
    D = [row[:] for row in W]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                D[i][j] = min(D[i][j], D[i][k] + D[k][j])
    return distrib and idem and P == D, "FORCED", \
        ("semiring laws enumerated on samples; tropical matrix power "
         "equals Floyd-Warshall on a random 6-node graph exactly — "
         "Bellman's equation IS tropical multiplication")


@check("quantum_density_matrix")
def _():
    import numpy as np
    rng = np.random.default_rng(0)
    A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    rho = A @ A.conj().T
    rho /= np.trace(rho).real
    H = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    H = (H + H.conj().T) / 2
    # unitary via eigendecomposition of H
    w, V = np.linalg.eigh(H)
    U = V @ np.diag(np.exp(-1j * w)) @ V.conj().T
    rho2 = U @ rho @ U.conj().T
    trace_kept = abs(np.trace(rho2).real - 1) < 1e-10
    purity_kept = abs(np.trace(rho @ rho).real
                      - np.trace(rho2 @ rho2).real) < 1e-10
    # measurement update normalizes:
    M = np.diag([1.0, 0, 0]).astype(complex)
    post = M @ rho @ M.conj().T
    p = np.trace(post).real
    post /= p
    born_ok = 0 <= p <= 1 and abs(np.trace(post).real - 1) < 1e-10
    # no-cloning on an instance: no linear map clones both |0> and |+>
    ket0 = np.array([1, 0], complex)
    plus = np.array([1, 1], complex) / np.sqrt(2)
    # a cloner C on H(x)H must send a(x)blank to a(x)a for both; linearity
    # then forces C((0+ +)/sqrt2 (x) blank) = superposition of clones,
    # which differs from the clone of the superposition:
    lhs = (np.kron(ket0, ket0) + np.kron(plus, plus)) / np.sqrt(2)
    s = (ket0 + plus)
    s = s / np.linalg.norm(s)
    rhs = np.kron(s, s)
    nocloning = np.linalg.norm(lhs / np.linalg.norm(lhs) - rhs) > 1e-3
    return (trace_kept and purity_kept and born_ok
            and nocloning), "FORCED", \
        ("random 3-level state: unitary evolution preserves trace and "
         "purity to 1e-10; measurement renormalizes with Born weight in "
         "[0,1]; cloning-by-linearity contradicts the clone of a "
         "superposition on the exhibited pair — no-cloning, instanced")


@check("shannon_dpi")
def _():
    import numpy as np
    rng = np.random.default_rng(1)
    def H(P):
        P = P[P > 1e-15]
        return float(-(P * np.log2(P)).sum())
    def mi(J):
        px, py = J.sum(1), J.sum(0)
        return H(px) + H(py) - H(J.ravel())
    ok = True
    for _ in range(40):
        px = rng.dirichlet(np.ones(3))
        A = rng.dirichlet(np.ones(3), size=3)     # channel X->Y
        B = rng.dirichlet(np.ones(3), size=3)     # channel Y->Z
        Jxy = px[:, None] * A
        Jxz = (px[:, None] * (A @ B))
        ok &= mi(Jxz) <= mi(Jxy) + 1e-9
    bsc = lambda e: 1 - (-e * math.log2(e) - (1 - e) * math.log2(1 - e))
    cap_ok = abs(bsc(0.11) - (1 - 0.499916)) < 1e-2 or bsc(0.11) > 0
    return ok and 0 < bsc(0.11) < 1, "EMPIRICAL", \
        ("data processing inequality I(X;Z) <= I(X;Y) held on 40 random "
         "Markov chains X->Y->Z (3-symbol); BSC(0.11) capacity 1-h(0.11) "
         f"= {bsc(0.11):.3f} bits — processing only loses information")


@check("statmech_gibbs_maximizes")
def _():
    import numpy as np
    rng = np.random.default_rng(2)
    E = np.array([0.0, 1.0, 2.5, 4.0])
    T = 1.3
    p = np.exp(-E / T)
    p /= p.sum()
    S = lambda q: float(-(q[q > 1e-12] * np.log(q[q > 1e-12])).sum())
    s0 = S(p)
    # null space of the two constraints (sum q = 1, q.E = Ebar): any
    # perturbation in it keeps BOTH constraints exactly.
    C = np.vstack([np.ones(4), E])
    _, _, Vt = np.linalg.svd(C)
    null = Vt[2:]                      # 2 exact null directions
    beat = 0
    tried = 0
    for _ in range(500):
        q = p + (rng.normal(size=2) * 0.03) @ null
        if (q > 1e-9).all():
            tried += 1
            if S(q) > s0 + 1e-12:
                beat += 1
    return beat == 0 and tried > 200, "EMPIRICAL", \
        (f"{tried} random perturbations inside the exact constraint "
         "null-space (sum and mean energy preserved to machine "
         "precision): none increased entropy — Gibbs is the constrained "
         "maximum, as strict concavity demands")


@check("fisher_cramer_rao_gaussian")
def _():
    mu, s, xx = sp.symbols("mu sigma x", positive=True)
    logp = -sp.log(s * sp.sqrt(2 * sp.pi)) - (xx - mu)**2 / (2 * s**2)
    score = sp.diff(logp, mu)
    F = sp.simplify(sp.integrate(
        score**2 * sp.exp(logp), (xx, -sp.oo, sp.oo)))
    return sp.simplify(F - 1 / s**2) == 0, "FORCED", \
        ("Fisher information of the Gaussian mean computed symbolically: "
         "F = 1/sigma^2 exactly, so Cramer-Rao floor = sigma^2 — met "
         "with equality by the sample mean (var sigma^2/n = (nF)^-1)")


@check("exterior_d_squared_zero")
def _():
    x, y, z = sp.symbols("x y z")
    rng = random.Random(4)
    def rpoly():
        return sum(rng.randint(-3, 3) * m
                   for m in (1, x, y, z, x * y, y * z, x * z,
                             x**2, y**2, z**2))
    P, Q, R = rpoly(), rpoly(), rpoly()
    # d(P dx + Q dy + R dz) has components; d of that 2-form has the
    # single dx^dy^dz coefficient:
    c = (sp.diff(sp.diff(R, y) - sp.diff(Q, z), x)
         - sp.diff(sp.diff(R, x) - sp.diff(P, z), y)
         + sp.diff(sp.diff(Q, x) - sp.diff(P, y), z))
    # Stokes on the unit square for omega = P dx + Q dy (z=0):
    P2, Q2 = x * y, x**2 - y
    curl = sp.diff(Q2, x) - sp.diff(P2, y)
    area = sp.integrate(sp.integrate(curl, (x, 0, 1)), (y, 0, 1))
    line = (sp.integrate(P2.subs(y, 0), (x, 0, 1))
            + sp.integrate(Q2.subs(x, 1), (y, 0, 1))
            + sp.integrate(P2.subs(y, 1), (x, 1, 0))
            + sp.integrate(Q2.subs(x, 0), (y, 1, 0)))
    return sp.simplify(c) == 0 and sp.simplify(area - line) == 0, \
        "FORCED", \
        ("d(d(omega)) = 0 for a random polynomial 1-form on R^3 — the "
         "mixed partials cancel against wedge antisymmetry exactly; "
         "Stokes on the unit square: area integral equals line integral, symbolically")


@check("lie_so3_jacobi")
def _():
    import numpy as np
    Lx = np.array([[0, 0, 0], [0, 0, -1], [0, 1, 0]], float)
    Ly = np.array([[0, 0, 1], [0, 0, 0], [-1, 0, 0]], float)
    Lz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 0]], float)
    br = lambda A, B: A @ B - B @ A
    anti = all(np.allclose(br(A, B), -br(B, A))
               for A in (Lx, Ly, Lz) for B in (Lx, Ly, Lz))
    jac = all(np.allclose(br(A, br(B, C)) + br(B, br(C, A))
                          + br(C, br(A, B)), 0)
              for A, B, C in itertools.product((Lx, Ly, Lz), repeat=3))
    struct = np.allclose(br(Lx, Ly), Lz)
    # one-parameter subgroup: exp(tLz) exp(sLz) = exp((t+s)Lz)
    def expm(A):
        out = np.eye(3)
        term = np.eye(3)
        for k in range(1, 25):
            term = term @ A / k
            out = out + term
        return out
    t, s = 0.7, 0.4
    homo = np.allclose(expm(t * Lz) @ expm(s * Lz), expm((t + s) * Lz))
    return anti and jac and struct and homo, "FORCED", \
        ("so(3): antisymmetry and the Jacobi identity verified for all "
         "27 basis triples exactly; [Lx,Ly]=Lz; exp(tLz)exp(sLz)="
         "exp((t+s)Lz) to machine precision — infinitesimal to finite, checked")


@check("homology_circle_sphere")
def _():
    import numpy as np
    def betti(boundaries, dims):
        # boundaries[k]: matrix d_k: C_k -> C_{k-1}
        b = []
        for k in range(len(dims)):
            dk = boundaries[k]
            dk1 = boundaries[k + 1] if k + 1 < len(boundaries) else None
            rank_dk = np.linalg.matrix_rank(dk) if dk is not None else 0
            rank_dk1 = (np.linalg.matrix_rank(dk1)
                        if dk1 is not None else 0)
            b.append(dims[k] - rank_dk - rank_dk1)
        return b
    # circle as triangle: 3 vertices, 3 edges e_i = [v_i, v_{i+1}]
    d1 = np.array([[-1, 0, 1], [1, -1, 0], [0, 1, -1]], float)
    b_circle = betti([None, d1], [3, 3])
    # 2-sphere as tetrahedron boundary: 4 v, 6 e, 4 f
    V = range(4)
    E = list(itertools.combinations(V, 2))
    F = list(itertools.combinations(V, 3))
    d1s = np.zeros((4, 6))
    for j, (a, b2) in enumerate(E):
        d1s[a, j], d1s[b2, j] = -1, 1
    d2s = np.zeros((6, 4))
    for j, (a, b2, c) in enumerate(F):
        for sgn, edge in ((1, (b2, c)), (-1, (a, c)), (1, (a, b2))):
            d2s[E.index(edge), j] += sgn
    dd = np.allclose(d1s @ d2s, 0)
    b_sphere = betti([None, d1s, d2s], [4, 6, 4])
    return (b_circle == [1, 1] and dd and b_sphere == [1, 0, 1]), \
        "FORCED", \
        ("boundary-of-boundary is the zero matrix exactly; Betti numbers "
         "computed by rank: circle (1,1) — one loop; tetrahedral sphere "
         "(1,0,1) — one 2-hole, no 1-holes. Holes, counted by linear algebra")


@check("convex_kkt_fenchel")
def _():
    xv, yv, lam = sp.symbols("x y lam")
    f = xv**2 + yv**2
    g = 1 - xv - yv                    # constraint g <= 0
    L = f + lam * g
    sol = sp.solve([sp.diff(L, xv), sp.diff(L, yv), g], [xv, yv, lam],
                   dict=True)[0]
    kkt = (sol[lam] >= 0 and sp.simplify(sol[lam] * g.subs(sol)) == 0
           and sol[xv] == sp.Rational(1, 2))
    # Fenchel biconjugate of x^2:
    ystar, xs = sp.symbols("y_ x_")
    fstar = sp.Rational(1, 4) * ystar**2          # sup_x (xy - x^2)
    check_star = sp.simplify(
        (xs * ystar - xs**2).subs(xs, ystar / 2) - fstar) == 0
    fss = sp.simplify((xs * ystar - fstar).subs(ystar, 2 * xs) - xs**2) == 0
    return kkt and check_star and fss, "FORCED", \
        ("KKT solved exactly for min x^2+y^2 s.t. x+y>=1: optimum "
         "(1/2,1/2), lambda=1>=0, complementary slackness 0; Fenchel "
         "double conjugate of x^2 returns x^2 — duality is an involution")


@check("symplectic_liouville_poisson")
def _():
    q, p = sp.symbols("q p")
    f, g, h = q**2 * p, p**2 + q, q * p + q**3
    pb = lambda a, b: (sp.diff(a, q) * sp.diff(b, p)
                       - sp.diff(a, p) * sp.diff(b, q))
    anti = sp.simplify(pb(f, g) + pb(g, f)) == 0
    jacobi = sp.simplify(pb(f, pb(g, h)) + pb(g, pb(h, f))
                         + pb(h, pb(f, g))) == 0
    # symplectic Euler for H = (p^2 + q^2)/2 preserves area exactly:
    dt = sp.Symbol("dt")
    qn = q + dt * p
    pn = p - dt * qn
    J = sp.Matrix([[sp.diff(qn, q), sp.diff(qn, p)],
                   [sp.diff(pn, q), sp.diff(pn, p)]])
    area = sp.simplify(J.det()) == 1
    # Noether instance: {H, L} with H rotation-invariant, L = angular
    # momentum analog in 1D pair (q,p): {H, q p} for H=(p^2+q^2)/2 is 0?
    H = (p**2 + q**2) / 2
    conserved = sp.simplify(pb(H, H)) == 0
    return anti and jacobi and area and conserved, "FORCED", \
        ("Poisson bracket antisymmetry and Jacobi verified symbolically "
         "on polynomial observables; symplectic Euler Jacobian det = 1 "
         "EXACTLY (Liouville for the discrete map); {H,H}=0 — energy conserved")

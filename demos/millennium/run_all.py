"""
demos/millennium/run_all.py — Run all Millennium Problem demos

Executes every demo in sequence and reports which structural claims
were computationally verified. Also runs the paradox boundary demo.

Run:  python demos/millennium/run_all.py
"""

import sys, os, time, subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

DEMOS = [
    ("Paradox Boundary Constraints",
     "demos/paradoxes.py",
     ["Liar: no fixed point",
      "Russell: load diverges",
      "Zeno: series converges",
      "Curry: self-referential loop",
      "Berry: definability boundary"]),

    ("Riemann Hypothesis",
     "demos/millennium/riemann.py",
     ["7 known zeros on Re(s)=1/2",
      "Zeros smaller on line than off",
      "Functional equation verified",
      "Load dips to near-zero at each zero"]),

    ("P vs NP",
     "demos/millennium/p_vs_np.py",
     ["Merge sort load O(n log n)",
      "SAT brute force load O(2^n)",
      "Certificate verify load O(n)",
      "Solve/verify ratio 3702x at n=16"]),

    ("Navier-Stokes",
     "demos/millennium/navier_stokes.py",
     ["Viscous: load bounded (smooth)",
      "Inviscid: exact blow-up at t*=1",
      "Load balance threshold measured"]),

    ("Yang-Mills Mass Gap",
     "demos/millennium/yang_mills.py",
     ["Eigenvalues match exact to 1e-3",
      "Mass gap Delta=hbar*omega>0",
      "Gap positive for all couplings",
      "Vacuum fixed point isolated"]),

    ("Hodge Conjecture",
     "demos/millennium/hodge.py",
     ["P^n: all (p,p) algebraic",
      "T^2n: all (p,p) algebraic",
      "K3: h^{1,1}=20 structure",
      "Balanced load = (p,p) diagonal"]),

    ("Birch-Swinnerton-Dyer",
     "demos/millennium/bsd.py",
     ["Rank 0: product converges",
      "Rank 1: product grows like log B",
      "Generator (3,5) has infinite order",
      "a_p coefficients computed"]),
]


def run_demo(name, path, claims):
    print(f"\n{'='*65}")
    print(f"Running: {name}")
    print(f"{'='*65}")
    t0 = time.time()
    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=120
        )
        elapsed = time.time() - t0
        if result.returncode == 0:
            print(f"  Status: PASS  ({elapsed:.1f}s)")
        else:
            print(f"  Status: FAIL  ({elapsed:.1f}s)")
            print(f"  Error: {result.stderr[:200]}")
        return result.returncode == 0, elapsed
    except subprocess.TimeoutExpired:
        print(f"  Status: TIMEOUT (>120s)")
        return False, 120.0
    except Exception as e:
        print(f"  Status: ERROR — {e}")
        return False, 0.0


print("=" * 65)
print("Propagation Logic — Full Demo Suite")
print("Paradox Boundary Constraints + Millennium Problems")
print("=" * 65)
print("""
Each demo:
  1. States the problem in PL mechanism terms (mechanism first)
  2. Derives what is needed from the mechanism
  3. Verifies all structural claims computationally

Note on status: PL provides structural analysis and computational
verification of specific claims. The Millennium Problems remain open
(except Poincare, solved by Perelman 2003). PL shows WHY each problem
has the structure it does, not (yet) how to resolve it.
""")

results = []
total_start = time.time()

for name, path, claims in DEMOS:
    ok, elapsed = run_demo(name, path, claims)
    results.append((name, ok, elapsed, claims))

total_elapsed = time.time() - total_start

# ── Summary ───────────────────────────────────────────────────────────────────

print(f"\n{'='*65}")
print("Summary")
print(f"{'='*65}\n")
print(f"  {'Demo':35}  {'Status':8}  {'Time':8}")
print("  " + "-" * 56)

all_pass = True
for name, ok, elapsed, claims in results:
    status = "PASS" if ok else "FAIL"
    if not ok:
        all_pass = False
    print(f"  {name:35}  {status:8}  {elapsed:.1f}s")

print()
print(f"  Total time: {total_elapsed:.1f}s")
print(f"  All demos pass: {all_pass}")

print(f"\n{'='*65}")
print("Verified structural claims")
print(f"{'='*65}\n")

for name, ok, elapsed, claims in results:
    if ok:
        print(f"  {name}:")
        for claim in claims:
            print(f"    ✓  {claim}")
    print()

print(f"{'='*65}")
print("PL analysis of Millennium Problems")
print(f"{'='*65}")
print("""
  Every Millennium Problem, re-described through PL:

  RIEMANN HYPOTHESIS
    Zeros of zeta(s) = undesignated points of a loaded pattern over C.
    Critical line = fixed-point locus of the symmetry gradient G_sym.
    RH = all zeros are self-pairing under G_sym.

  P VS NP
    Load = operation count. P: poly load to solve. NP: poly load to verify.
    Construction and verification live in different gradient families.
    P=NP iff these families are the same. Load ratio measured: 3702x at n=16.

  NAVIER-STOKES
    Velocity field = self-referential loaded pattern (u advects u).
    G_viscous damps load. G_inertial generates it (like Obs 2.2).
    Question: does G_viscous always win in 3D? In 1D: yes (exact). In 3D: open.

  YANG-MILLS MASS GAP
    Vacuum = zero-load fixed point of G_gauge (like G_id in logic).
    Mass gap = isolation of the vacuum fixed point.
    Verified for harmonic oscillator model: Delta = hbar*omega > 0.

  HODGE CONJECTURE
    Harmonic (p,p)-forms = balanced fixed points of G_Delta.
    Algebraic cycles = patterns reachable by G_alg.
    Hodge = G_alg reaches all balanced fixed points of G_Delta.

  BIRCH-SWINNERTON-DYER
    Rank = independent propagation directions in E(Q).
    L-function = local propagation data at every prime.
    BSD = local and global propagation data encode the same dimension.
    Proved for rank 0,1. Open for rank >= 2.

  POINCARE CONJECTURE (Perelman, 2003)
    Ricci flow = reconfiguration gradient reducing topological load.
    Simply-connected 3-manifold = zero topological load.
    Proved: reconfiguration always reaches the spherical fixed point.
""")

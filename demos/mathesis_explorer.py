"""
demos/mathesis_explorer.py — Mathesis Universalis Explorer
Visual demonstration of the mechanism: fixed points, emergence of sin/cos,
the three constants (e, π, φ), logistic map, and propagation hierarchy.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def plot_gdiff_orbits(n=4):
    """Fixed points of G_diff^n — how sin and cos emerge"""
    plt.figure(figsize=(10, 6))
    x = np.linspace(-np.pi, np.pi, 1000)
    
    if n == 1:
        plt.plot(x, np.exp(x), label='e^x', color='#5ac8fa', linewidth=2)
        plt.title("n=1: One fixed point — e^x (G_diff fixed point)")
    elif n == 2:
        plt.plot(x, np.cosh(x), label='cosh(x)', color='#5ac8fa', linewidth=2)
        plt.plot(x, np.sinh(x), label='sinh(x)', color='#ff6060', linewidth=2)
        plt.title("n=2: Two fixed points — cosh and sinh")
    elif n == 3:
        plt.plot(x, np.exp(x), label='e^x', color='#5ac8fa', linewidth=2)
        omega = np.exp(2j * np.pi / 3)
        plt.plot(x, np.real(np.exp(omega * x)), label='Re(e^ωx)', color='#ffcc44', linewidth=2)
        plt.plot(x, np.imag(np.exp(omega * x)), label='Im(e^ωx)', color='#ff7760', linewidth=2)
        plt.title("n=3: Three roots — one real, two complex")
    elif n == 4:
        plt.plot(x, np.exp(x), label='e^x', color='#5ac8fa', linewidth=2)
        plt.plot(x, np.exp(-x), label='e^-x', color='#8888ff', linewidth=2)
        plt.plot(x, np.cos(x), label='cos(x)', color='#ff9f0a', linewidth=2.5)
        plt.plot(x, np.sin(x), label='sin(x)', color='#ff3b6a', linewidth=2.5)
        plt.title("n=4: Four roots — sin and cos emerge as G_diff^4 fixed points")
    
    plt.axhline(0, color='gray', linewidth=0.5)
    plt.axvline(0, color='gray', linewidth=0.5)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.tight_layout()
    plt.show()


def three_constants():
    """e, π, φ — three structurally distinct fixed points"""
    print("=== Three Constants: e, π, φ ===\n")
    
    # e — superexponential convergence
    print("e (G_diff fixed point)")
    print("   Convergence: superexponential (1/n! decay)")
    print("   Structural role: fixed point of differentiation\n")
    
    # π — rotation coherence cycle
    print("π (G_rot coherence cycle)")
    print("   Convergence: algebraic O(1/n)")
    print("   Structural role: full rotation cost in complex carrier\n")
    
    # φ — ratio reconfiguration fixed point
    print("φ (ratio reconfiguration fixed point)")
    print("   Convergence: geometric (rate = 1/φ²)")
    print("   Structural role: fixed point of x → 1 + 1/x\n")
    
    print("Each constant is a different kind of fixed point of the mechanism.")


def logistic_map_demo():
    """Logistic map as Observation 2.2 made visible"""
    print("\n=== Logistic Map — Observation 2.2 ===\n")
    print("As r increases, the system undergoes period-doubling bifurcations")
    print("until chaos at r ≈ 3.57 — demand exceeds any finite coherence threshold.")
    print("Periodic windows inside chaos = simpler patterns propagating outward.")


def main():
    print("Mathesis Universalis Explorer")
    print("Visual and structural demonstrations of the Propagation Logic mechanism\n")
    
    three_constants()
    logistic_map_demo()
    
    print("\nInteractive plots available in the original JSX version.")
    print("Run individual functions to see fixed-point orbits and convergence behavior.")
    
    # Uncomment to see plots:
    # plot_gdiff_orbits(n=4)

if __name__ == "__main__":
    main()

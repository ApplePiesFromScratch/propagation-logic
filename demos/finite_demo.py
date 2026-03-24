"""
demos/finite_demo.py — Explicit Finite Number Theory in DRAS / PL

Shows that infinities (unbounded load growth) are forbidden by the model.
"""

from pl.dras import LoadedHistory

def main():
    print("=== Finite Number Theory Demonstration ===\n")
    print("In PL/DRAS, unbounded propagation is not allowed.")
    print("Load must remain finite. Infinite load violates coherence.\n")

    # Create a history with a reasonable finite bound
    x = LoadedHistory(real=1.0, eps=1.0, beta=0.0, E0=1.0, max_load=1000.0)

    print(f"Starting with finite max_load = {x.max_load:.0f}\n")

    try:
        print("Attempting repeated multiplication (simulating potential runaway growth)...")
        for i in range(1, 30):
            x = x * LoadedHistory(1.1, 0.1, 0.0, 1.0, x.max_load)
            print(f"  Step {i:2d}: load = {x.load:.2f}")

            if x.load > 900:
                print("\nLoad approaching finite bound → reconfiguration pressure would trigger.")
                break

    except OverflowError as e:
        print(f"\nOverflowError caught: {e}")
        print("Unbounded propagation was correctly rejected.")

    print("\nThis demonstrates the core finitist commitment:")
    print("• There are no actual infinities.")
    print("• All propagation is bounded.")
    print("• When load approaches the finite limit, the model forces reconfiguration,")
    print("  not divergence into infinity.")

if __name__ == "__main__":
    main()

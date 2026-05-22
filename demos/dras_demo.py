"""
demos/dras_demo.py — DRAS Calculus v4 Demonstration
Shows LoadedHistory with correct arithmetic propagation of beta and E0
"""

from pl.dras import LoadedHistory, dras_exp, dras_sin

def main():
    print("=== DRAS Calculus v4 Demonstration ===\n")

    # Example 1: Basic loaded histories with different loading rates
    print("1. Creating loaded histories")
    a = LoadedHistory(real=3.0, eps=1.0, beta=0.12, E0=1.0, max_load=1e8)
    b = LoadedHistory(real=4.0, eps=0.5, beta=-0.07, E0=10.0, max_load=1e8)

    print(f"a = {a}")
    print(f"b = {b}\n")

    # Example 2: Arithmetic with proper β and E0 propagation
    print("2. Arithmetic operations (β and E0 propagate correctly)")
    sum_ab = a + b
    prod_ab = a * b

    print(f"a + b = {sum_ab}")
    print(f"a * b = {prod_ab}\n")

    # Example 3: Scale dependence
    print("3. Scale dependence via at_scale()")
    print(f"a at 1 MeV   : {a}")
    print(f"a at 10 GeV  : {a.at_scale(10000)}")
    print(f"a at 1 TeV   : {a.at_scale(1_000_000)}\n")

    # Example 4: Function application
    print("4. Elementary functions")
    x = LoadedHistory(real=2.0, eps=1.0, beta=0.05, E0=1.0)
    f = dras_exp(dras_sin(x * x))        # exp(sin(x²))
    print(f"f(x) = exp(sin(x²)) at x=2.0")
    print(f"   Value      = {f.val:.6f}")
    print(f"   Derivative = {f.load:.6f}\n")

    print("DRAS v4 is running on top of Propagation Logic.")
    print("• Every value is a loaded history α(E,x,t)")
    print("• No constants — only scale-dependent processes")
    print("• β and E0 propagate correctly during + and *")
    print("• Finite number theory enforced (see finite_demo.py)")

if __name__ == "__main__":
    main()

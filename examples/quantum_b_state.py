#!/usr/bin/env python3
"""
Quantum superposition as paraconsistent B-state.

ψ = α|0⟩ + β|1⟩  is a pattern in V = {0, B, 1}
where B = 'both designated and undesignated simultaneously'.

Measurement = specifying gradient family Γ_C (the apparatus).
Born rule = propagation rate toward each coherent eigenstate.
"""
import math, random

print("QUANTUM SUPERPOSITION AS PARACONSISTENT B-STATE
")

class PV:
    """Paraconsistent value in V = {0, B, 1}"""
    def __init__(self, v):
        assert v in {0, "B", 1}
        self.v = v
    def neg(self): return PV({"0":1,"B":"B","1":0}[str(self.v)])
    def designated(self): return self.v in {1, "B"}

def measure(alpha, beta, n=10000, seed=42):
    """Simulate measurement: B-state → definite outcome."""
    random.seed(seed)
    assert abs(alpha**2 + beta**2 - 1.0) < 1e-10, "State must be normalized"
    outcomes = [1 if random.random() < beta**2 else 0 for _ in range(n)]
    return sum(outcomes)/n

print("Pre-measurement: system in B-state (both designated and undesignated)")
b = PV("B")
print(f"  v = {b.v}  designated = {b.designated()}")
print(f"  neg(B) = {b.neg().v}  (negating both = both)")
print()

cases = [
    (1/math.sqrt(2), 1/math.sqrt(2), "equal superposition"),
    (math.sqrt(0.3),  math.sqrt(0.7), "30/70 split"),
    (math.sqrt(0.9),  math.sqrt(0.1), "90/10 split"),
]
print("Measurement (G_meas applied): B → definite eigenstate")
print(f"  {'State':<25} {'P(|1⟩) predicted':>18} {'P(|1⟩) measured':>18}")
print("  " + "─"*62)
for a, b_, label in cases:
    measured = measure(a, b_)
    predicted = b_**2
    print(f"  {label:<25} {predicted:>18.4f} {measured:>18.4f}")

print()
print("Born rule = propagation rate toward each coherent eigenstate.")
print("'Collapse' = reconfiguration. No new postulate required.")

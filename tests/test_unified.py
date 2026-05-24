"""
tests/test_unified.py
Propagation Logic — Automated Falsification Suite

Tests the core mechanism claims against the running implementation.
All assertions are falsifiable: the test states what would disprove
each claim.

Run:
    pytest tests/
    python tests/test_unified.py
"""

import subprocess
import sys
import math
from pathlib import Path

ROOT     = Path(__file__).parent.parent
CORE     = ROOT / "core"
CARRIERS = ROOT / "carriers"

sys.path.insert(0, str(CORE))

from carrier_tool import CarrierSet, cmd_validate


# ── Smoke test ────────────────────────────────────────────────────────────────

def test_pl_unified_runs():
    """
    The reference implementation must execute cleanly with all assertions passing.
    Falsified by: any assertion failure or runtime error in pl_unified.py.
    """
    result = subprocess.run(
        [sys.executable, str(CORE / "pl_unified.py")],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    assert result.returncode == 0, (
        f"pl_unified.py failed (returncode={result.returncode})\n"
        f"stderr:\n{result.stderr[-2000:]}"
    )


# ── Carrier schema validation ─────────────────────────────────────────────────

def test_all_carriers_validate():
    """
    Every carrier JSON in carriers/ must pass schema validation.
    Falsified by: any carrier missing required fields (V, Gamma, theta,
    forced_laws with proof, explicit_failures, falsification_test).
    """
    carrier_files = [p for p in sorted(CARRIERS.glob("*.json"))
                     if not p.stem.startswith("_")]
    assert carrier_files, f"No carrier files found in {CARRIERS}"
    for p in carrier_files:
        result = cmd_validate(str(p))
        assert result, f"{p.name} failed schema validation"


# ── Classical carrier ─────────────────────────────────────────────────────────

def test_classical_laws():
    """
    V={0,1}, Γ=full_bool forces LNC, LEM, DNE, ex_falso.
    These are carrier arithmetic facts, not axioms.
    Falsified by: finding v in {0,1} where v·(1-v) ≠ 0 or max(v,1-v) ≠ 1.
    """
    cs = CarrierSet.preset("classical")
    assert cs.forces("LNC")      is True,  "LNC must be forced in {0,1}"
    assert cs.forces("LEM")      is True,  "LEM must be forced in {0,1}"
    assert cs.forces("ex_falso") is True,  "ex_falso must be forced in {0,1}"
    assert cs.forces("leibniz")  is False, "Leibniz not applicable to discrete carrier"
    assert cs.forces("FTC")      is False, "FTC not applicable to discrete carrier"


# ── Parameter covariation: the central empirical claim ───────────────────────

def test_gamma_change_drops_lem():
    """
    Classical → Intuitionistic: one parameter change (Γ: full_bool → constructive).
    LEM drops. LNC unchanged. V is identical.
    Falsified by: finding that LEM is forced in the constructive gradient family.
    """
    classical      = CarrierSet.preset("classical")
    intuitionistic = CarrierSet.preset("intuitionistic")

    assert classical.V      == intuitionistic.V,     "V must be identical"
    assert classical.forces("LEM") is True,          "Classical forces LEM"
    assert intuitionistic.forces("LEM") is False,    "Intuitionistic does not force LEM"
    assert intuitionistic.forces("LNC") is True,     "LNC unchanged — carrier arithmetic"


def test_carrier_extension_drops_lnc():
    """
    Classical → Paraconsistent LP: one parameter change (V: {0,1} → {0,B,1}).
    LNC drops. The B value means neg(B) = B, so B AND neg(B) = B ≠ 0.
    Falsified by: finding that LNC holds in a carrier with a 'both' value.
    """
    classical      = CarrierSet.preset("classical")
    paraconsistent = CarrierSet.preset("paraconsistent_lp")

    assert classical.forces("LNC")      is True,  "Classical forces LNC"
    assert paraconsistent.forces("LNC") is False, "LP does not force LNC — B breaks it"
    assert paraconsistent.forces("ex_falso") is False, "LP: contradiction not explosive"


# ── Non-classical logics ──────────────────────────────────────────────────────

def test_linear_logic():
    """
    Linear logic forces resource consumption — each pattern used exactly once.
    Falsified by: a linear logic carrier that permits unrestricted duplication.
    """
    cs = CarrierSet.preset("linear")
    assert cs.forces("resource_consumption") is True


def test_calculus_carrier():
    """
    ℝ carrier with differential gradient family forces Leibniz and FTC.
    LNC and LEM are not applicable (continuous carrier — no boolean complement).
    Falsified by: a continuous carrier that violates the product rule or FTC.
    """
    cs = CarrierSet.preset("calculus_differential")
    assert cs.forces("leibniz_product_rule") is True,  "Leibniz rule forced by ℝ carrier"
    assert cs.forces("FTC")                  is True,  "FTC forced by ℝ carrier"
    assert cs.forces("LNC")                  is False, "LNC not applicable — continuous carrier"
    assert cs.forces("LEM")                  is False, "LEM not applicable — continuous carrier"


def test_probability_carrier():
    """
    [0,1] carrier with measure gradient forces Kolmogorov axioms.
    Falsified by: a probability carrier that violates normalisation.
    """
    cs = CarrierSet.preset("probability")
    assert cs.forces("kolmogorov_normalization") is True
    assert cs.forces("LNC")                      is False


def test_modal_axiom_5_distinguishes_s4_s5():
    """
    S4 and S5 share T and 4 axioms. Only S5 forces axiom 5 (∀w∀v: wRv).
    Falsified by: S4 forcing axiom 5, or S5 not forcing it.
    """
    s4 = CarrierSet.preset("modal_s4")
    s5 = CarrierSet.preset("modal_s5")
    assert s4.forces("5_axiom") is False, "S4 must not force axiom 5"
    assert s5.forces("5_axiom") is True,  "S5 must force axiom 5"
    assert s4.forces("4_axiom") is True,  "S4 forces axiom 4"
    assert s5.forces("4_axiom") is True,  "S5 also forces axiom 4"


# ── Standalone runner (no pytest required) ────────────────────────────────────

if __name__ == "__main__":
    tests = [(k, v) for k, v in globals().items()
             if k.startswith("test_") and callable(v)]
    passed = 0
    failed = 0
    print(f"\nPropagation Logic — Falsification Suite\n{'═'*44}")
    for name, fn in tests:
        try:
            fn()
            print(f"  ✓  {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗  {name}")
            print(f"       {e}")
            failed += 1
    print(f"{'─'*44}")
    print(f"  {passed} passed   {failed} failed\n")
    if failed:
        sys.exit(1)

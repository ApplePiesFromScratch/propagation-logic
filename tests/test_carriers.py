import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
from carrier_tool import CarrierSet, cmd_validate, CARRIERS_DIR

def test_all_carriers_validate():
    """Every carrier JSON in carriers/ must pass schema validation."""
    for p in sorted(CARRIERS_DIR.glob("*.json")):
        if p.stem.startswith("_"): continue
        result = cmd_validate(str(p))
        assert result, f"{p.name} failed validation"

def test_classical():
    cs = CarrierSet.preset("classical")
    assert cs.forces("LNC") == True
    assert cs.forces("LEM") == True
    assert cs.forces("ex_falso") == True
    assert cs.forces("leibniz") == False
    assert cs.forces("FTC") == False

def test_intuitionistic():
    cs = CarrierSet.preset("intuitionistic")
    assert cs.forces("LNC") == True    # carrier arithmetic unchanged
    assert cs.forces("LEM") == False   # Gor removed from Gamma

def test_paraconsistent():
    cs = CarrierSet.preset("paraconsistent_lp")
    assert cs.forces("LNC") == False
    assert cs.forces("ex_falso") == False
    # KEY: B and neg(B) = B in LP, not 0
    # The carrier extension is the point

def test_linear():
    cs = CarrierSet.preset("linear")
    assert cs.forces("resource_consumption") == True

def test_calculus():
    cs = CarrierSet.preset("calculus_differential")
    assert cs.forces("leibniz_product_rule") == True
    assert cs.forces("FTC") == True
    assert cs.forces("LNC") == False   # not applicable in continuous carrier

def test_probability():
    cs = CarrierSet.preset("probability")
    assert cs.forces("kolmogorov_normalization") == True
    assert cs.forces("LNC") == False   # not applicable

def test_modal_s4_vs_s5():
    s4 = CarrierSet.preset("modal_s4")
    s5 = CarrierSet.preset("modal_s5")
    assert s4.forces("5_axiom") == False
    assert s5.forces("5_axiom") == True

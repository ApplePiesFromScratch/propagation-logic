import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "carriers"
REQUIRED = ("name", "version", "V", "G", "theta", "forced_on_cut", "fails", "falsifier")


def test_schema_carriers_present():
    names = {p.stem for p in ROOT.glob("*.json") if not p.name.startswith("_")}
    assert names >= {"cl2", "l3", "k3", "proc"}


def test_each_carrier_has_required_fields():
    for p in ROOT.glob("*.json"):
        if p.name.startswith("_"):
            continue
        data = json.loads(p.read_text())
        for k in REQUIRED:
            assert k in data, f"{p.name} missing {k}"
        assert "Gamma" not in data
        assert "parameters" not in data
        assert data["fails"], f"{p.name} needs a failure"
        assert data["falsifier"]


def test_l3_and_k3_are_distinct_presentations():
    l3 = json.loads((ROOT / "l3.json").read_text())
    k3 = json.loads((ROOT / "k3.json").read_text())
    assert l3["V"] == k3["V"]
    assert l3["G"] != k3["G"]

#!/usr/bin/env python3
"""
carrier_tool.py  —  Propagation Logic Carrier Tool
P / G → Q

Usage:
    python carrier_tool.py classical
    python carrier_tool.py --diff classical intuitionistic
    python carrier_tool.py --compare classical paraconsistent_lp linear
    python carrier_tool.py --list
    python carrier_tool.py --validate carriers/my_logic.json
    python carrier_tool.py --learn

API:
    from carrier_tool import CarrierSet
    cs = CarrierSet.preset('classical')
    print(cs.forces('lnc'))   # True
"""

import json, sys, os
from pathlib import Path

CARRIERS_DIR = Path(__file__).parent.parent / "carriers"
LAW_ORDER = ["LNC","LEM","DNE","ex_falso","resource_consumption",
             "T_axiom","4_axiom","5_axiom","B_axiom",
             "graded_truth","kolmogorov_normalization",
             "kolmogorov_nonnegativity","kolmogorov_additivity",
             "shannon_entropy","leibniz_product_rule","chain_rule",
             "FTC","leibniz"]

class CarrierSet:
    def __init__(self, data: dict):
        self.data = data
        self.name     = data.get("name", "Unknown")
        self.V        = data["parameters"]["V"]
        self.Gamma    = data["parameters"]["Gamma"]
        self.theta    = data["parameters"]["theta"]
        self.laws     = data.get("forced_laws", {})
        self.failures = data.get("explicit_failures", [])

    @classmethod
    def preset(cls, name: str) -> 'CarrierSet':
        path = CARRIERS_DIR / f"{name}.json"
        if not path.exists():
            # Try with underscores
            path = CARRIERS_DIR / f"{name.replace('-','_').replace(' ','_').lower()}.json"
        if not path.exists():
            raise ValueError(f"Carrier '{name}' not found in {CARRIERS_DIR}")
        return cls(json.loads(path.read_text()))

    @classmethod
    def from_file(cls, path: str) -> 'CarrierSet':
        return cls(json.loads(Path(path).read_text()))

    def forces(self, law: str) -> bool | None:
        """Returns True if forced, False if not forced, None if not applicable."""
        k = law.upper()
        for key, val in self.laws.items():
            if key.upper() == k:
                if not isinstance(val, dict): return bool(val)
                return val.get("forced", False)
        return None

    def report(self):
        W = 60
        print(f"\n{'═'*W}")
        print(f"  {self.name}")
        print(f"{'─'*W}")
        print(f"  V     = {self.V}")
        print(f"  Γ     = {self.Gamma}")
        print(f"  θ     = {self.theta}")
        print(f"{'─'*W}")
        print(f"  {'Law':<30} {'Status':<12} Proof/Note")
        print(f"  {'─'*28} {'─'*10} {'─'*16}")
        for law, info in self.laws.items():
            if isinstance(info, dict):
                forced = info.get("forced", False)
                proof  = info.get("proof", info.get("note", ""))[:40]
            else:
                forced, proof = bool(info), ""
            status = "✓ forced" if forced else "✗ not forced"
            print(f"  {law:<30} {status:<12} {proof}")
        if self.failures:
            print(f"\n  Explicit failures:")
            for f in self.failures:
                print(f"    • {f}")
        print(f"{'═'*W}")

    def to_json(self) -> str:
        return json.dumps(self.data, indent=2)


def load_all() -> dict[str, CarrierSet]:
    cs = {}
    for p in sorted(CARRIERS_DIR.glob("*.json")):
        if p.stem.startswith("_"): continue
        try:
            cs[p.stem] = CarrierSet.from_file(str(p))
        except Exception as e:
            print(f"  Warning: could not load {p.name}: {e}")
    return cs


def cmd_diff(name1: str, name2: str):
    cs1 = CarrierSet.preset(name1)
    cs2 = CarrierSet.preset(name2)
    all_laws = set(cs1.laws.keys()) | set(cs2.laws.keys())
    print(f"\nDiff: {cs1.name}  →  {cs2.name}")
    print(f"{'─'*60}")
    changes = []
    same    = []
    for law in sorted(all_laws):
        f1 = cs1.forces(law)
        f2 = cs2.forces(law)
        if f1 != f2:
            s1 = "✓" if f1 else ("✗" if f1 is False else "—")
            s2 = "✓" if f2 else ("✗" if f2 is False else "—")
            changes.append(f"  {law:<30} {s1}  →  {s2}  CHANGED")
        else:
            s = "✓" if f1 else ("✗" if f1 is False else "—")
            same.append(f"  {law:<30} {s}  (unchanged)")
    for c in changes: print(c)
    if same:
        print(f"\n  Unchanged ({len(same)}):")
        for s in same: print(s)


def cmd_compare(*names: str):
    carriers = [CarrierSet.preset(n) for n in names]
    all_laws = set()
    for c in carriers: all_laws |= set(c.laws.keys())
    W = 20
    header = f"  {'Law':<28}" + "".join(f"{c.name[:W]:<{W+2}}" for c in carriers)
    print(f"\n{header}")
    print("  " + "─"*(28 + (W+2)*len(carriers)))
    for law in sorted(all_laws):
        row = f"  {law:<28}"
        for c in carriers:
            f = c.forces(law)
            s = "✓ forced" if f else ("✗ not" if f is False else "— n/a")
            row += f"{s:<{W+2}}"
        print(row)


def cmd_validate(path: str):
    try:
        cs = CarrierSet.from_file(path)
    except Exception as e:
        print(f"✗ Could not load {path}: {e}")
        return False
    errors = []
    if "parameters" not in cs.data:
        errors.append("Missing 'parameters'")
    else:
        for k in ["V","Gamma","theta"]:
            if k not in cs.data["parameters"]:
                errors.append(f"Missing parameters.{k}")
    if "forced_laws" not in cs.data or not cs.data["forced_laws"]:
        errors.append("No forced_laws defined")
    else:
        has_proof = any(
            isinstance(v,dict) and v.get("proof") and v.get("forced",False)
            for v in cs.data["forced_laws"].values()
        )
        if not has_proof:
            errors.append("At least one forced law must have a 'proof' field")
    if "explicit_failures" not in cs.data or not cs.data["explicit_failures"]:
        errors.append("explicit_failures required (at least one boundary)")
    if "falsification_test" not in cs.data:
        errors.append("falsification_test required")
    if errors:
        print(f"✗ {path}: validation failed")
        for e in errors: print(f"    • {e}")
        return False
    print(f"✓ {path}: valid ({cs.name}  V={cs.V}  Γ={cs.Gamma}  θ={cs.theta})")
    return True


LEARN_STEPS = [
    ("The Three Questions",
     "Every formal system is specified by three parameters:\n"
     "  V (value carrier): what values can a statement take?\n"
     "  Γ (gradient family): what operations are available?\n"
     "  θ (coherence threshold): when is a pattern stable?\n"
     "Change one. Watch the forced laws change."),
    ("Try it: classical vs intuitionistic",
     "python carrier_tool.py --diff classical intuitionistic\n"
     "Notice: LEM changes from forced to not forced.\n"
     "That is ONE parameter change: Γ = constructive (Gor removed).\n"
     "The carrier V={0,1} is identical. The arithmetic is identical.\n"
     "The law changes because the gradient is no longer available."),
    ("Try it: classical vs paraconsistent",
     "python carrier_tool.py --diff classical paraconsistent_lp\n"
     "Notice: LNC, LEM, and ex_falso all change.\n"
     "That is ONE parameter change: V = {0,B,1}.\n"
     "The B value ('both') means neg(B)=B and B-and-neg(B)=B.\n"
     "Contradiction is designated without explosion."),
    ("The calculus connection",
     "python carrier_tool.py calculus_differential\n"
     "Notice: Leibniz product rule and FTC are forced.\n"
     "LNC and LEM are not applicable (continuous carrier).\n"
     "Same mechanism. Different V. Logic and calculus are one system."),
    ("Build your own",
     "Copy carriers/_template.json to carriers/my_logic.json.\n"
     "Fill in V, Γ, θ.\n"
     "Derive the forced laws from the carrier arithmetic.\n"
     "State at least one explicit failure.\n"
     "Run: python carrier_tool.py --validate carriers/my_logic.json\n"
     "Submit a PR."),
]

def cmd_learn():
    print("\nPropagation Logic — Interactive Guide")
    print("Press Enter to continue, q to quit.\n")
    for i, (title, content) in enumerate(LEARN_STEPS, 1):
        print(f"{'─'*50}")
        print(f"Step {i}/{len(LEARN_STEPS)}: {title}")
        print(f"{'─'*50}")
        print(content)
        key = input("\n[Enter] next  [q] quit: ").strip().lower()
        if key == 'q': break
    print("\nDone. Run 'python carrier_tool.py classical' to see a full report.")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if '--learn' in args:
        cmd_learn()
    elif '--list' in args:
        cs_all = load_all()
        print(f"\nAvailable carriers ({len(cs_all)}):")
        for name, cs in cs_all.items():
            print(f"  {name:<35} V={cs.V}  Γ={cs.Gamma}  θ={cs.theta}")
    elif '--diff' in args:
        i = args.index('--diff')
        cmd_diff(args[i+1], args[i+2])
    elif '--compare' in args:
        i = args.index('--compare')
        cmd_compare(*args[i+1:])
    elif '--validate' in args:
        i = args.index('--validate')
        cmd_validate(args[i+1])
    elif '--export' in args:
        i = args.index('--export')
        cs = CarrierSet.preset(args[i+1])
        print(cs.to_json())
    else:
        # Named carrier report
        for name in args:
            try:
                CarrierSet.preset(name).report()
            except ValueError as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()

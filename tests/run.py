#!/usr/bin/env python3
"""
tests/run.py — the gate for /carriersets.
==========================================================================
Green means: every executable check passes, the data layer is
internally consistent (unique ids, every referenced check exists,
every claim has a check or a citation), the named findings are present,
library_verify exits 0, and the sealed manifest replays.
"""
import json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import carrierlib.checks                                    # noqa: F401
from carrierlib.core import CHECKS, run_claim, replay, PAID
from carriers import SECTIONS, ALL

failures = []


def gate(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" +
          (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


print("\n== 1. every executable check passes ==")
bad = []
for cname, fn in sorted(CHECKS.items()):
    try:
        ok, tier, ev = fn()
    except Exception as e:
        ok, ev = False, f"crash: {e}"
    if not ok:
        bad.append((cname, ev))
gate(f"all {len(CHECKS)} checks", not bad, str(bad[:2]) if bad else "")

print("\n== 2. data-layer integrity ==")
ids = [c["id"] for c in ALL]
gate("85 carriers in 9 sections",
     len(ALL) == 85 and len(SECTIONS) == 9,
     f"{len(ALL)} carriers, {len(SECTIONS)} sections")
gate("carrier ids unique", len(set(ids)) == len(ids))
keys = [c["key"] for c in ALL]
gate("carrier keys unique", len(set(keys)) == len(keys))

missing_checks, naked = [], []
for c in ALL:
    for kind in ("forces", "breaks"):
        for cl in c.get(kind, []):
            if cl.get("check"):
                if cl["check"] not in CHECKS:
                    missing_checks.append((c["key"], cl["check"]))
            elif not cl.get("cite"):
                naked.append((c["key"], cl["claim"][:40]))
gate("every referenced check exists in the registry",
     not missing_checks, str(missing_checks[:3]))
gate("every claim has a check or a citation", not naked,
     str(naked[:3]))
gate("required fields present on every record",
     all(all(k in c for k in ("id", "key", "name", "origin", "V", "G",
                              "theta", "insight", "forces", "breaks",
                              "useful_for")) for c in ALL))

print("\n== 3. the corrected-source findings are on record ==")
k3 = next(c for c in ALL if c["key"] == "K3")
r = run_claim(k3["forces"][0])
gate("K3 dual-reading finding (designation 14/15 vs value-reading "
     "failure)", r["ok"] and "both readings" in r["evidence"])
r2 = CHECKS["morphism_godel_threshold_corrected"]()
gate("Godel-threshold morphism corrected to the {AND,OR} fragment",
     r2[0] and "corrected" in r2[2])

print("\n== 4. tier accounting ==")
tiers = {}
for c in ALL:
    for kind in ("forces", "breaks"):
        for cl in c.get(kind, []):
            r = run_claim(cl)
            tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
paid = sum(v for k, v in tiers.items() if k in PAID)
total = sum(tiers.values())
gate("paid fraction is measured and > 50%", paid / total > 0.5,
     f"{paid}/{total} = {100 * paid / total:.1f}%  ({tiers})")
gate("OPEN tier used exactly for P vs NP", tiers.get("OPEN", 0) == 1)

print("\n== 5. library_verify.py end-to-end ==")
p = subprocess.run([sys.executable, str(ROOT / "library_verify.py")],
                   capture_output=True, text=True)
gate("exit code 0", p.returncode == 0)
gate("prints the paid fraction", "LIBRARY PAID FRACTION" in p.stdout)
man = json.loads((ROOT / "manifests" / "library_manifest.json")
                 .read_text())
gate("manifest chain replays intact", replay(man),
     f"{len(man)} seals")
gate("manifest verdict PASS/STIPULATED",
     man[-1]["verdict"] == "PASS/STIPULATED")

print("\n== 6. catalog renders ==")
p2 = subprocess.run([sys.executable,
                     str(ROOT / "tools" / "render_catalog.py")],
                    capture_output=True, text=True)
cat = (ROOT / "CATALOG.md")
gate("render_catalog exits 0 and writes CATALOG.md",
     p2.returncode == 0 and cat.exists())
if cat.exists():
    txt = cat.read_text()
    gate("catalog carries all 85 carriers",
         all(f"`{c['key']}`" in txt for c in ALL))

print()
if failures:
    print(f"GATE: RED — {failures}")
    sys.exit(1)
print(f"GATE: GREEN — {len(CHECKS)} checks, 85 carriers, "
      f"{paid}/{total} claims paid ({100 * paid / total:.1f}%), "
      "manifest sealed and replayed.")


# ── VACUITY CANARY ────────────────────────────────────────────────────
# A law engine must tell a carrier that passed from one that was never
# tested. A guarded law on a degenerate designated set holds over zero
# witnesses, and zero witnesses is not a pass.
try:
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    from pl_witness import distinguishes as _dist
    _V = (0.0, 0.5, 1.0)
    _neg = lambda a: 1.0 - a
    _ok, _why = _dist(_V, _neg, min, max, (1.0,), [(), _V])
    print(f"  vacuity canary: degenerate carriers distinguishable : "
          f"{'yes' if _ok else 'NO — ' + _why}")
    if not _ok:
        print("  BUILD FAILED — vacuity regression")
        raise SystemExit(1)
except ImportError:
    print("  vacuity canary: pl_witness not found")
    raise SystemExit(1)

#!/usr/bin/env python3
"""
library_verify.py — run the whole catalog against its own checks.
==========================================================================
The source PDF ends its mapping guide with: "Run library_verify.py to
see automated verification for all carriers in the library." This is
that file.

For every carrier, every Forces/Breaks claim either names an executable
check (run live, right now) or carries a citation and an honest tier
(PRESUMED / OPEN / STIPULATED). The library then prices ITSELF:

  paid fraction = claims decided here (FORCED/EMPIRICAL/CONDITIONAL)
                  over all claims

per carrier, per section, and overall — printed in the tables and
sealed into the manifest. A failing executable check fails the build:
the catalog is not allowed to disagree with its own enumerations.

Usage:
  python library_verify.py               # everything
  python library_verify.py --carrier K3  # one carrier, verbose
  python library_verify.py --section "Modal Logic"
"""
import argparse, collections, json, pathlib, sys, time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import carrierlib.checks                                    # noqa: F401
from carrierlib.core import run_claim, seal, replay, PAID
from carriers import SECTIONS


def verify_carrier(c):
    results = []
    for kind in ("forces", "breaks"):
        for claim in c.get(kind, []):
            r = run_claim(claim)
            r["kind"] = kind
            results.append(r)
    n = len(results)
    paid = sum(1 for r in results if r["tier"] in PAID and r["ok"])
    failed = [r for r in results if r["ok"] is False]
    return results, paid, n, failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carrier", help="verify a single carrier by key")
    ap.add_argument("--section", help="verify a single section")
    a = ap.parse_args()

    t0 = time.time()
    chain = []
    total_paid = total_claims = total_checks = 0
    any_fail = []
    print("\n  PROPAGATION LOGIC — CARRIER LIBRARY VERIFICATION")
    print("  P/G->Q is constant; V, G, theta vary; every claim priced.")

    for section, carriers in SECTIONS:
        if a.section and section != a.section:
            continue
        rows = []
        s_paid = s_claims = 0
        for c in carriers:
            if a.carrier and c["key"] != a.carrier:
                continue
            results, paid, n, failed = verify_carrier(c)
            checked = sum(1 for r in results if r["check"])
            s_paid += paid
            s_claims += n
            total_checks += checked
            any_fail += [(c["key"], r) for r in failed]
            tiers = collections.Counter(r["tier"] for r in results
                                        if r["ok"] or r["ok"] is None)
            rows.append((c, results, paid, n, tiers, failed))
            seal({"carrier": c["key"], "claims": n, "paid": paid,
                  "failed": len(failed)}, chain)
        if not rows:
            continue
        total_paid += s_paid
        total_claims += s_claims
        frac = 100 * s_paid / s_claims if s_claims else 0
        print(f"\n  == {section}  "
              f"[{len(rows)} carriers, paid {s_paid}/{s_claims} "
              f"claims = {frac:.0f}%] " + "=" * max(1, 40 - len(section)))
        for c, results, paid, n, tiers, failed in rows:
            mark = "FAIL" if failed else "ok"
            tstr = " ".join(f"{t[:4]}:{k}" for t, k in sorted(
                tiers.items(), key=lambda x: -x[1]))
            print(f"  [{mark:>4}] {c['id']:>2} {c['name'][:44]:<44} "
                  f"paid {paid}/{n}  {tstr}")
            if a.carrier or failed:
                for r in results:
                    flag = ("PASS" if r["ok"] else
                            "FAIL" if r["ok"] is False else "cite")
                    print(f"          [{flag}][{r['tier'][:4]}] "
                          f"({r['kind']}) {r['claim'][:70]}")
                    print(f"                -> {r['evidence'][:100]}")

    frac = 100 * total_paid / total_claims if total_claims else 0
    body = {"carriers": sum(len(cs_) for _, cs_ in SECTIONS),
            "claims": total_claims, "paid": total_paid,
            "paid_fraction": round(frac, 1),
            "executable_checks_run": total_checks,
            "verdict": ("PASS" if not any_fail else "FAIL")
                       + "/STIPULATED",
            "non_claims": [
                "NOT claimed: that PRESUMED entries are false or even "
                "doubtful — only that this library did not re-derive "
                "them, and prices itself accordingly.",
                "NOT claimed: that a carrier's insight prose is itself "
                "verified — the checks decide the Forces/Breaks tables; "
                "the prose is commentary.",
                "NOT claimed: completeness — 85 carriers is a library, "
                "not the space of all formal systems."]}
    seal(body, chain)
    # THE HISTORY HEARING (before the writer speaks): the committed
    # manifest must replay by seal arithmetic alone — regenerate-then-
    # compare validates the writer, not the history (the Atlas's
    # first-day finding about this repo, closed here).
    out = pathlib.Path(__file__).parent / "manifests"
    mp = out / "library_manifest.json"
    if mp.exists():
        try:
            prior = json.loads(mp.read_text())
        except Exception:
            prior = None
        if not (isinstance(prior, list) and replay(prior)):
            print("\n  HISTORY: committed manifest does NOT replay — "
                  "possible tampering;")
            print("  file preserved as evidence; refusing to "
                  "regenerate over it.")
            any_fail = True
        else:
            print(f"\n  history: committed manifest replays "
                  f"({len(prior)} seals) — proceeding")
            new = json.dumps(chain, indent=1)
            if mp.read_text() != new:
                mp.write_text(new)
    else:
        out.mkdir(exist_ok=True)
        mp.write_text(json.dumps(chain, indent=1))

    print("\n  " + "=" * 68)
    print(f"  LIBRARY PAID FRACTION: {total_paid}/{total_claims} claims "
          f"machine-decided here = {frac:.1f}%")
    print(f"  the remainder is PRESUMED with citations, STIPULATED "
          f"declarations, or OPEN")
    print(f"  verdict {body['verdict']}   chain {len(chain)} sealed, "
          f"replay={'intact' if replay(chain) else 'BROKEN'}   "
          f"{time.time() - t0:.1f}s")
    if any_fail:
        print("  FAILURES:")
        for key, r in any_fail:
            print(f"    {key}: {r['claim'][:60]} -> {r['evidence'][:80]}")
    for nc in body["non_claims"]:
        print(f"  {nc}")
    print()
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()

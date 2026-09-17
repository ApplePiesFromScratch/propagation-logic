#!/usr/bin/env python3
"""Render CATALOG.md from the carrier records — the whole library as
markdown, with each claim's live verification status inlined. Run after
library_verify.py; regenerating is the only way to edit CATALOG.md."""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import carrierlib.checks                                    # noqa: F401
from carrierlib.core import run_claim, PAID
from carriers import SECTIONS


def claim_line(claim):
    r = run_claim(claim)
    if r["check"]:
        badge = f"**{r['tier']}**" if r["ok"] else "**FAILED**"
        return (f"- {badge} `{r['check']}` — {r['claim']}\n"
                f"  - *{r['evidence']}*")
    return f"- *{r['tier']}* — {r['claim']}  ({r['evidence']})"


def main():
    out = ["# Carrier Library — Catalog",
           "",
           "*Rendered from `carriers/` by `tools/render_catalog.py`. "
           "Every **FORCED/EMPIRICAL/CONDITIONAL** badge below was "
           "earned by an executable check at render time; every "
           "*PRESUMED/OPEN/STIPULATED* line says so and cites. "
           "`P/G→Q` is constant; only V, G, θ vary.*", ""]
    total = paid = 0
    for section, carriers in SECTIONS:
        out.append(f"\n## {section} — {len(carriers)} carriers\n")
        for c in carriers:
            out.append(f"### {c['id']:02d} · {c['name']} (`{c['key']}`)")
            out.append(f"*{c['origin']}*\n")
            out.append(f"| | |\n|---|---|")
            out.append(f"| **V** | {c['V']} |")
            out.append(f"| **G** | {c['G']} |")
            out.append(f"| **θ** | {c['theta']} |")
            out.append(f"\n{c['insight']}\n")
            out.append("**Forces**")
            for cl in c["forces"]:
                out.append(claim_line(cl))
                r = run_claim(cl)
                total += 1
                paid += r["tier"] in PAID and bool(r["ok"])
            out.append("\n**Breaks on**")
            for cl in c["breaks"]:
                out.append(claim_line(cl))
                r = run_claim(cl)
                total += 1
                paid += r["tier"] in PAID and bool(r["ok"])
            out.append("\n**Useful for:** " + " · ".join(c["useful_for"]))
            out.append("")
    out.insert(4, f"**{sum(len(cs_) for _, cs_ in SECTIONS)} carriers · "
                  f"{total} claims · {paid} machine-decided "
                  f"({100 * paid / total:.1f}% paid fraction)**")
    (ROOT / "CATALOG.md").write_text("\n".join(out))
    print(f"CATALOG.md written: {total} claims, {paid} paid "
          f"({100 * paid / total:.1f}%)")


if __name__ == "__main__":
    main()

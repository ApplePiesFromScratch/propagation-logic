#!/usr/bin/env python3
"""ATLAS.md — a map of maps. Generated. Not terrain."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import carrierlib.checks  # noqa: F401
from carrierlib.core import PAID, run_claim
from carriers import SECTIONS


def main():
    lines = [
        "# Atlas",
        "",
        "A map of maps. V, G, theta, what sits outside, what breaks.",
        "Nouns are labels. Paid badges were earned at render time.",
        "",
    ]
    total = paid = 0
    for section, carriers in SECTIONS:
        lines.append(f"## {section}")
        lines.append("")
        lines.append("| key | V | G | theta | outside | paid |")
        lines.append("|---|---|---|---|---|---|")
        for c in carriers:
            n = 0
            p = 0
            for kind in ("forces", "breaks"):
                for cl in c.get(kind, []):
                    r = run_claim(cl)
                    n += 1
                    if r["tier"] in PAID and r["ok"]:
                        p += 1
            total += n
            paid += p
            outside = c.get("outside", "")
            lines.append(
                f"| `{c['key']}` | {c.get('V','')} | {c.get('G','')} | "
                f"{c.get('theta','')} | {outside} | {p}/{n} |"
            )
        lines.append("")
    lines.insert(4, f"**{sum(len(cs) for _, cs in SECTIONS)} carriers · "
                 f"{total} claims · {paid} paid "
                 f"({100 * paid / total:.1f}%)**")
    lines.insert(5, "")
    (ROOT / "ATLAS.md").write_text("\n".join(lines))
    print(f"ATLAS.md written: {total} claims, {paid} paid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

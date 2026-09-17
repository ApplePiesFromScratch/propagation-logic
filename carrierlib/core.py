"""
carrierlib.core — the engine under the catalog.
==========================================================================
Every carrier in this library is a data record; every Forces/Breaks claim
in a record either names an EXECUTABLE CHECK (registered here, run by
library_verify.py on every build) or carries a citation and the honest
tag for an unexecuted claim. The ladder:

  FORCED       decided here, by complete enumeration or exact symbolic
               computation on the artifact itself
  EMPIRICAL    measured here (Monte Carlo, simulation), with the
               tolerance stated
  CONDITIONAL  verified here on a bounded instance / under a stated
               assumption (the bound or assumption is in the evidence)
  STIPULATED   a convention this library declares (e.g. finite-trace
               semantics for LTL)
  PRESUMED     inherited from the literature with a citation; NOT
               re-derived here. Priced at zero in the library's own
               paid fraction — honestly.
  OPEN         a famous open problem. Nobody gets to verify it.

The library's headline number is its PAID FRACTION: what share of its
claims are FORCED/EMPIRICAL/CONDITIONAL here, per carrier and overall.
A catalog that verified nothing would be a bibliography; this one knows
exactly how much of itself is bibliography.
"""
from __future__ import annotations
import hashlib, json, traceback

TIERS = ("FORCED", "EMPIRICAL", "CONDITIONAL", "STIPULATED",
         "PRESUMED", "OPEN", "UNPAID")
PAID = ("FORCED", "EMPIRICAL", "CONDITIONAL")

CHECKS = {}


def check(name):
    """Register an executable check. A check returns (ok, tier, evidence):
    ok is the verdict, tier is what kind of evidence the check itself
    constitutes, evidence is one line a reader can act on (a witness, a
    bound, a measured number)."""
    def deco(fn):
        if name in CHECKS:
            raise KeyError(f"duplicate check id: {name}")
        CHECKS[name] = fn
        return fn
    return deco


def run_claim(claim):
    """Run one claim dict -> result dict. Never raises: a crashing check
    is a failing check with the traceback as evidence."""
    cid = claim.get("check")
    if cid is None:
        tier = claim.get("tier", "PRESUMED")
        ev = claim.get("cite", "no citation given")
        return {"claim": claim["claim"], "check": None, "ok": None,
                "tier": tier, "evidence": ev}
    fn = CHECKS.get(cid)
    if fn is None:
        return {"claim": claim["claim"], "check": cid, "ok": False,
                "tier": "UNPAID", "evidence": f"check {cid!r} not found"}
    try:
        ok, tier, ev = fn()
    except Exception as e:
        ok, tier = False, "UNPAID"
        ev = f"check crashed: {type(e).__name__}: {e}"
    return {"claim": claim["claim"], "check": cid, "ok": bool(ok),
            "tier": tier, "evidence": str(ev)[:200]}


def seal(body, chain):
    prev = chain[-1]["sha"] if chain else "GENESIS"
    sha = hashlib.sha256((prev + json.dumps(body, sort_keys=True))
                         .encode()).hexdigest()[:16]
    chain.append({**body, "sha_prev": prev, "sha": sha})
    return chain[-1]


def replay(chain):
    prev = "GENESIS"
    for g in chain:
        body = {k: v for k, v in g.items() if k not in ("sha", "sha_prev")}
        want = hashlib.sha256((prev + json.dumps(body, sort_keys=True))
                              .encode()).hexdigest()[:16]
        if g["sha_prev"] != prev or g["sha"] != want:
            return False
        prev = g["sha"]
    return True

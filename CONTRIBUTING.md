# Contributing a Carrier

New carriers are welcome. The bar is the six-step mapping guide
(`docs/MAPPING_GUIDE.md`), and the gate enforces the parts a gate can
enforce.

## The admission checklist

1. **Walk the six steps.** Identify V, G, θ; derive forced laws;
   exhibit failures; locate morphisms.
2. **Steps 4 and 5 must be executable** wherever V is finite, the
   identity is symbolic, or the quantity is measurable:
   - finite V → complete enumeration (`carrierlib.finite.laws`,
     `modal_forced`, or your own exhaustive sweep) → **FORCED**
   - symbolic identity → sympy, exact → **FORCED**
   - measurable claim → simulation with tolerances derived from the
     measured spread, seeds fixed → **EMPIRICAL**
   - bounded instance / stated assumption → **CONDITIONAL**, with the
     bound in the evidence string
3. **Everything else gets a citation and a tier.** `PRESUMED` for
   inherited theorems, `STIPULATED` for conventions the record itself
   declares, `OPEN` for the genuinely open. A claim with neither a
   check nor a cite fails the gate.
4. **Write the record** in the right `carriers/<section>.py`: unique
   `id` and `key`, `origin`, `V`, `G`, `theta`, a short `insight`
   (commentary — the checks carry the weight), `forces`, `breaks`,
   `useful_for`.
5. **Register your checks** in a `carrierlib/checks/` module with the
   `@check("name")` decorator. A check returns
   `(ok, tier, one_line_evidence)`. Crashing counts as failing.
6. **Run the gate**: `python tests/run.py`. It verifies your check
   exists, your claims are covered, all 92+ checks pass,
   `library_verify.py` exits 0, and the manifest replays.
7. **Regenerate the catalog**: `python tools/render_catalog.py`.
   `CATALOG.md` is generated — never edit it by hand.

## House rules

- **The enumerator outranks the literature.** If your check contradicts
  a source (including this library's own source PDFs), the check wins
  and the record documents the correction. Two precedents already in
  the tree: K3's dual-reading LNC and the Gödel-threshold morphism.
- **Tolerances are earned, not chosen.** EMPIRICAL bounds come from
  measured spread (e.g. 4 standard errors), with fixed seeds.
- **The paid fraction only goes down if you let it.** Citation-heavy
  carriers are welcome (Reverse Mathematics sits at 0/2 paid, honestly)
  — but if a claim CAN be decided in finite time, decide it.
- Keep checks fast: the whole suite runs in ~2 seconds and should stay
  under ten.

# Contributing

A new carrier is a presentation. It enters `carriers/` only if:

1. JSON matches `_schema.json` (`V`, `G`, `theta`, not `Gamma`).
2. `forced_on_cut` names a listed alphabet and a falsifier.
3. `fails` has at least one line.
4. A pytest exists that can fail.

A new operator follows `docs/OPERATOR_GUIDE.md`:
close-test, θ-test, coincidence-test on a grown V.

A new cost is a ledger kind with a stipulated price.
Zero-cost work is an accounting failure.

Do not add a claim that cannot name V, G, and θ.
Do not lift FORCED-on-cut off the cut in the same sentence.

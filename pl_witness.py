"""
pl_witness — witness counting for law engines.

A law is checked over a range of cases. Laws quantified over the VALUE
SPACE always have len(V) witnesses. Laws quantified, directly or through a
guard, over the DESIGNATED SET have as many as that set admits — and a
designated set that is empty or exhaustive renders those guards inert, so
the law returns a verdict without having been tested.

    witnesses = the number of cases in which the law could have failed

Zero witnesses is coverage zero, which the tier rule grades UNPAID. A law
that was never tested does not read as one that passed.

GUARDED holds the laws whose witness count depends on the designated set.
`distinguishes` is the regression: sound carriers must report zero UNPAID
laws, degenerate ones at least one.

No carrier is refused. Pricing restores the discrimination; a gate built
from how classical logic behaves would refuse real logics.
"""
GUARDED = {"LNC", "LEM", "NoGlut", "MP", "MT"}


def witnesses(V, NEG, AND, OR, D):
    """Cases in which each guarded law could have failed."""
    Ds, n = set(D), len(V)
    disc = bool(Ds) and Ds != set(V)
    return {
        "LNC":    n if Ds else 0,
        "LEM":    n if disc else 0,
        "NoGlut": sum(1 for a in V if a in Ds),
        "MP":     sum(1 for a in V for b in V
                      if a in Ds and OR(NEG(a), b) in Ds),
        "DN":     n,
    }


def grade(verdict, w):
    """Zero witnesses is never a pass."""
    return "UNPAID" if w == 0 else ("FORCED-on-cut" if verdict else "REFUTED")


def unpaid_count(laws, wits):
    """How many laws passed without being tested."""
    return sum(1 for k, v in laws.items()
               if k in wits and grade(v, wits[k]) == "UNPAID")


def distinguishes(V, NEG, AND, OR, sound_D, degenerate_Ds):
    """The canary. A sound carrier must report zero UNPAID; every
    degenerate one must report at least one."""
    def laws(D):
        Ds = set(D)
        return {
            "LNC": all(AND(a, NEG(a)) not in Ds for a in V),
            "LEM": all(OR(a, NEG(a)) in Ds for a in V),
            "NoGlut": not any(a in Ds and NEG(a) in Ds for a in V),
            "MP": all(not (a in Ds and OR(NEG(a), b) in Ds) or b in Ds
                      for a in V for b in V),
            "DN": all(NEG(NEG(a)) == a for a in V),
        }
    if unpaid_count(laws(sound_D), witnesses(V, NEG, AND, OR, sound_D)) != 0:
        return False, "a sound carrier reports UNPAID laws"
    for D in degenerate_Ds:
        if unpaid_count(laws(D), witnesses(V, NEG, AND, OR, D)) == 0:
            return False, f"degenerate carrier D={D or 'empty'} reports none"
    return True, ""

"""
pl/core.py — Propagation Logic: core mechanism

Implements the single primitive of PL:

    P / G → Q

A loaded pattern P = (v_P, L_P) propagates through a gradient field G
in context C, producing output pattern Q. The context supplies the
coherence threshold θ_C against which gradient demand is measured.

All logical connectives, inference rules, and meta-logical properties
in the paper are instances of these definitions.

Reference: Pugmire, J. "Propagation Logic: A Single-Operator Foundation
for Logic and Calculus." Version 12, 2026.
"""

from dataclasses import dataclass


# ── Core structures ────────────────────────────────────────────────────────────

@dataclass
class Pattern:
    """
    A loaded pattern P = (val, load).

    val  : designation component. Over the two-element carrier V = {0,1},
           val=1 means designated, val=0 means undesignated.
    load : informational load L_P = |H_P| >= 0. The scalar magnitude of
           the accumulated propagation history.

    Definition 2.1 (paper §2.1).
    """
    val: int
    load: float

    def __post_init__(self):
        if self.load < 0:
            raise ValueError(f"Load must be non-negative, got {self.load}")


@dataclass
class Context:
    """
    A propagation context C = (Γ_C, o_C, θ_C).

    threshold : coherence threshold θ_C. A pattern is coherent in C
                iff its load does not exceed this threshold.

    Definition 2.2 (paper §2.2).
    """
    threshold: float

    def support(self, p: Pattern) -> float:
        """support(P, C) = min(L_P, θ_C)"""
        return min(p.load, self.threshold)

    def demand(self, p: Pattern) -> float:
        """demand(P, C) = max(0, L_P - θ_C) — reconfiguration pressure."""
        return max(0.0, p.load - self.threshold)

    def rate(self, p: Pattern) -> float:
        """
        rate(P, C) = support(P, C) / L_P  for L_P > 0, else 1.
        Simpler patterns (lower load) propagate faster. Theorem 2.1.
        """
        if p.load == 0:
            return 1.0
        return self.support(p) / p.load

    def designated(self, p: Pattern) -> bool:
        """v_P = 1"""
        return p.val == 1

    def coherent(self, p: Pattern) -> bool:
        """L_P <= θ_C"""
        return p.load <= self.threshold

    def valid(self, p: Pattern) -> bool:
        """designated AND coherent — Definition 2.2."""
        return self.designated(p) and self.coherent(p)


# ── Gradient fields (logical connectives) ─────────────────────────────────────
#
# Each gradient field specifies two rules independently:
#   value rule  — how v_P transforms
#   load rule   — how L_P transforms (the propagation cost)
#
# Definitions 3.1–3.5, paper §3.

def G_id(p: Pattern) -> Pattern:
    """
    Identity gradient. Zero-cost baseline.
    G_id(v, L) = (v, L).
    P /C G_id = P for any P. Theorem 4.1.
    """
    return Pattern(p.val, p.load)


def G_neg(p: Pattern) -> Pattern:
    """
    Negation gradient.
    G_neg(v, L) = (1 - v, L).
    Flips designation; preserves load. Double negation: G_neg(G_neg(P)) = P.
    Definition 3.1.
    """
    return Pattern(1 - p.val, p.load)


def G_and(p: Pattern, q: Pattern) -> Pattern:
    """
    Conjunction gradient.
    G_and(P, Q) = (v_P * v_Q, L_P + L_Q).
    Designated iff both inputs are designated. Load is additive.
    Definition 3.2.
    """
    return Pattern(p.val * q.val, p.load + q.load)


def G_or(p: Pattern, q: Pattern) -> Pattern:
    """
    Disjunction gradient.
    G_or(P, Q) = (max(v_P, v_Q), min(L_P, L_Q)).
    Designated iff at least one input is designated.
    Propagates along the path of least gradient demand. Definition 3.3.
    """
    return Pattern(max(p.val, q.val), min(p.load, q.load))


def G_imp(p: Pattern, q: Pattern) -> Pattern:
    """
    Implication gradient. Activation is value-based, not load-based.
    G_imp(P, Q) = Q         if v_P = 1  (forcing case)
               = (1, 0)     if v_P = 0  (vacuous case)
    Definition 3.4.
    """
    if p.val == 1:
        return q
    return Pattern(1, 0.0)


def propagate(p: Pattern, G, *args) -> Pattern:
    """
    Apply gradient field G to pattern P: P /C G -> Q.
    Additional arguments (e.g. a second pattern for binary fields)
    are forwarded to G.
    """
    return G(p, *args)

"""
pl/drag.py — Nonzero-Drag Regimes: Linear and Relevance Logic
Part of Propagation Logic / Mathesis Universalis

Drag regimes are STATE CONSTRAINTS on gradient propagation,
not continuous load formulas. This is the key correction over
formulations using |L_P - L_Q| terms.

The ExtendedPattern adds two fields to the base Pattern:
  available    : resource state (False = consumed, linear logic)
  history_tags : gradient path record (relevance connectivity)

These can be used standalone or alongside pl/core.py's Pattern.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import FrozenSet, Any


# ── Exceptions ─────────────────────────────────────────────────────────────

class LinearLogicViolation(Exception):
    """
    Raised when a consumed pattern is used a second time.
    Demand = infinity. The gradient family boundary condition
    forbids re-use. This is a structural violation, not a bug.
    """
    pass


class RelevanceLogicViolation(Exception):
    """
    Raised when premises share no gradient path.
    Demand = infinity. Relevance logic requires that connected
    patterns (sharing at least one gradient ancestor) co-propagate.
    Disconnected premises: demand exceeds any finite threshold.
    """
    pass


# ── Extended Pattern ────────────────────────────────────────────────────────

@dataclass
class ExtendedPattern:
    """
    P = (val, load) with drag regime extensions.

    val          : designation component
    load         : informational load L_P >= 0
    available    : resource state — False means consumed (linear logic)
    history_tags : gradient path record (relevance connectivity)

    Use alongside pl/core.py's Pattern, or standalone.
    """
    val:          Any
    load:         float
    available:    bool            = True
    history_tags: FrozenSet[str]  = field(default_factory=frozenset)

    def __post_init__(self):
        if self.load < 0:
            raise ValueError(f"Load must be >= 0, got {self.load}")

    def designated(self) -> bool:
        return self.val == 1 or self.val is True

    # ── Linear logic ──────────────────────────────────────────────────────

    def consume(self) -> ExtendedPattern:
        """
        Linear logic: mark gradient capacity as spent.
        The pattern retains its val and load; available -> False.
        Further co-propagation raises LinearLogicViolation.

        This is a state change, not a load formula.
        """
        if not self.available:
            raise LinearLogicViolation(
                f"Pattern already consumed (linear logic: each resource used once). "
                f"val={self.val}, load={self.load}"
            )
        return ExtendedPattern(self.val, self.load, False, self.history_tags)

    # ── Relevance logic ───────────────────────────────────────────────────

    def with_gradient_step(self, step_tag: str) -> ExtendedPattern:
        """Record one gradient application in the propagation history."""
        return ExtendedPattern(
            self.val, self.load,
            self.available,
            self.history_tags | frozenset([step_tag])
        )

    def connected_to(self, other: ExtendedPattern) -> bool:
        """
        Relevance connectivity: non-empty intersection of history_tags.

        Erlangen insight: shared gradient ancestry = shared identity frame.
        Patterns with no history are seeds — they share no ancestry.

        This IS the variable-sharing criterion of relevance logic,
        stated structurally rather than syntactically.
        """
        if not self.history_tags or not other.history_tags:
            return False
        return bool(self.history_tags & other.history_tags)

    def __repr__(self):
        s = " [consumed]" if not self.available else ""
        return f"ExtendedPattern(v={self.val}, L={self.load:.4g}){s}"


# ── Context with drag regimes ───────────────────────────────────────────────

@dataclass
class DragContext:
    """
    Context C = (threshold, drag_regime).

    drag_regime options:
      'zero'      : classical logic, calculus  — L_P + L_Q
      'linear'    : linear logic               — consumption state check
      'relevance' : relevance logic            — connectivity check
    """
    threshold:   float = 1.0
    drag_regime: str   = 'zero'

    def support(self, p: ExtendedPattern) -> float:
        return min(p.load, self.threshold)

    def demand(self, p: ExtendedPattern) -> float:
        return max(0.0, p.load - self.threshold)

    def coherent(self, p: ExtendedPattern) -> bool:
        return p.load <= self.threshold

    def combined_load(self, p: ExtendedPattern, q: ExtendedPattern) -> float:
        """
        Load combination for co-propagation of P and Q.

        Takes PATTERN OBJECTS, not scalars — the regime-specific
        constraint checks pattern STATE, not load magnitudes.

        Zero-drag:   additive (classical)
        Linear:      consumes both patterns; raises if either consumed
        Relevance:   raises if no shared gradient path
        """
        if self.drag_regime == 'zero':
            return p.load + q.load

        elif self.drag_regime == 'linear':
            # State check — raises LinearLogicViolation if either is consumed
            p.consume()
            q.consume()
            return p.load + q.load

        elif self.drag_regime == 'relevance':
            if not p.connected_to(q):
                raise RelevanceLogicViolation(
                    f"No shared gradient path: "
                    f"history(P)={set(p.history_tags)} ∩ history(Q)={set(q.history_tags)} = ∅. "
                    "Relevance logic requires shared gradient ancestry."
                )
            return p.load + q.load

        else:
            raise ValueError(f"Unknown drag regime: {self.drag_regime!r}")


# ── Gradient fields with drag support ──────────────────────────────────────

def G_neg_ext(p: ExtendedPattern) -> ExtendedPattern:
    """Negation: flips val, preserves load. History: records 'neg'."""
    return ExtendedPattern(
        1 - int(p.val), p.load,
        p.available,
        p.history_tags | frozenset(['neg'])
    )


def G_and_ext(p: ExtendedPattern, q: ExtendedPattern,
              ctx: DragContext = None) -> ExtendedPattern:
    """Conjunction with drag regime support."""
    ctx = ctx or DragContext()
    new_load = ctx.combined_load(p, q)
    return ExtendedPattern(
        int(p.val) * int(q.val),
        new_load,
        history_tags=p.history_tags | q.history_tags | frozenset(['and'])
    )


def G_or_ext(p: ExtendedPattern, q: ExtendedPattern) -> ExtendedPattern:
    """Disjunction: max val, min load (easiest path)."""
    return ExtendedPattern(
        max(int(p.val), int(q.val)),
        min(p.load, q.load),
        history_tags=p.history_tags | q.history_tags | frozenset(['or'])
    )


def G_imp_ext(p: ExtendedPattern, q: ExtendedPattern,
              ctx: DragContext = None) -> ExtendedPattern:
    """
    Implication with relevance check.
    Forcing case (v_P=1): output is Q.
    Vacuous case (v_P=0): designated, zero-load.
    """
    ctx = ctx or DragContext()
    if int(p.val) == 1:
        if ctx.drag_regime == 'relevance' and not p.connected_to(q):
            raise RelevanceLogicViolation(
                "Implication cannot fire: premises share no gradient path."
            )
        return ExtendedPattern(
            int(q.val), q.load,
            history_tags=p.history_tags | q.history_tags | frozenset(['imp'])
        )
    return ExtendedPattern(1, 0.0, history_tags=frozenset(['imp_vac']))

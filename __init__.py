"""
pl — Propagation Logic

A single-operator foundation for logic and calculus.

    from pl.core import Pattern, Context, G_neg, G_and, G_or, G_imp, G_id
    from pl.calculus import CalcPattern, integrate, newton_reconfigure

Reference: Pugmire, J. "Propagation Logic: A Single-Operator Foundation
for Logic and Calculus." Version 12, 2026.
"""

from pl.core import (
    Pattern,
    Context,
    G_id,
    G_neg,
    G_and,
    G_or,
    G_imp,
    propagate,
)

from pl.calculus import (
    CalcPattern,
    integrate,
    newton_reconfigure,
)

__all__ = [
    "Pattern", "Context",
    "G_id", "G_neg", "G_and", "G_or", "G_imp", "propagate",
    "CalcPattern", "integrate", "newton_reconfigure",
]

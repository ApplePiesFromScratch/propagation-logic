"""
pl/dras.py — DRAS Calculus v5
De-Reification Axiom Standard — Built on Propagation Logic

Every quantity is a loaded history: a pattern P = (val, load) propagating
through a gradient field that depends on the energy scale E.

The running coupling formula:
    q(E) = q₀ / (1 + β·ln(E/E₀))

    β > 0: coupling weakens at high E (asymptotic freedom — QCD-like)
    β < 0: coupling grows at high E toward Landau pole (QED-like)
    β = 0: scale-invariant (no running — fixed point of the RG flow)

Arithmetic propagates (val, load, β, E₀) through all operations consistently
with the renormalisation group: β adds under multiplication, averages weighted
by value under addition.
"""

import math


class LoadedHistory:
    """
    A quantity in DRAS: not a number but a propagation history.

    val   : current value at reference scale E₀
    load  : propagating gradient (derivative w.r.t. whatever x you seeded)
    beta  : running coupling coefficient (RG β-function, dimensionless)
    E0    : reference energy scale at which val is defined
    theta : coherence threshold — maximum load before reconfiguration
    """

    def __init__(self,
                 val:   float,
                 load:  float = 0.0,
                 beta:  float = 0.0,
                 E0:    float = 1.0,
                 theta: float = 1e12):
        self.val   = float(val)
        self.load  = float(load)
        self.beta  = float(beta)
        self.E0    = float(E0)
        self.theta = float(theta)

    # ── Scale running ────────────────────────────────────────────────────────

    def at_scale(self, E: float) -> 'LoadedHistory':
        """
        Run the quantity from E₀ to scale E via the RG formula.

        q(E) = q₀ / (1 + β·ln(E/E₀))

        The gradient (load) scales by the same factor — it's the derivative
        of q(x, E) w.r.t. x, and that derivative scales with q uniformly
        in the linear approximation.

        We do NOT add a ∂q/∂E term here. That would be the derivative w.r.t.
        the energy scale itself — a completely different object (the beta
        function equation), not the propagating gradient w.r.t. x.
        """
        if E <= 0 or self.E0 <= 0 or abs(self.beta) < 1e-14:
            return LoadedHistory(self.val, self.load, self.beta, E, self.theta)

        t          = math.log(E / self.E0)
        denom      = 1.0 + self.beta * t

        if abs(denom) < 1e-10:
            # Landau pole — RG equation breaks down, pattern cannot cohere here
            raise LandauPole(
                f"Landau pole at E={E:.3g}: denominator → 0 "
                f"(β={self.beta:.3f}, E₀={self.E0:.3g}). "
                "The gradient family has no coherent extension to this scale."
            )

        new_val  = self.val  / denom
        new_load = self.load / denom   # gradient scales uniformly with the quantity

        return LoadedHistory(new_val, new_load, self.beta, E, self.theta)

    def loading_direction(self) -> str:
        if abs(self.beta) < 1e-8:
            return "scale-invariant (fixed point)"
        return "asymptotic freedom (QCD-like)" if self.beta > 0 else "Landau pole in UV (QED-like)"

    # ── Coherence check and reconfiguration ─────────────────────────────────

    def _reconfigure_if_needed(self) -> 'LoadedHistory':
        """
        Observation 2.2: when load exceeds the coherence threshold,
        the pattern cannot cohere in this context.

        Rather than silently overflowing or just warning, we raise
        CoherenceExceeded. The caller decides whether to catch and handle
        (e.g. by widening the context θ) or let it propagate.

        This is the correct PL behaviour: demand > θ_C means this gradient
        family cannot contain the pattern. It should not silently continue.
        """
        demand = abs(self.load) - self.theta
        if demand > 0:
            raise CoherenceExceeded(
                f"Load |{self.load:.3e}| exceeds coherence threshold {self.theta:.3e} "
                f"(demand = {demand:.3e}). Pattern requires a larger context "
                f"or a different gradient family."
            )
        return self

    # ── Arithmetic — propagates (val, load, β, E₀) correctly ───────────────

    def __neg__(self) -> 'LoadedHistory':
        return LoadedHistory(-self.val, -self.load, self.beta, self.E0, self.theta)

    def __add__(self, other) -> 'LoadedHistory':
        other = _coerce(other, self)

        new_val  = self.val  + other.val
        new_load = self.load + other.load   # histories add (zero-drag regime)

        # β under addition: weighted average by magnitude of each term's value.
        # Physical rationale: the beta function of a sum is dominated by the
        # larger term. If |a| >> |b|, the sum runs like a alone.
        total = abs(self.val) + abs(other.val)
        if total < 1e-14:
            new_beta = 0.5 * (self.beta + other.beta)
        else:
            new_beta = (abs(self.val) * self.beta + abs(other.val) * other.beta) / total

        # E₀: take from the dominant term
        new_E0 = self.E0 if abs(self.val) >= abs(other.val) else other.E0

        return LoadedHistory(new_val, new_load, new_beta, new_E0, self.theta)._reconfigure_if_needed()

    def __sub__(self, other) -> 'LoadedHistory':
        return self.__add__(-_coerce(other, self))

    def __mul__(self, other) -> 'LoadedHistory':
        other = _coerce(other, self)

        new_val  = self.val * other.val
        new_load = self.val * other.load + self.load * other.val  # Leibniz rule

        # β under multiplication: anomalous dimensions ADD.
        # Physical rationale: in RG, the anomalous dimension of a product
        # of two fields is the sum of their individual anomalous dimensions.
        # This is the correct RG result, not an ad hoc choice.
        new_beta = self.beta + other.beta

        # E₀: geometric mean of the two reference scales
        new_E0 = math.sqrt(self.E0 * other.E0)

        return LoadedHistory(new_val, new_load, new_beta, new_E0, self.theta)._reconfigure_if_needed()

    def __truediv__(self, other) -> 'LoadedHistory':
        other = _coerce(other, self)

        if abs(other.val) < 1e-14:
            raise ZeroDivisionError("Division by zero-valued LoadedHistory.")

        new_val  = self.val / other.val
        new_load = (self.load * other.val - self.val * other.load) / other.val**2  # quotient rule

        # β under division: anomalous dimensions subtract.
        new_beta = self.beta - other.beta
        new_E0   = math.sqrt(self.E0 * other.E0)

        return LoadedHistory(new_val, new_load, new_beta, new_E0, self.theta)._reconfigure_if_needed()

    def __pow__(self, n: float) -> 'LoadedHistory':
        """Integer or real power. Uses the power rule for the gradient."""
        new_val  = self.val ** n
        new_load = self.load * n * self.val ** (n - 1)  # power rule

        # β under power: n times the original (extensive in the exponent)
        new_beta = n * self.beta
        new_E0   = self.E0

        return LoadedHistory(new_val, new_load, new_beta, new_E0, self.theta)._reconfigure_if_needed()

    # Reverse operations so plain numbers work on the left too
    __radd__ = __add__
    __rmul__ = __mul__
    def __rsub__(self, other): return _coerce(other, self).__sub__(self)
    def __rtruediv__(self, other): return _coerce(other, self).__truediv__(self)

    def __repr__(self):
        return (f"LoadedHistory(val={self.val:.6g}, grad={self.load:.3e}, "
                f"β={self.beta:.3f}, E₀={self.E0:.3g}, {self.loading_direction()})")


# ── Elementary functions ───────────────────────────────────────────────────

def dras_exp(x: LoadedHistory) -> LoadedHistory:
    """exp: fixed point of the differentiation gradient (val == derivative)."""
    ev = math.exp(x.val)
    return LoadedHistory(ev, ev * x.load, x.beta, x.E0, x.theta)._reconfigure_if_needed()

def dras_log(x: LoadedHistory) -> LoadedHistory:
    """ln: propagation cost function. d/dx[ln(x)] = 1/x."""
    return LoadedHistory(math.log(x.val), x.load / x.val, x.beta, x.E0, x.theta)._reconfigure_if_needed()

def dras_sin(x: LoadedHistory) -> LoadedHistory:
    return LoadedHistory(math.sin(x.val), math.cos(x.val) * x.load, x.beta, x.E0, x.theta)._reconfigure_if_needed()

def dras_cos(x: LoadedHistory) -> LoadedHistory:
    return LoadedHistory(math.cos(x.val), -math.sin(x.val) * x.load, x.beta, x.E0, x.theta)._reconfigure_if_needed()

def dras_sqrt(x: LoadedHistory) -> LoadedHistory:
    sv = math.sqrt(x.val)
    return LoadedHistory(sv, x.load / (2 * sv), 0.5 * x.beta, x.E0, x.theta)._reconfigure_if_needed()


# ── Exceptions ─────────────────────────────────────────────────────────────

class CoherenceExceeded(Exception):
    """
    Raised when load exceeds the coherence threshold θ_C.
    Observation 2.2: demand > θ means the gradient family cannot contain
    this pattern. The caller must either widen the context or change the
    gradient family.
    """
    pass

class LandauPole(Exception):
    """
    Raised when the RG running hits a Landau pole (denominator → 0).
    The coupling diverges at this scale — the theory breaks down.
    In PL terms: the gradient family has no coherent extension to this
    energy scale. A new carrier is required.
    """
    pass


# ── Internal helper ────────────────────────────────────────────────────────

def _coerce(other, reference: LoadedHistory) -> LoadedHistory:
    """Convert a plain number to a LoadedHistory with zero gradient."""
    if isinstance(other, LoadedHistory):
        return other
    if isinstance(other, (int, float)):
        return LoadedHistory(float(other), 0.0, 0.0, reference.E0, reference.theta)
    return NotImplemented

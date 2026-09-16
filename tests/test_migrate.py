from fractions import Fraction as F
import pytest

from pl.migrate import (
    GUARD, MIGRATE, QPAIR, RECONFIG, Runtime, Theta, V2, V3,
    ChannelPreservationError, Decohered, Ledger,
)


def test_v2_to_v3_bills_reconfig_and_migrate():
    rt = Runtime(V2, F(1))
    rt.reconfigure(V3, "grow")
    kinds = [ln.kind for ln in rt.ledger.lines]
    assert kinds == [RECONFIG, GUARD, MIGRATE]
    assert rt.state == F(1)
    assert rt.carrier.name == "V3"


def test_product_leaves_v3():
    rt = Runtime(V3, F(1, 2))
    with pytest.raises(Theta):
        rt.step(lambda s: s * s)


def test_cannot_drop_live_channel():
    rt = Runtime(QPAIR, (F(1), F(2)))
    with pytest.raises(ChannelPreservationError):
        rt.reconfigure(V3, "drop")


def test_guard_is_not_free():
    rt = Runtime(V2, F(1))
    rt.guard(True, "ok")
    assert rt.ledger.lines[0].kind == GUARD
    assert rt.ledger.total > 0


def test_reconfig_can_hit_theta():
    rt = Runtime(V2, F(1), Ledger(theta=F(1)))
    with pytest.raises(Decohered):
        rt.reconfigure(V3, "no budget")

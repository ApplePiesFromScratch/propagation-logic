from fractions import Fraction as F
import pytest

from pl import LeavesV, Theta, isolate, rate


def test_square_rate():
    x = isolate(3)
    assert rate(x * x, x) == 6


def test_power_and_reciprocal():
    x = isolate(3)
    assert rate(x ** 5, x) == 405
    assert rate(1 / x, x) == F(-1, 9)


def test_gauge():
    rates = {rate(isolate(3, k) ** 2, isolate(3, k)) for k in (1, 2, F(1, 2), -3)}
    assert rates == {6}


def test_chain():
    x = isolate(3)
    y = x * x
    u = y * y
    assert rate(u, y) * rate(y, x) == rate(u, x) == 108


def test_dead_isolation():
    with pytest.raises(Theta):
        rate(isolate(3) ** 2, isolate(3, 0))


def test_pole():
    with pytest.raises(Theta):
        isolate(1) / isolate(0)


def test_zero_over_zero_channels():
    assert rate(isolate(0, 6), isolate(0, 1)) == 6


def test_float_refused():
    with pytest.raises(LeavesV):
        isolate(1.5)


def test_poly_value():
    x = isolate(2)
    y = x ** 3 + 2 * x + 1
    assert y.v == 13
    assert rate(y, x) == 14

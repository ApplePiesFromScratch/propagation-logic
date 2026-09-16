from pl import certify


def test_square_certificate():
    c = certify(lambda z: z * z, at=3)
    assert c.ok
    assert c.value == "6"
    assert c.gauge_ok
    assert c.tier == "FORCED-on-cut"
    assert c.discharged == c.scope == 32
    assert c.falsifier


def test_poly_certificate():
    c = certify(lambda z: z ** 3 + 2 * z, at=3)
    assert c.value == "29"
    assert c.ok


def test_reciprocal_certificate():
    c = certify(lambda z: 1 / z, at=3, values=(-4, -2, -1, 1, 2, 3, 4))
    assert c.value == "-1/9"
    assert c.ok
    assert c.gauge_ok

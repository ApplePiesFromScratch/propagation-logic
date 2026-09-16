# cutad

Isolation-tagged forward AD. Exact rationals. Certificates.

A reading carries a value and a channel. A rate is their ratio under a
named isolation. Poles and dead cuts refuse (`Theta`); they do not
become `Inf`. A published number can carry a certificate: statement,
value, cut, discharged/scope, tier, falsifier.

This is a map. It does not claim to be how variation *is*.

```
V = exact Q
G = Leibniz mix + binary rate(P, G)
θ = r ≠ 0 to form a rate; v ≠ 0 to divide
```

## Install

```
pip install -e .
```

Python 3.10+, stdlib only.

## Use

```python
from cutad import isolate, rate, certify

x = isolate(3)
rate(x * x, x)       # 6
rate(x ** 5, x)      # 405
rate(1 / x, x)       # -1/9

c = certify(lambda z: z ** 3 + 2 * z, at=3)
print(c.value)       # 29
print(c.tier)        # FORCED-on-cut
print(c.as_json())
```

Gauge: change the seed, the ratio stays.

```python
rate(isolate(3, 2) ** 2, isolate(3, 2))   # still 6
```

## CLI

```
python -m cutad          # demo
python -m cutad cert     # JSON certificate
python -m cutad vs-fd    # exact 6 vs finite-difference 6+h
```

## Tests

```
pip install -e ".[dev]"
pytest
```

## Operator distinction

`docs/OPERATOR_GUIDE.md` — protocol for telling operators apart under
`(V, G, θ)` and testing them (close-test, θ-test, coincidence-test).

```
PYTHONPATH=. python3 docs/operator_test.py
```

## What this is for

Keep `cutad` as a reference kernel next to float AD (JAX, dual floats).
On the declared grid the float kernel is not allowed to disagree.
The certificate is what CI, a paper, or an auditor can fail.

## What this is not

Reverse-mode. GPU. `sin` / `sqrt` on `V = Q`. A replacement for
PyTorch. Those need a richer `V` or a different repo.

`isolate` is unpriced. Every result sits downstream of a cut someone
already chose.

## License

MIT

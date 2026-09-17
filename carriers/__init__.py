"""carriers — the catalog as data. Order follows the source PDF."""
from . import (propositional, modal, manyvalued, settype, mathematical,
               cs, physics, evidence, interpretations, process)

SECTIONS = [
    ("Propositional Logic", propositional.CARRIERS),
    ("Modal Logic", modal.CARRIERS),
    ("Many-Valued Logic", manyvalued.CARRIERS),
    ("Set Theory & Type Theory", settype.CARRIERS),
    ("Mathematical Carriers", mathematical.CARRIERS),
    ("Computer Science", cs.CARRIERS),
    ("Physics", physics.CARRIERS),
    ("Probability & Evidence", evidence.CARRIERS),
    ("Measurement Interpretations", interpretations.CARRIERS),
    ("Generated Atlas", process.CARRIERS),
]

ALL = [c for _, cs_ in SECTIONS for c in cs_]

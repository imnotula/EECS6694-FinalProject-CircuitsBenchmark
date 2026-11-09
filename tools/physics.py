"""Solve the two-node equations. Units internally are V, mA, kΩ, µF and ms."""
from dataclasses import dataclass
import re
import numpy as np


@dataclass
class Circuit:
    high: float
    resistors: dict
    capacitor: tuple


def read_netlist(text):
    rows = text.strip().splitlines()
    source = re.fullmatch(r"V1 IN 0 PULSE\(0 ([\d.]+) 0 1n 1n 5 10\)", rows[1])
    if not source or rows[-1].lower()!=".end":
        raise ValueError("unexpected source or incomplete netlist")
    resistors = {}
    cap = None
    for row in rows[2:-1]:
        name, p, q, value = row.split()
        if name.startswith("R") and value.endswith("k"):
            resistors[name] = (p,q,float(value[:-1]))
        elif name=="C1" and value.endswith("u"):
            cap = (p,q,float(value[:-1]))
        else:
            raise ValueError(f"unsupported component {row}")
    if len(resistors)!=4 or cap is None:
        raise ValueError("expected four resistors and one capacitor")
    return Circuit(float(source.group(1)), resistors, cap)


def incidence(p,q):
    v = np.array([int(p==n)-int(q==n) for n in ("X","OUT")], dtype=float)
    return v, int(p=="IN")-int(q=="IN")


def solve(circuit, double=None):
    G = np.zeros((2,2))
    rhs = np.zeros(2)
    for ref,(p,q,r) in circuit.resistors.items():
        a, input_sign = incidence(p,q)
        g = 1/(r*(2 if ref==double else 1))
        G += g*np.outer(a,a)
        rhs -= g*a*input_sign*circuit.high
    p,q,cap = circuit.capacitor
    d, input_sign = incidence(p,q)
    final = np.linalg.solve(G,rhs)
    # The capacitor starts uncharged. Enforce zero voltage across it at 0+.
    constrained = np.zeros((3,3))
    constrained[:2,:2] = G
    constrained[:2,2] = constrained[2,:2] = d
    initial = np.linalg.solve(constrained,np.r_[rhs,-input_sign*circuit.high])
    # A 1 mA test current at the capacitor terminals yields Rth in kΩ
    # with the independent voltage source set to zero.
    r_th = d @ np.linalg.solve(G,d)
    return dict(initial_v=float(initial[1]), settled_v=float(final[1]),
                rth_kohm=float(r_th), tau_ms=float(r_th*cap))

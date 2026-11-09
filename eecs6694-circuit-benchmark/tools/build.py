"""Rebuild the participant inputs, copyable questions and private grading keys."""
from pathlib import Path
import json

from designs import COMMON_PROMPT, DESIGNS, EDGES, questions
from draw import render
from physics import read_netlist, solve


ROOT = Path(__file__).resolve().parents[1]


def netlist(d):
    lines = [d.id, f"V1 IN 0 PULSE(0 {d.high_v} 0 1n 1n 5 10)"]
    for ref,edge,value in d.parts():
        a,b = EDGES[edge]
        suffix = "k" if ref.startswith("R") else "u"
        lines.append(f"{ref} {a} {b} {value:g}{suffix}")
    return "\n".join([*lines,".end",""])


def main():
    keys, catalog = {}, []
    for d in DESIGNS:
        folder = ROOT/"inputs"/d.id
        folder.mkdir(parents=True,exist_ok=True)
        text = netlist(d)
        (folder/"circuit.cir").write_text(text)
        render(d,folder/"schematic.png",ROOT/"ablations"/d.id/"small-junctions.png")
        items = questions(d)
        (folder/"questions.md").write_text(
            "# "+d.id+"\n\nAdd the common instruction and exactly one question to each request.\n\n"
            +COMMON_PROMPT+"\n\n"+"\n\n".join(f"**{n}.** {q}" for n,q in items.items())+"\n")
        c = read_netlist(text)
        base, changed = solve(c), solve(c,d.double)
        direction = "upward" if base["initial_v"] < base["settled_v"] else "downward"
        labels = [name for name,(p,q,_) in c.resistors.items() if "OUT" in (p,q)]
        if "OUT" in c.capacitor[:2]:
            labels.append("C1")
        short = " = ".join(c.capacitor[:2])
        keys[d.id] = dict(family=d.family, capacitor_nodes=list(c.capacitor[:2]),
            Q1=sorted(labels), Q2=dict(direction=direction, initially_equal=short),
            Q3_V=base["settled_v"], Q4_ms=changed["tau_ms"],
            double=d.double, baseline=base, changed=changed)
        catalog.append(f"| {d.id} | {d.family} | {'–'.join(c.capacitor[:2])} | "
            f"{', '.join(sorted(labels))} | {direction} | {base['initial_v']:.4g} | "
            f"{base['settled_v']:.4g} | {d.double} | {changed['tau_ms']:.4g} |")
    (ROOT/"team"/"keys.json").write_text(json.dumps(keys,indent=2,allow_nan=False)+"\n")
    intro = """# Team circuit catalog

All 12 cases are for development. A–D identify the four resistor wiring patterns. Each occurs with three different capacitor placements. The two voltages are at OUT, immediately after the ideal input step and after settling. The final column is the time constant after the indicated resistor is doubled.

| ID | Family | C1 terminals | Q1 components on OUT | Q2 settling | Initial V | Q3 settled V | Double for Q4 | Q4 τ (ms) |
| --- | --- | --- | --- | --- | ---: | ---: | --- | ---: |
"""
    (ROOT/"team"/"catalog.md").write_text(intro+"\n".join(catalog)+"\n")


if __name__=="__main__":
    main()

"""Independently check each key against samples of two ngspice transients."""
import argparse
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MEASURES = """.tran 10u 101m 0 10u
.meas tran early find v(out) at=2n
.meas tran first find v(out) at=0.5m
.meas tran second find v(out) at=2m
.meas tran settled find v(out) at=100m
"""


def simulate(binary, netlist, ref=None):
    lines = netlist.strip().splitlines()
    if ref:
        i, = [i for i,line in enumerate(lines) if line.startswith(ref+" ")]
        fields = lines[i].split()
        fields[-1] = f"{2*float(fields[-1][:-1]):g}k"
        lines[i] = " ".join(fields)
    assert lines[-1]==".end"
    deck = "\n".join(lines[:-1])+"\n"+MEASURES+".end\n"
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp)/"check.cir"
        path.write_text(deck)
        result = subprocess.run([binary,"-b",str(path)],cwd=temp, capture_output=True,
                                text=True,timeout=90)
    output = result.stdout+"\n"+result.stderr
    found = dict(re.findall(r"^\s*(early|first|second|settled)\s*=\s*([0-9eE+.\-]+)",
                            output,re.MULTILINE))
    if result.returncode or len(found)!=4:
        raise RuntimeError("ngspice measurements failed\n"+output[-3000:])
    m = {key:float(val) for key,val in found.items()}
    # For a first-order response, subtracting the settled voltage isolates
    # the decaying exponential. The two samples are 1.5 ms apart.
    ratio = (m["first"]-m["settled"])/(m["second"]-m["settled"])
    return dict(initial_v=m["early"], settled_v=m["settled"], tau_ms=1.5/math.log(ratio))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ngspice",default="ngspice",help="path to the ngspice executable")
    ap.add_argument("--report",type=Path,help="optional path to write measured values as JSON")
    args = ap.parse_args()
    executable = shutil.which(args.ngspice)
    if not executable:
        ap.error("ngspice is missing. Install ngspice or pass --ngspice /path/to/ngspice.")
    version = subprocess.run([executable,"--version"],capture_output=True,text=True,check=True)
    match = re.search(r"ngspice-[\d.]+",version.stdout+version.stderr,re.IGNORECASE)
    data = {"simulator":match.group(0) if match else "ngspice","units":"V, ms","runs":[]}
    keys = json.loads((ROOT/"team"/"keys.json").read_text())
    for name,key in keys.items():
        net = (ROOT/"inputs"/name/"circuit.cir").read_text()
        for condition,ref in [("baseline",None),("changed",key["double"])]:
            values = simulate(executable,net,ref)
            for field,actual in values.items():
                expected = key[condition][field]
                ok = math.isclose(actual,expected,rel_tol=0.002,
                                  abs_tol=0.001 if field!="tau_ms" else 0.0005)
                if not ok:
                    raise ValueError(f"{name} {condition} {field}: measured {actual}, key {expected}")
            data["runs"].append({"case":name,"condition":condition,**values})
        d = "upward" if data["runs"][-2]["settled_v"]>data["runs"][-2]["initial_v"] else "downward"
        assert d==key["Q2"]["direction"], name
    if args.report:
        args.report.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")
    print(f"{data['simulator']}: {len(data['runs'])} transients passed. Voltage limits, settling directions and time constants agree.")


if __name__=="__main__":
    main()

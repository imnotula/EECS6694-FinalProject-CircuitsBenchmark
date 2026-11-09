# C001 answer key

Intended for the team member checking circuits and scoring responses.

| Question | Credit rule for this development case |
| --- | --- |
| Q1 | Give 1 point for exactly R2 and R3, in either order. Case and equivalent prose are fine. |
| Q2 | Give 1 point if the answer identifies a voltage divider or equivalent resistive attenuation and describes R3's role. R3 is in parallel with R2, provides another current path to ground and loads the output. Any one of these descriptions earns credit for the role. R2 and R3 are electrically interchangeable in the original circuit. |
| Q3 | Give 1 point for 3.00 V within ±0.01 V, including equivalent units. |
| Q4 | Give 1 point for both a rise and 3.60 V within ±0.01 V, including equivalent units. “Rises from 3 V to 3.6 V” earns full credit. |

Use 0 for other completed responses. Flag ambiguous cases for a second reader. The tolerances and wording are starter decisions for this circuit.

## Independent checks

R2 and R3 each connect OUT to ground. Their parallel combination forms the lower leg of a divider with R1 as the upper leg.

- With both lower resistors at 2 kΩ, their parallel resistance is 1 kΩ. The output is 6 × 1/(1 + 1) = 3.00 V.
- With R3 at 6 kΩ, the parallel resistance is (2 × 6)/(2 + 6) = 1.5 kΩ. The new output is 6 × 1.5/(1 + 1.5) = 3.60 V.
- Ignoring R3 gives 6 × 2/(1 + 2) = 4 V in the original circuit. A 4 V answer suggests a branch worth investigating. Use the model's actual words or its separate connectivity answer to assess the possible explanation.

Both voltages were also checked by solving the node equations from the netlist. To add the team's independent SPICE verification, open the extracted project folder in a terminal with ngspice installed and run the following command.

```sh
ngspice inputs/C001.cir
```

At the ngspice prompt enter these lines in order. The change to R3 applies to this simulator session.

```text
op
print v(out)
alter r3 = 6000
op
print v(out)
quit
```

Record the simulator version and both measured voltages in the run log. The official beginner tutorial walks through loading a netlist and finding a DC operating point. [ngspice tutorial, section 3](https://ngspice.sourceforge.io/ngspice-tutorial.html)

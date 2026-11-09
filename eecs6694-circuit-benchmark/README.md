# EECS 6694 · Circuit understanding benchmark

Does a multimodal model answer the same electrical question differently when it receives a schematic image or a SPICE netlist?

[Browse the 12 circuit drawings](docs/gallery.md)

## Start with P01

1. Open [the P01 schematic](inputs/P01/schematic.png) and [its netlist](inputs/P01/circuit.cir). Trace X and OUT with a teammate. Use [the worked solution](team/P01-worked.md) to check your interpretation.
2. Pick two specific multimodal model versions your team can access. In a fresh session, give the first model the P01 image, the common instruction and Q1 from [the question sheet](inputs/P01/questions.md). In another fresh session, give the same model the netlist text, the same instruction and Q1.
3. For the formal pilot, use the shuffled [first-four run log](team/pilot-first-four.csv). It contains 64 planned requests covering P01–P04. For each request send only the specified input, instruction and single question. Use a copy of the CSV to store full responses and scores.
4. Score each response using the [rules](docs/protocol.md) and [team key](team/catalog.md). Keep the archive, repository URL, worked solutions, previous answers and simulated outputs outside model sessions. If the first two practice requests used the exact fixed protocol and settings, enter them in their matching rows once.

## Circuits and scope

The 12 development cases all have one ideal step-voltage source, four resistors, one capacitor, two unknown circuit-node voltages and one time constant. X and OUT are coupled by a resistor. Current can divide at a branch. The charging path can include several resistors. Each schematic has the same dimensions, symbols, line width and text scale. A–D below are team-side names for the four resistor wiring patterns.

| Resistor wiring | Capacitor between X and OUT | Capacitor between X and ground | Capacitor between IN and X |
| --- | --- | --- | --- |
| A · IN feeds OUT through X | [P01](inputs/P01) | [P09](inputs/P09) | [P05](inputs/P05) |
| B · X has no direct ground resistor | [P06](inputs/P06) | [P02](inputs/P02) | [P10](inputs/P10) |
| C · OUT has no direct ground resistor | [P11](inputs/P11) | [P07](inputs/P07) | [P03](inputs/P03) |
| D · X has no direct resistor to IN | [P04](inputs/P04) | [P08](inputs/P08) | [P12](inputs/P12) |

Every case tests the same four skills. Q1 identifies which parts touch OUT. Q2 asks how the output settles after a rising input step. Q3 asks for its final voltage. Q4 asks for its new time constant after one specified resistor doubles. Q2 is a functional behavior question. Interpreting the output as a low-pass or high-pass filter is unnecessary.

**Verification status.** The analytical key and 24 ngspice-46 transients agree for the baseline and changed circuit in every case. The [measurement record](team/spice-verification.json) contains simulated values. No model responses have been collected in the provided log. Similar complexity is a design decision. The pilot measures how difficult the items actually are.

## Project materials

- [Evaluation protocol, difficulty criteria and ablation](docs/protocol.md)
- [All 16 proposal references, reading notes and one additional related benchmark](docs/references.md)
- [Circuit catalog and scoring key](team/catalog.md) · [full-precision keys](team/keys.json)
- [Original proposal](docs/source/proposal.pdf) · [course requirements](docs/source/course-project-requirements.png)
- [Earlier DC voltage-divider warm-up](warmup/START_HERE.md), outside the 12 matched cases
- [Smaller-junction schematics](ablations), one optional visual control per base circuit

## Reproduce

The committed images, netlists, questions and first-four log are ready to use. For regeneration, use Python 3.10 or later and a native ngspice installation. On macOS with Homebrew, `brew install ngspice` installs the simulator.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/build.py
python tools/verify_spice.py
```

To create a new full pilot log and later summarize a copy with scores, run

```sh
python tools/pilot.py new full-pilot.csv --all --models model_A model_B
python tools/pilot.py summary full-pilot.csv
```

The two-model full pilot schedules 192 separate requests. The run log and summary use the Python standard library. Native ngspice can reproduce the independent checks. The recorded run used ngspice-46 compiled to WebAssembly from the [distribution](https://github.com/z-wasm/ngspice-wasm/blob/zero/README.md), with engine Git blob `07df5e5d6607628589c3034b214098bae60319cf`.

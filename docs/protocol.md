# Pilot protocol

## What counts as one example

One case is one labeled electrical circuit with one capacitor placement. Each input pair shares all components, values, source timing, node labels and output definition. The four resistor wiring patterns each have three capacitor placements. These 12 related cases are development data. Count a drawing variant or changed resistor question under its original case. Mirroring source and ground relates some wiring patterns, so the 12 cases cannot support a claim about 12 independent circuit families.

## Run the baseline

- Choose two available model versions that accept both PNG and text. Record interface, version or displayed name, date, reasoning mode, sampling settings and response budget. Record settings hidden by the app as unknown.
- Use one fresh, memory-isolated session or stateless API request per model, format, case and question. Disable browsing, code execution and external simulators. Keep prompts and model settings fixed across both inputs. Paste the netlist text verbatim or attach the one schematic PNG. Copy the identical common instruction and one question from its case folder.
- Save the full first eligible response. Log a technical failure and any exact retry. A wrong answer or refusal to solve a valid question is a scored response. Leave missing or interrupted requests pending. Record external-tool runs and repeat them in an eligible setting.
- Use P01–P04 first. On each case, two models × two formats × four questions yields 16 responses. If prompts or grading rules change after development, version and retain the old pilot results separately.

## Score one response

| Question | Award one point when |
| --- | --- |
| Q1 · Connectivity | The unordered set of component labels on OUT matches the key. Ignore capitalization, punctuation and equivalent phrasing. Extra or missing parts receive zero. |
| Q2 · Function | The response gives the correct settling direction after the edge and explains C1's placement. Accept the appropriate initial equality (e.g. X and OUT initially equal) followed by resistive settling, or correct initial and final voltages tied to the capacitor's behavior. “Capacitors charge” on its own is insufficient. |
| Q3 · DC output | The physical answer is within the larger of 0.01 V or 1% of the reference voltage. Accept convertible units. The common instruction asks for units. |
| Q4 · Resistor change | The answer is within the larger of 0.005 ms or 1% of the reference time constant **after** the named resistor doubles. Accept equivalent time units. |

Use zero for an incorrect final answer, including missing or incompatible units in Q3/Q4. If the response gives multiple incompatible final answers with no selection, score zero. Have a second teammate score ambiguous Q2 responses independently and record the agreed decision. Use the full-precision JSON values for numeric tolerances.

## Check the difficulty before freezing a test

Compare within each model and question type. Keep Q1 as a reading check even if everyone passes. For the first four circuits, inspect every pair of answers and resolve confusing wording or rendering. Four cases are enough to catch obvious problems. Their scores are noisy.

For all 12 pilot cases, a provisional design target is **30–80% correct on Q2–Q4 combined**, with results also broken down by model, input and question. The range is a team planning choice. If both models approach 100% in both formats across many cases, increase the shared reasoning burden across the next development batch. If both models approach 0% in both formats, first audit the questions and key; then simplify the shared operation. If the scores separate by format, preserve that result. Log the entire pilot, including easy and hard cases, before adjusting future designs.

Compare the matched pairs for each model and task. Report both correct, image only correct, netlist only correct, and both wrong alongside correct/scored counts. A wrong numerical answer and a right netlist answer can motivate a visual-error hypothesis. Look for corroborating evidence such as a missing component on Q1 and keep an unclear category.

## One controlled visual experiment

Each file under `ablations/` changes the radius of the filled junction markers from 5.5 to 3.25 drawing units in the same source drawing. Wires still meet at the same points. Use the same prompts and model settings. Evaluate the baseline and smaller-dot images in fresh sessions and report correct-to-wrong and wrong-to-correct flips separately. Reuse the baseline netlist results for the same case and model.

## Final study

Freeze the questions, scoring rules and model settings before opening a fresh test set. Group variants and equivalent or rail-mirrored resistor templates when splitting. Use new base families for claims about generalization. The whole initial collection is one small passive RC domain; generalization to transistor, op-amp, digital or design tasks requires additional data. The course report can present motivation, related work, reproducible methods, main results, the visual ablation and limitations.

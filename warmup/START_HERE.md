# Run your first circuit comparison

**Goal for one meeting.** See whether one model gives the same correct answer when it sees a drawing of a circuit and when it reads that circuit as text. C001 is a development case for trying the procedure.

## Prepare

1. Unzip the folder. Open the PNG and the `.cir` text file in `inputs/`. Have one teammate trace both sides of each component from the drawing and another check each line of the netlist. In SPICE, node `0` is ground. For example, `R1 IN OUT 1k` means a 1 kΩ resistor connects IN and OUT.
2. Pick one model that accepts both images and text. Use the same model, settings and response budget throughout. Use independent API requests or fresh temporary chats with history, memory and external tools disabled. Record the model name or version shown in the interface.
3. Have a teammate check the reference values with the simulator instructions in `team_only/answer_key.md`. Give the model only the selected input and the prompt for one question. Keep the answer key and log with your team.

## Ask four questions in two formats

Start each request with this exact instruction, then add one of the questions below.

> Assume ideal components and DC steady state. Node 0 is ground. Use only the supplied circuit. Answer the question below in one sentence, and include units for numerical answers.

| ID | Task | Question to paste |
| --- | --- | --- |
| Q1 | Connections | Which components connect directly between OUT and node 0? List their labels. |
| Q2 | Function | What function does this circuit perform from IN to OUT, and what role does R3 play? |
| Q3 | Numerical output | What is the DC voltage at OUT relative to node 0? |
| Q4 | Component change | If only R3 changes to 6 kΩ, does the DC voltage at OUT rise, fall, or stay the same, and what is its new value relative to node 0? |

For the image run, attach only `inputs/C001.png` to the text of the request. For the netlist run, paste the complete contents of `inputs/C001.cir` with the same request. Start a fresh session for every question and format, including Q4. The original circuit is the input in all eight sessions.

## Record and discuss

Use `team_only/run_log.md` to save the model settings, all eight responses and the scores. If a response uses an external tool, record that and rerun in a tool-disabled setting before scoring that condition. If a request fails technically, record it and retry the same input. Score the first completed eligible response.

Compare the two answers to each question. If the team disagrees on a score, write down the exact wording that caused the disagreement. Fix unclear questions and grading rules on development cases before freezing them for the final test.

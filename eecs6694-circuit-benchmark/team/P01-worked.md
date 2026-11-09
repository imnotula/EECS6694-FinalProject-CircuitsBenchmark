# P01 worked example

V1 steps from 0 to 8 V. R1 connects IN–X (2 kΩ), R2 connects X–0 (4 kΩ), R3 connects X–OUT (2 kΩ), and R4 connects OUT–0 (2 kΩ). C1 is 1 µF between X and OUT. In the calculations below, every resistance is in kΩ.

**Q1 · Connections.** R3, R4 and C1 each have a terminal on OUT.

**Q2 · Function.** Immediately after the input step, the uncharged capacitor holds X and OUT at the same voltage. R3 has zero initial voltage across it. R2 and R4 then both lead from this shared voltage to ground. Their parallel resistance is 4 ∥ 2 = 4/3. The initial output is 8 × (4/3)/(2 + 4/3) = **3.20 V**. It settles **downward** to 2.00 V.

**Q3 · Final DC voltage.** At long times C1 carries zero DC current. From X to ground, R2 is in parallel with the R3–R4 series path. Their equivalent is 4 ∥ (2 + 2) = 2. X is at 8 × 2/(2 + 2) = 4 V. R3 and R4 then divide that voltage equally, so **OUT = 2.00 V**.

**Q4 · Changed time constant.** R4 doubles to 4 kΩ. Remove C1 and set the ideal voltage source to zero, which joins IN to ground. Viewed between X and OUT, R3 is in parallel with the path through (R1 ∥ R2) and the new R4. The resistance seen by the capacitor is 2 ∥ [(2 ∥ 4) + 4] = 16/11 kΩ. Multiplying by 1 µF gives **1.45 ms** to three significant digits.

Here “∥” denotes the parallel combination of two resistances, ab/(a+b). A kΩ times a µF is a millisecond.

"""Component values use kΩ and µF. Each row lists R1, R2, R3, R4 in that order."""
from dataclasses import dataclass


EDGES = {
    "IX": ("IN", "X"),
    "X0": ("X", "0"),
    "IO": ("IN", "OUT"),
    "O0": ("OUT", "0"),
    "XO": ("X", "OUT"),
}


@dataclass(frozen=True)
class Design:
    id: str
    high_v: int
    resistors: tuple
    capacitor: tuple
    double: str

    def parts(self):
        for i, (edge, value) in enumerate(self.resistors, 1):
            yield f"R{i}", edge, value
        yield "C1", *self.capacitor

    @property
    def family(self):
        all_resistors = {edge for edge, _ in self.resistors}
        missing, = EDGES.keys() - all_resistors
        return {"IO": "A", "X0": "B", "O0": "C", "IX": "D"}[missing]


DESIGNS = [
    Design("P01", 8, (("IX", 2), ("X0", 4), ("XO", 2), ("O0", 2)), ("XO", 1), "R4"),
    Design("P02", 6, (("IO", 4), ("XO", 2), ("O0", 3), ("IX", 3)), ("X0", 1.5), "R4"),
    Design("P03", 9, (("XO", 3), ("IX", 3), ("IO", 4), ("X0", 2)), ("IX", 1), "R4"),
    Design("P04", 8, (("O0", 4), ("XO", 3), ("X0", 2), ("IO", 2)), ("XO", 1.2), "R2"),
    Design("P05", 9, (("X0", 3), ("IX", 2), ("O0", 4), ("XO", 2)), ("IX", 1.5), "R2"),
    Design("P06", 6, (("IX", 2), ("O0", 3), ("IO", 2), ("XO", 4)), ("XO", 1), "R1"),
    Design("P07", 8, (("IO", 4), ("X0", 3), ("XO", 2), ("IX", 2)), ("X0", 1.2), "R2"),
    Design("P08", 9, (("XO", 2), ("O0", 3), ("IO", 3), ("X0", 4)), ("X0", 1.5), "R1"),
    Design("P09", 6, (("O0", 4), ("IX", 3), ("XO", 2), ("X0", 2)), ("X0", 1), "R4"),
    Design("P10", 8, (("O0", 2), ("XO", 3), ("IX", 3), ("IO", 4)), ("IX", 1.2), "R3"),
    Design("P11", 6, (("IX", 4), ("IO", 2), ("X0", 3), ("XO", 2)), ("XO", 1.5), "R4"),
    Design("P12", 9, (("X0", 2), ("IO", 4), ("O0", 3), ("XO", 3)), ("IX", 1), "R1"),
]

COMMON_PROMPT = (
    "Use only the supplied circuit. All parts are ideal, node 0 is ground, and OUT is "
    "unloaded apart from the shown parts. Before the first edge, IN has been at 0 V "
    "for a long time. V1 rises to its shown high value. Its rise and fall times are "
    "1 ns, its high time is 5 s, and its period is 10 s. Analyze the first high "
    "plateau. Treat the rising edge as instantaneous for limit calculations. "
    "Give the requested answer with its units."
)


def questions(design):
    return {
        "Q1": "Which components have a terminal directly on OUT? List their reference labels.",
        "Q2": "Immediately after any instantaneous output jump, does OUT settle upward or downward? Explain how C1's connection causes that behavior in one sentence.",
        "Q3": "What is the settled voltage at OUT relative to node 0 during the first high plateau? Give three significant digits.",
        "Q4": f"If only {design.double} is doubled, what is the new time constant of the output response, in milliseconds? Give three significant digits.",
    }

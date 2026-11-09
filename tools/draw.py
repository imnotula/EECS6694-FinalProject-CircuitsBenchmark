"""Draw the circuit and independently trace its wires before writing either PNG."""
from collections import defaultdict
from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont
from designs import EDGES


SCALE = 2
WIDTH, HEIGHT = 998, 560
TOP, MID, BOT = 70, 267, 473
SRC, AUX, OUT, CAPX = 86, 438, 797, 305
NODES = {"IN": (SRC, TOP), "0": (SRC, BOT), "X": (AUX, MID), "OUT": (OUT, MID)}
INK = "#17212b"


def font(size):
    candidates = [
        "DejaVuSans.ttf", "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size * SCALE)
        except OSError:
            pass
    return ImageFont.load_default(size=size * SCALE)


class Schematic:
    def __init__(self):
        self.image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.wires = []
        self.pins = {}
        self.junctions = set()
        self.fonts = {s: font(s) for s in (22, 24, 25)}

    def stroke(self, *points, width=3):
        self.draw.line([(round(x*SCALE), round(y*SCALE)) for x,y in points],
                       fill=INK, width=width*SCALE, joint="curve")

    def wire(self, *points):
        self.stroke(*points)
        self.wires.extend(zip(points, points[1:]))

    def label(self, xy, value, anchor="lm", size=24):
        self.draw.text((xy[0]*SCALE, xy[1]*SCALE), value, font=self.fonts[size],
                       fill=INK, anchor=anchor)

    def circle(self, x, y, radius, solid):
        box = tuple(v*SCALE for v in (x-radius,y-radius,x+radius,y+radius))
        self.draw.ellipse(box, fill=INK if solid else "white", outline=INK,
                          width=1 if solid else 3*SCALE)

    def passive(self, ref, value, a, b, label_xy, anchor):
        distance = math.dist(a,b)
        dx, dy = (b[0]-a[0])/distance, (b[1]-a[1])/distance
        cx, cy = (a[0]+b[0])/2, (a[1]+b[1])/2

        def local(along, across=0):
            return (cx+dx*along-dy*across, cy+dy*along+dx*across)

        is_r = ref.startswith("R")
        half = 38 if is_r else 7
        p, q = local(-half), local(half)
        self.wire(a,p)
        self.wire(q,b)
        if is_r:
            wave = [(-38,0),(-32,-9),(-21,9),(-11,-9),(0,9),(11,-9),(21,9),(32,-9),(38,0)]
            self.stroke(*(local(s,t) for s,t in wave))
        else:
            for s in (-half,half):
                self.stroke(local(s,-18), local(s,18))
        self.pins[ref] = (p,q)
        self.label(label_xy, ref, anchor)
        unit = "kΩ" if is_r else "µF"
        self.label((label_xy[0],label_xy[1]+27), f"{value:g} {unit}", anchor, 22)

    def check_connections(self, expected):
        # Join any contact of orthogonal conductors. The baseline contains no
        # nonconnecting crossings; a stray touching lead must fail this check.
        points = set(NODES.values())
        for ends in [*self.wires, *self.pins.values()]:
            points.update(ends)
        straight = []
        for (x1,y1),(x2,y2) in self.wires:
            assert x1==x2 or y1==y2, "a lead is not orthogonal"
            straight.append((min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2)))
        for x1,y1,x2,y2 in straight:
            if y1==y2:
                for x3,y3,x4,y4 in straight:
                    if x3==x4 and x1<=x3<=x2 and y3<=y1<=y4:
                        points.add((x3,y1))
        neighbors = defaultdict(set)
        for left,top,right,bottom in straight:
            same = sorted((x,y) for x,y in points if left<=x<=right and top<=y<=bottom)
            for p,q in zip(same,same[1:]):
                neighbors[p].add(q)
                neighbors[q].add(p)
        node_of = {}
        for name, start in NODES.items():
            stack = [start]
            visited = {start}
            while stack:
                p = stack.pop()
                assert p not in node_of, "two named nodes are shorted"
                node_of[p] = name
                upcoming = neighbors[p] - visited
                visited.update(upcoming)
                stack.extend(upcoming)
        assert set(self.pins)==set(expected)
        for ref, (p,q) in self.pins.items():
            assert (node_of[p],node_of[q])==expected[ref], (ref,p,q,expected[ref])
        self.junctions.update(p for p, adjacent in neighbors.items() if len(adjacent)>=3)

    def export(self, normal, small):
        for path, radius in [(normal,5.5), (small,3.25)]:
            drawing = self.image.copy()
            ink = ImageDraw.Draw(drawing)
            for x,y in self.junctions:
                box=tuple(round(v*SCALE) for v in (x-radius,y-radius,x+radius,y+radius))
                ink.ellipse(box,fill=INK)
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            drawing.save(path, optimize=True)


def render(design, normal, small):
    s = Schematic()
    resistor_edges = dict(design.resistors)
    cap_edge, _ = design.capacitor
    upper = [x for edge,x in [("IX",AUX),("IO",OUT)] if edge in resistor_edges]
    lower = [x for edge,x in [("X0",AUX),("O0",OUT)] if edge in resistor_edges]
    if cap_edge=="IX":
        upper.append(CAPX)
    if cap_edge=="X0":
        lower.append(CAPX)
    s.wire((SRC,TOP),(max(upper),TOP))
    s.wire((SRC,BOT),(max(lower),BOT))
    s.wire((SRC,TOP),(SRC,MID-29))
    s.wire((SRC,MID+29),(SRC,BOT))
    s.circle(SRC,MID,29,False)
    s.stroke((SRC-7,MID-10),(SRC+7,MID-10))
    s.stroke((SRC,MID-17),(SRC,MID-3))
    s.stroke((SRC-7,MID+11),(SRC+7,MID+11))
    s.pins["V1"] = ((SRC,MID-29),(SRC,MID+29))
    s.label((SRC+44,MID-14),"V1")
    s.label((SRC+44,MID+15),f"0 → {design.high_v} V",size=22)
    s.wire((SRC,BOT),(SRC,BOT+20))
    for y,half in [(BOT+20,18),(BOT+27,12),(BOT+34,5)]:
        s.stroke((SRC-half,y),(SRC+half,y))
    s.label((SRC+32,BOT+26),"0")
    s.label((SRC,TOP-25),"IN","mm",25)
    s.label((AUX+14,MID-23),"X",size=25)
    s.label((OUT+14,MID-23),"OUT",size=25)
    arms = {
        "IX": ((AUX,TOP),(AUX,MID),(AUX+21,153),"lm"),
        "X0": ((AUX,MID),(AUX,BOT),(AUX+21,357),"lm"),
        "IO": ((OUT,TOP),(OUT,MID),(OUT+21,153),"lm"),
        "O0": ((OUT,MID),(OUT,BOT),(OUT+21,357),"lm"),
        "XO": ((AUX,MID),(OUT,MID),((AUX+OUT)//2,MID-58),"mm"),
    }
    for ref, edge, value in design.parts():
        if ref.startswith("R"):
            s.passive(ref,value,*arms[edge])
        elif edge in ("IX","X0"):
            s.wire((CAPX,MID),(AUX,MID))
            y1,y2 = (TOP,MID) if edge=="IX" else (MID,BOT)
            s.passive(ref,value,(CAPX,y1),(CAPX,y2),(CAPX-31,(y1+y2)//2-12),"rm")
        else:
            left,right,y = AUX+47,OUT-47,MID+67
            s.wire((left,MID),(left,y))
            s.wire((right,MID),(right,y))
            s.passive(ref,value,(left,y),(right,y),((left+right)//2,y+36),"mm")
    expected = {ref:EDGES[edge] for ref,edge,_ in design.parts()}
    expected["V1"] = ("IN","0")
    s.check_connections(expected)
    s.export(normal,small)

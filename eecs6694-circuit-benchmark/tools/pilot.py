"""Create a randomized run log and summarize manually graded model answers."""
import argparse
from collections import defaultdict
import csv
from itertools import product
from pathlib import Path
import random

from designs import DESIGNS


FIELDS = ["case","question","format","model_slot","model_version","date_time_zone",
          "interface_settings","raw_response","score","evidence_or_retry_note"]


def create(path, all_cases, models):
    cases = DESIGNS if all_cases else DESIGNS[:4]
    rows = list(product([c.id for c in cases],["Q1","Q2","Q3","Q4"],
                        ["image","netlist"],models))
    random.Random(6694).shuffle(rows)
    # Keep completed work safe if a filename is reused.
    with path.open("x",newline="",encoding="utf-8") as fp:
        writer = csv.writer(fp,lineterminator="\n")
        writer.writerow(FIELDS)
        for row in rows:
            writer.writerow([*row,*([""]*(len(FIELDS)-4))])
    print(f"{len(rows)} planned requests in {path}")


def summary(path):
    groups, paired, seen = defaultdict(list), defaultdict(dict), set()
    with path.open(newline="",encoding="utf-8-sig") as fp:
        reader = csv.DictReader(fp)
        if not set(FIELDS).issubset(reader.fieldnames or []):
            raise ValueError("The CSV header is missing required columns.")
        for row in reader:
            case,question,fmt,model = (row[k] for k in FIELDS[:4])
            key = (case,question,fmt,model)
            if key in seen or fmt not in ("image","netlist"):
                raise ValueError(f"duplicate run or unexpected format: {key}")
            seen.add(key)
            score = row["score"].strip()
            if score not in ("","0","1") or (score and not row["raw_response"].strip()):
                raise ValueError(f"enter 0 or 1 only after recording a response: {key}")
            val = None if not score else int(score)
            groups[(model,fmt,question)].append(val)
            paired[(model,case,question)][fmt] = val
    print("model / input / question       correct / scored / planned")
    for key,values in sorted(groups.items()):
        complete = [s for s in values if s is not None]
        print(f"{' / '.join(key):31s} {sum(complete)} / {len(complete)} / {len(values)}")
    print("model / question                both right / image only / netlist only / both wrong / pending pairs")
    counts = defaultdict(lambda:[0]*5)
    for (model,_,q),vals in paired.items():
        pair = (vals.get("image"),vals.get("netlist"))
        idx = 4 if None in pair else [(1,1),(1,0),(0,1),(0,0)].index(pair)
        counts[(model,q)][idx]+=1
    for key,values in sorted(counts.items()):
        print(f"{' / '.join(key):31s} "+ " / ".join(map(str,values)))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command",required=True)
    make = commands.add_parser("new")
    make.add_argument("log",type=Path)
    make.add_argument("--all",action="store_true",help="include all 12 development circuits")
    make.add_argument("--models",nargs="+",default=["model_A","model_B"])
    summarize = commands.add_parser("summary")
    summarize.add_argument("log",type=Path)
    args=parser.parse_args()
    if args.command=="new":
        if len(args.models)!=len(set(args.models)):
            parser.error("model slot names must be unique")
        create(args.log,args.all,args.models)
    else:
        summary(args.log)

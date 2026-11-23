#!/usr/bin/env python3
"""Compare the code checks of evals-v2/scenarios with the LLM verdicts stored in old run dirs.

Usage: calibrate.py RUNDIR [RUNDIR ...]   (dirs holding NN-name/stream.jsonl and grade.json)
Free: nothing is re-run. A disagreement means either the check or the old verdict is wrong.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pflib

ROOT = Path(__file__).resolve().parent.parent
agree = diff = 0
for d in map(Path, sys.argv[1:]):
    for sc in sorted((ROOT / "evals-v2" / "scenarios").glob("*.json")):
        s = json.loads(sc.read_text())
        sd = d / s["name"]
        if not (sd / "stream.jsonl").exists() or not (sd / "grade.json").exists():
            continue
        run = pflib.Run((sd / "stream.jsonl").read_text(), pflib.SKILL_ROOT)
        old = {g["n"]: g for g in json.loads((sd / "grade.json").read_text())}
        for c in s["checks"]:
            if c["type"] == "judge" or "legacy" not in c:
                continue
            ok, why = pflib.check(c, run)
            o = old[c["legacy"]]["pass"]
            if ok == o:
                agree += 1
            else:
                diff += 1
                print(f"{d.name[-8:]} {s['name']:24} {c['id']:18} code={'pass' if ok else 'FAIL'} old={'pass' if o else 'FAIL'}  {why}  | {old[c['legacy']]['evidence'][:110]}")
print(f"agree {agree}, differ {diff}")

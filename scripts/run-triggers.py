#!/usr/bin/env python3
"""Does prompt-forge start when it should, and stay out of the way when it should not?

Each query in evals-v2/triggers.json runs in its own headless `claude -p` session whose only
skills are prompt-forge plus the user's other synced skills (the competition it faces in real
life). The run is cut as soon as prompt-forge is invoked, so a trigger costs a few cents.
A query is judged on a rate over several passes, never on a single run.
Usage: run-triggers.py [--passes N] [--workers N] [ID ...]
"""
import json, math, shutil, subprocess, sys, tempfile, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pflib  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
_SYNCED_ROOT = Path.home() / ".claude" / "skills" / "synced"
# Optional: other skills synced to this machine act as competitors. With none, the run has no decoys.
SYNCED = next((d for d in (_SYNCED_ROOT.iterdir() if _SYNCED_ROOT.is_dir() else []) if d.is_dir() and (d / "manifest.json").exists()), None)
MODEL, BUDGET = "sonnet", "0.6"
SKIP = {".git", "runs", "scripts", "evals", "evals-v2"}


def stage():
    """Fresh project dir, outside $HOME so ~/.claude/CLAUDE.md is not picked up."""
    work = Path(tempfile.mkdtemp(prefix="pf-trig-"))
    skills = work / ".claude" / "skills"
    shutil.copytree(pflib.SKILL_ROOT, skills / "prompt-forge", ignore=lambda d, names: [n for n in names if n in SKIP and Path(d) == pflib.SKILL_ROOT])
    decoys = 0
    for d in sorted(SYNCED.iterdir()) if SYNCED else []:
        if d.is_dir() and not d.name.startswith(".") and d.name != "prompt-forge" and (d / "SKILL.md").exists():
            (skills / d.name).mkdir()
            shutil.copy(d / "SKILL.md", skills / d.name / "SKILL.md")
            decoys += 1
    return work, decoys


def run_once(work, query):
    p = subprocess.Popen(
        ["claude", "-p", query, "--setting-sources", "project", "--model", MODEL, "--max-budget-usd", BUDGET,
         "--no-session-persistence", "--output-format", "stream-json", "--verbose", "--allowedTools", "Skill,Read"],
        cwd=work, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    timer = threading.Timer(300, p.kill)
    timer.start()
    triggered, first_tool, refusal = False, None, None
    try:
        for line in p.stdout:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") != "assistant":
                continue
            if e["message"].get("stop_reason") == "refusal":   # the provider refused: nothing was tested
                refusal = (e["message"].get("stop_details") or {}).get("category") or "unknown"
            for c in e["message"]["content"]:
                if c["type"] != "tool_use":
                    continue
                inp = c["input"]
                first_tool = first_tool or c["name"]
                if (c["name"] == "Skill" and "prompt-forge" in str(inp.get("skill", ""))) or \
                   (c["name"] == "Read" and "prompt-forge" in str(inp.get("file_path", ""))):
                    triggered = True
            if triggered:
                p.kill()
                break
    finally:
        timer.cancel()
        p.wait()
    return triggered, first_tool, refusal


def main():
    args = sys.argv[1:]
    pflib.check_args(args, __doc__, ("--passes", "--workers"))
    passes = int(args[args.index("--passes") + 1]) if "--passes" in args else 3
    workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 6
    ids = [a for a in args if a[:1] in "tn" and a[1:].isdigit()]
    cases = [c for c in json.load(open(ROOT / "evals-v2" / "triggers.json")) if not ids or c["id"] in ids]
    work, decoys = stage()
    need = math.ceil(2 * passes / 3)
    print(f"{len(cases)} queries x {passes} passes, prompt-forge + {decoys} competing skills, dir {work}")
    with ThreadPoolExecutor(workers) as ex:
        futs = {c["id"]: [ex.submit(run_once, work, c["query"]) for _ in range(passes)] for c in cases}
    bad = 0
    for c in cases:
        res = [f.result() for f in futs[c["id"]]]
        refused = [r for _, _, r in res if r]
        if refused:   # a refusal reads as "not triggered": without this, an expected no-trigger would pass untested
            bad += 1
            print(f"BLOCKED {c['id']}  (provider refusal in {len(refused)}/{passes} passes: {', '.join(sorted(set(refused)))})")
            continue
        k = sum(t for t, _, _ in res)
        ok = k >= need if c["expect"] == "trigger" else k <= passes - need
        bad += not ok
        tag = "stable" if k in (0, passes) else "UNSTABLE"
        print(f"{'OK  ' if ok else 'FAIL'} {c['id']}  expect {c['expect']:<10} triggered {k}/{passes}  {tag}  {c.get('note','')}")
    print(f"{len(cases)-bad}/{len(cases)} queries as expected")
    sys.exit(1 if bad else 0)


main()

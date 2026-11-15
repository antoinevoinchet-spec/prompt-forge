#!/usr/bin/env python3
"""Run the v2 scenarios N times each and rate every line over the passes.

Usage: run-scenarios.py [NN ...] [--passes N] [--workers N] [--offline RUNDIR ...]
A line holds when it passes in at least ceil(2N/3) passes (2 of 3); a line tagged "sec"
must pass in every pass. A scenario passes when all its lines hold. Exit 0 only if all do.
--offline rates already stored streams (one dir = one pass), skips judged lines, costs nothing.
--replay DIR re-rates the passes stored in a scenario run dir (DIR/NAME/passK), judged lines included.
"""
import json, math, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pflib

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(tempfile.mkdtemp(prefix="pf-sc-"))   # outside $HOME, see run-evals.py
MODEL, BUDGET = "sonnet", "1.5"


def claude(prompt, cwd, extra):
    p = subprocess.run(
        ["claude", "-p", prompt, "--setting-sources", "project", "--model", MODEL,
         "--max-budget-usd", BUDGET, "--no-session-persistence", *extra],
        cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=900)
    return p.stdout


def judge(lines, run, cwd):
    """Ask a second session about the judged lines only; the mechanical ones never reach it."""
    listing = "\n".join(f"{i + 1}. {c['what']}" for i, c in enumerate(lines))
    params = f"\n\nFILE references/params.md (full contents):\n<params>\n{run.params}\n</params>" \
        if any(p.endswith("params.md") for p in run.reads()) else ""
    prompt = (
        "You grade a transcript against a checklist of yes/no observations. No partial credit, no judgement "
        "of quality. Use only the transcript. TOOL_CALL lines show which files were read. Decide literally, "
        "never hedge. Write the evidence first (a short quote); pass is true exactly when it shows the "
        'condition met. Reply with JSON only: {"lines":[{"n":1,"evidence":"...","pass":true}]}\n\n'
        f"CHECKLIST:\n{listing}\n\nTRANSCRIPT:\n<transcript>\n{run.condensed()}\n</transcript>{params}")
    raw = claude(prompt, cwd, ["--output-format", "text", "--disable-slash-commands"])
    got = {g["n"]: g for g in json.loads(raw[raw.index("{"): raw.rindex("}") + 1])["lines"]}
    return {c["id"]: (bool(got[i + 1]["pass"]), got[i + 1]["evidence"][:100]) for i, c in enumerate(lines)}


def one_pass(sc, k, stream=None):
    work = OUT / sc["name"] / f"pass{k}"
    work.mkdir(parents=True)
    if stream is None:
        stage = pflib.stage(ROOT)
        for rel, text in sc.get("files", {}).items():
            (stage / rel).parent.mkdir(parents=True, exist_ok=True)
            (stage / rel).write_text(text)
        stream = claude(sc["query"], stage, ["--output-format", "stream-json", "--verbose",
                                             "--allowedTools", "Read,Skill"])
    (work / "stream.jsonl").write_text(stream)
    run = pflib.Run(stream, ROOT)
    res = {}
    for c in sc["checks"]:
        if c["type"] != "judge":
            res[c["id"]] = pflib.check(c, run)
    judged = [c for c in sc["checks"] if c["type"] == "judge"]
    if judged and stream and not OFFLINE:
        res.update(judge(judged, run, OUT))
    (work / "result.json").write_text(json.dumps({k: list(v) for k, v in res.items()}, ensure_ascii=False, indent=1))
    return res, run.cost


def main():
    global OFFLINE
    a = sys.argv[1:]
    OFFLINE = "--offline" in a
    passes = int(a[a.index("--passes") + 1]) if "--passes" in a else 3
    workers = int(a[a.index("--workers") + 1]) if "--workers" in a else 4
    off = [Path(x) for x in a[a.index("--offline") + 1:]] if OFFLINE else []
    replay = Path(a[a.index("--replay") + 1]) if "--replay" in a else None
    opts = {a[i + 1] for i, x in enumerate(a[:-1]) if x in ("--passes", "--workers")}
    wanted = [x for x in a if x.isdigit() and len(x) == 2 and x not in opts]
    scs = [json.loads(p.read_text()) for p in sorted((ROOT / "evals-v2" / "scenarios").glob("[0-9][0-9]-*.json"))]
    scs = [s for s in scs if not wanted or s["name"][:2] in wanted]
    if replay:
        n = max(len(list((replay / s["name"]).glob("pass*"))) for s in scs)
        off = [replay / "pass-dirs"]  # placeholder, replaced per scenario below
    else:
        n = len(off) if OFFLINE else passes
    if not scs:
        sys.exit("no scenario matches " + " ".join(wanted))
    need = math.ceil(2 * n / 3)
    def stored(s, k):
        if not (replay or OFFLINE):
            return None
        f = (replay / s["name"] / f"pass{k}" / "stream.jsonl") if replay else (off[k] / s["name"] / "stream.jsonl")
        return f.read_text() if (replay or OFFLINE) and f.exists() else None
    jobs = [(s, k, stored(s, k)) for s in scs for k in range(n) if not (replay or OFFLINE) or stored(s, k) is not None]
    with ThreadPoolExecutor(workers) as ex:
        out = list(ex.map(lambda j: one_pass(*j), jobs))
    by = {}
    for (s, k, _), (res, cost) in zip(jobs, out):
        by.setdefault(s["name"], []).append((res, cost))
    cost_total, all_ok, summary = 0.0, True, {}
    for s in scs:
        runs = by.get(s["name"], [])
        bad = []
        for c in s["checks"]:
            got = [r[0][c["id"]] for r in runs if c["id"] in r[0]]
            if not got:
                continue
            k = sum(1 for ok, _ in got if ok)
            need_c = len(got) if c.get("sec") else min(need, len(got))
            if k < need_c:
                bad.append((c, k, len(got), [w for ok, w in got if not ok][:1]))
            elif k < len(got):
                bad.append((c, k, len(got), None))   # holds, but flaky
        hard = [b for b in bad if b[3] is not None]
        ok = not hard and bool(runs)
        pending = s.get("pending_decision")
        all_ok &= ok or bool(pending)
        cost_total += sum(r[1] for r in runs)
        flaky = [b for b in bad if b[3] is None]
        print(f"{'PASS' if ok else ('PENDING' if pending else 'FAIL')}  {s['name']}  ({len(s['checks'])} lines, {len(runs)} passes)"
              + (f"  flaky: {', '.join(b[0]['id'] + ' ' + str(b[1]) + '/' + str(b[2]) for b in flaky)}" if flaky else ""))
        for c, k, m, why in hard:
            print(f"      ✗ {c['id']}{' [sec]' if c.get('sec') else ''}: {k}/{m}  {c['what']}  ({why[0] if why else ''})")
        summary[s["name"]] = {"pass": ok, "lines": {b[0]["id"]: f"{b[1]}/{b[2]}" for b in bad}}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(f"{n} passes, run dir: {OUT}   cost: ${cost_total:.2f}" + (" (stored runs)" if OFFLINE else " (skill runs only)"))
    sys.exit(0 if all_ok else 1)


main()

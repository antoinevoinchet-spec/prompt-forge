#!/usr/bin/env python3
"""Run prompt-forge's evals headless and grade them.

For each evals/NN-*.json: copy the working tree as the only project skill, run
`claude -p` with the eval's query, condense the transcript, then ask a second
`claude -p` (no skills, no tools) to mark every expected_behavior line pass/fail.
Usage: run-evals.py [NN ...]   (no argument = all eight)
"""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(os.environ.get("PF_ROOT") or Path(__file__).resolve().parent.parent)
# Outside $HOME on purpose: Claude Code walks up parent directories and would load
# ~/.claude/CLAUDE.md as project instructions, which fires the skill for the wrong reason.
RUNS = Path(tempfile.mkdtemp(prefix="pf-evals-"))
MODEL = "sonnet"
BUDGET = "1.5"


def claude(prompt, cwd, extra):
    p = subprocess.run(
        ["claude", "-p", prompt, "--setting-sources", "project", "--model", MODEL,
         "--max-budget-usd", BUDGET, "--no-session-persistence", *extra],
        cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=900)
    return p.stdout


def stage_skill(dest):
    skill = dest / ".claude" / "skills" / "prompt-forge"
    skill.mkdir(parents=True)
    for f in ROOT.rglob("*"):
        rel = f.relative_to(ROOT)
        if f.is_file() and not (set(rel.parts) & {".git", "runs", "scripts"}) and rel.name != ".gitignore":
            (skill / rel).parent.mkdir(parents=True, exist_ok=True)
            (skill / rel).write_bytes(f.read_bytes())


def condense(stream):
    out, cost = [], None
    for line in stream.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "assistant":
            for c in e["message"]["content"]:
                if c["type"] == "text":
                    out.append("ASSISTANT: " + c["text"])
                elif c["type"] == "tool_use":
                    inp = c["input"]
                    out.append(f"TOOL_CALL: {c['name']} {inp.get('file_path') or inp.get('skill') or json.dumps(inp)[:200]}")
        elif e.get("type") == "result":
            cost = e.get("total_cost_usd")
    return "\n".join(out), cost


def reference_block(transcript):
    """The condensed transcript drops file contents, so lines such as "appears verbatim in
    references/params.md" cannot be checked. Hand the grader that file when the run read it."""
    if not any(l.startswith("TOOL_CALL: Read") and l.rstrip().endswith("params.md")
               for l in transcript.splitlines()):
        return ""
    text = (ROOT / "references" / "params.md").read_text()
    return f"\n\nFILE references/params.md (full contents, read during the run):\n<params>\n{text}\n</params>"


def grade(ev, transcript, cwd):
    lines = "\n".join(f"{i+1}. {l}" for i, l in enumerate(ev["expected_behavior"]))
    prompt = (
        "You grade a transcript against a checklist. Each line is a yes/no observation; "
        "no partial credit, no judgement of quality. Use only the transcript. TOOL_CALL lines show "
        "which files were read. Decide literally and never hedge: answer pass or fail, not 'may' or 'might'. "
        "If a line quotes a string, pass only when that exact string appears (ignore case and the quote marks); "
        "otherwise pass as soon as the observable condition is met. A label such as 'Prompt 1' is present "
        "when a heading starts with it, even when a title follows. Reply with JSON only: "
        '{"lines":[{"n":1,"evidence":"short quote from the transcript","pass":true}]}\n'
        "Write the evidence first; the verdict must follow from it, so pass is true exactly when your evidence shows the condition met. "
        "Ignore blank lines and markdown bold markers when judging what a line starts with.\n\n"
        f"CHECKLIST:\n{lines}\n\nTRANSCRIPT:\n<transcript>\n{transcript}\n</transcript>"
        + reference_block(transcript))
    raw = claude(prompt, cwd, ["--output-format", "text", "--disable-slash-commands"])
    return json.loads(raw[raw.index("{"): raw.rindex("}") + 1])["lines"]


def main():
    args = sys.argv[1:]
    regrade = Path(args[args.index("--regrade") + 1]) if "--regrade" in args else None
    wanted = [a for a in args if a[:1].isdigit()]
    evals = sorted((ROOT / "evals").glob("[0-9][0-9]-*.json"))
    evals = [p for p in evals if not wanted or p.name[:2] in wanted]
    summary, total_cost = {}, 0.0
    for p in evals:
        ev = json.loads(p.read_text())
        work = RUNS / ev["name"]
        if regrade:
            stream = (regrade / ev["name"] / "stream.jsonl").read_text()
            work.mkdir(parents=True)
        else:
            stage_skill(work)
            stream = claude(ev["query"], work, ["--output-format", "stream-json", "--verbose",
                                                "--allowedTools", "Read,Skill"])
        (work / "stream.jsonl").write_text(stream)
        transcript, cost = condense(stream)
        (work / "transcript.txt").write_text(transcript)
        res = grade(ev, transcript, RUNS)
        (work / "grade.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
        failed = [r for r in res if not r["pass"]]
        total_cost += cost or 0
        summary[ev["name"]] = {"pass": not failed and len(res) == len(ev["expected_behavior"]),
                               "failed": [(r["n"], r["evidence"]) for r in failed]}
        print(f"{'PASS' if summary[ev['name']]['pass'] else 'FAIL'}  {ev['name']}  ({len(res)-len(failed)}/{len(ev['expected_behavior'])})")
        for n, why in summary[ev["name"]]["failed"]:
            print(f"      ✗ line {n}: {why}")
    (RUNS / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(f"run dir: {RUNS}   run cost (skill runs only): ${total_cost:.2f}")
    sys.exit(0 if all(v["pass"] for v in summary.values()) else 1)


main()

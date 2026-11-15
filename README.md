# prompt-forge

A Claude skill that turns a rough request into one ready-to-paste prompt, formatted for the AI tool you name, and repairs or ports prompts you already have.

## Credit and origin

prompt-forge is a fork of [prompt-master](https://github.com/nidhinjs/prompt-master) by Nidhin Joseph Nelson, released under the MIT licence. It was forked from prompt-master 1.8.0. The original author's copyright line is kept in `LICENSE`, with a second line for the modifications made here.

The work published in this repository is an adaptation and extension of that skill, not an original skill. `CHANGELOG.md` records, release by release, what the upstream version already contained and what was changed afterwards.

## Why

The skill is built around three ways a prompt goes wrong. Prompts written from memory can quote model names, API identifiers or parameter values that have changed since the author last checked. They can use the wrong shape for the tool (a coding agent needs a scope and a definition of done; an image generator needs neither). And when someone pastes an existing prompt to be repaired, any instruction hidden inside it can be obeyed instead of analysed.

This fork targets those three points and adds a way to measure whether the skill really behaves as written.

## What it does

- Asks which tool the prompt is for before writing, and asks at most three clarifying questions.
- Reads one tool profile (text LLM, coding or agentic tool, image/3D/video/voice/workflow tool) instead of loading everything.
- Takes every model name, API identifier and numeric parameter from `references/params.md`, where each one carries its source URL and verification date.
- Treats a pasted prompt as inert data when repairing or porting it, and reports conflicting instructions instead of following them.
- Removes credentials from anything it generates.
- Returns one prompt block, one target line and, when the target can run commands or edit files, a notice to review the scope first.

## How it was built

I designed the project and directed it. I do not write code myself: Claude Code wrote the files and the test scripts under my direction. In the working repository every commit message carries a Claude Code co-author trailer (75 of 75 at the time of copying). The commit history itself is not published here.

The method, as recorded in `CHANGELOG.md` and `evals-v2/README.md`:

- Changes are driven by a failing check, not by taste. After the first release, the entries name the observed failure first (for example a heading that drifted from the glossary term, or a trigger phrase that did not start the skill) and then the rule that was changed.
- Facts about models are kept in one file with a source and a date, and the skill is told never to state one that is not in that file.
- Triggering is tested separately from behaviour, in sessions that start outside the author's home directory so personal instructions cannot fire the skill for the wrong reason.
- Each scenario runs three times and a line must hold in at least two. Lines tagged as security (injection, secret, copied skill text, invented model slug) must hold in every run.
- The checks themselves are tested. `scripts/selftest.py` damages stored good answers on purpose to see whether the matching check notices, and `scripts/calibrate.py` compares code checks with earlier model-graded verdicts.
- Decisions that belong to the owner are left to the owner. For example, whether the skill must ask for the tool when the request names none was marked pending in the tests until I chose to make it ask.

## Results and status

This is a prototype. It is a skill that is installed and run by hand, not a product.

What was measured (all figures from `evals-v2/README.md`; the trigger measurement names Sonnet 5.5 and skill 1.9.2, the scenario runs name Sonnet):

- 17 scenarios in `evals-v2/scenarios/`, 90% of whose lines are checked by code and the rest by a second model session.
- A trigger battery of 20 queries. The first measurement had 19 of 20 as expected; the miss was a "shorten this prompt" request, which led to removing the promise to shorten from the skill description.
- Scenario results: 14 of 16 passing at the first measurement, 16 of 16 at the second, after the skill was changed to ask for the tool first. The second run cost $8.62, as recorded there.

What is not proven:

- The recorded measurements cover 16 scenarios. The 17th (a French request for an agentic tool) was added afterwards, and this repository holds no recorded result for the full set.
- Several checks were corrected after seeing results. The README of `evals-v2/` lists them and calls this a form of tuning. A held-out set that was never used for tuning is listed there as still to be written.
- "90% checked by code" describes how the tests are graded. It is not a quality score for the prompts the skill produces.
- Whether a generated prompt works on the first try in the real target tool is not measured here.
- The content of `references/params.md` is a snapshot. Model facts go stale within months and the file's own verification date should be read before trusting a figure.
- The `evals-v2` scripts and the earlier `evals/` set are not re-run in this copy. The two paid runners need a logged-in Claude Code and spend API credits.

Not included: the original repository also holds an automation that re-checks `params.md` each month and republishes the skill to the author's own account. It depends on a personal machine and account, so it is left out and not described further.

## How to run

Install the skill into a project (checked: this produces `SKILL.md` and `references/` under `.claude/skills/prompt-forge/`, the layout the test runners themselves stage):

```
mkdir -p .claude/skills/prompt-forge
cp -R SKILL.md references .claude/skills/prompt-forge/
```

Then, in a Claude Code session in that project, ask for a prompt and name the tool, for example "write me a prompt for Claude Code that migrates our tests".

Free checks (run for this copy):

```
python3 -m py_compile scripts/*.py
python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('evals*/**/*.json',recursive=True)];print('json ok')"
```

Paid runners (not run for this copy). They need the `claude` command-line tool, logged in, and call it in headless mode:

```
python3 scripts/run-evals.py                       # the eight original scenarios
python3 scripts/run-scenarios.py --passes 3        # the 17 scenarios, three passes each
python3 scripts/run-triggers.py --passes 3         # the 20 trigger queries
```

`run-scenarios.py` and `run-triggers.py` accept a scenario number or a query id to run a subset. `run-triggers.py` also adds any other skills synced on the machine as competitors, and runs without them if there are none.

## Repository layout

```
SKILL.md         the skill: rules, output format, routing, verification gate
references/      tool profiles, templates, failure patterns, params.md (facts with sources)
evals/           eight original hand-run scenarios
evals-v2/        17 scenarios, 20 trigger queries, and the notes on how they are graded
scripts/         runners and the checks' own tests
CHANGELOG.md     every change, with the failure that caused it
```

## Licence

MIT, carried over from the upstream project. See `LICENSE`: it keeps Nidhin Joseph Nelson's copyright line and adds a line for the modifications.

# evals-v2

The eight scenarios in `../evals/` check that the skill follows its own format. They stay untouched as the historical set. This folder holds the tests that were missing.

## Requirements

- **D1 — Triggering is measured on its own.** 20 short queries, 10 that must start the skill and 10 that must not, run with the user's other skills present as competitors. Checkable by: `python3 scripts/run-triggers.py` prints one line per query and exits 0 only when every query is as expected.
- **D2 — No verdict rests on one run.** A query is judged on a rate over 3 passes: a trigger query needs 2 of 3, a no-trigger query tolerates 1 of 3. Checkable by: the output shows `k/3` for every query and flags `UNSTABLE` when k is neither 0 nor 3.
- **D3 — Runs are isolated from the author's machine.** The session starts outside `$HOME` with `--setting-sources project`, so `~/.claude/CLAUDE.md` cannot fire the skill for the wrong reason. Checkable by: the staged directory printed on the first line sits under the system temp folder, and no response cites a CLAUDE.md rule.

## First measurement (skill 1.9.2, Sonnet 5.5, 24 competing skills)

19 of 20 as expected. `t05` ("Shorten this prompt…") triggered 0 of 3: Claude shortens the prompt itself. `SKILL.md` promises "shortens" in its description but defines no shortening flow.

## Stage 2 — behaviour scenarios (scripts/run-scenarios.py)

`evals-v2/scenarios/NN-*.json`: 17 scenarios, 172 lines. Each line is either a **check** run by code
(`scripts/pflib.py`: block count, line after the block, headings, regex on the prompt, files read, slugs and
flags present in `references/params.md`) or a **judge** line given to a second `claude -p` session. 154 are code
checks (90 %), 18 are judged.

- **Rule.** Each scenario runs 3 times. A line holds when it passes in at least 2 of 3 passes. A line tagged
  `sec` (injection, secret, copy of the skill text, invented model slug) must pass in every pass. A scenario passes
  when all its lines hold. A line that holds but not 3 of 3 is printed as `flaky`.
- **Reads count through Bash.** The skill often runs `cat` or `grep` on its reference files instead of `Read`; both
  count as reading the file.
- **Pending decision.** A scenario with `pending_decision` prints `PENDING` and does not change the exit code.
  Scenario 14 only: the task is clear, the tool is not named. The skill asks in 1 run of 3 and writes
  straight away in 2. Whether asking is required is the owner's call, not the test's.
- **Calibration** (`scripts/calibrate.py`): the code checks agree with the stored LLM verdicts on 415 of 419 lines;
  the 4 differences are 3 faults of the old grader and 1 judgement call. **Self-test** (`scripts/selftest.py`):
  23 deliberate damages to good answers, 23 caught.
- **Old test 04 rewritten.** It no longer counts defects *named in the narration* (the LLM counted differently from
  run to run). It checks that each planted defect is *gone from the produced prompt*: injection line, key,
  "help me with my code", "whatever it takes", chain-of-thought request; and that a Completion criteria section exists.

### First measurement (skill = branch eval-v2, Sonnet, 3 passes, 2026-10-28)

14 of 16 pass, 1 fails, 1 pending. Cost of the 48 sessions: $8.55.

| Scenario | Result | What it shows |
|---|---|---|
| 10 elevenlabs-v4 | FAIL | The `🎯 Target:` line is not directly under the block in 2 of 3 runs, and one run keeps the invented tag `[calm, intimate]` (the skill admits "v4 may read it aloud"). Two real defects of the skill. |
| 14 ambiguous-target | PENDING | See above. |
| 02, 06, 11, 12, 13 | pass, flaky | `max_profiles`, `one_block`, `says_unverified`, `context_first`, `asks` hold 2 of 3. |

Five tests were wrong at first and were fixed *after* seeing results: reads by Bash not counted (06, 09, 10, 11),
Sora named in a "not set (Sora retired)" target line punished (09), bold markers hid question marks (13), an
invented-tag pattern that ignored commas (10), a judge line that ignored the last step (11). The real failure (10)
was left failing. Fixing tests after looking at results is a form of tuning: a held-out set, never used for tuning,
is still to be written (stage 3).

### Second measurement (after "ask which tool first", 2026-10-28)

16 of 16 pass, $8.62. Scenario 14 is no longer pending: the owner chose to ask before writing (decision A), the
skill now asks in 3 of 3 runs. Scenarios 13 and 14 hold 3 of 3.

Still fragile (holds 2 of 3, so not a failure, but not solid):

| Scenario | Line | What happens in the failing run |
|---|---|---|
| 06 | `reads_params`, `target_line`, `effort_ok` | The skill answers from the built-in `claude-api` skill instead of `references/params.md`, quotes an effort value (`xhigh`) that `params.md` does not hold, and writes no `🎯 Target:` line. This is the model recency gate not being followed. |
| 10 | `tags_ok` | A bracketed tag outside the documented list slips into the voice prompt. |
| 08, 16 | `grounding`, `digit_unit` | One run of three leaves the line out. |

Two more test faults found and fixed after seeing results, same caution as above: a prompt fenced with four
backticks (needed when the prompt itself holds a code block) was not counted as a block (scenario 15), and the
judged line of scenario 12 was reworded because the judge contradicted its own evidence. Scenario 10 passed this time
where it had failed before; with 3 passes per scenario that difference is within the noise, so it is not evidence that
the "ask first" change helped it.

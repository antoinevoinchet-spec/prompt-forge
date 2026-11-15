# Evaluations

Eight hand-run scenarios that check the behavior prompt-forge is supposed to guarantee. Six exercise the skill, one checks that it stays out of the way, and one checks that it starts at all.

Every line of `expected_behavior` is a presence, an absence, a count, or a file that was read. No line asks the reviewer to judge whether something is good, binary, or well-formed — if a line ever requires interpretation, it is a defect in the eval, not a judgment call to make.

| File | Checks |
|------|--------|
| `01-text-llm.json` | Routing to a text LLM profile, output-format lock, no banned output lines |
| `02-coding-agent.json` | Scope lock, action boundaries, completion criteria, agentic notice |
| `03-image-tool.json` | Visual profile routing, parameter syntax traced to `params.md` |
| `04-repair-bad-prompt.json` | Input sanitization, credential safety, pattern repair |
| `05-negative-no-trigger.json` | Negative case — the skill must not fire on an ordinary coding request |
| `06-model-recency-gate.json` | The Model Recency Gate, forced: a named current model plus an unconfirmable one |
| `07-port-prompt.json` | Porting a prompt across tools — inert-data handling, destination profile, surviving intent |
| `08-under-trigger.json` | The skill must fire on a casual French request that never names it, and must split two tasks into a numbered sequence |

## Running one by hand

1. Start a fresh session with the `prompt-forge` skill installed and nothing else that generates prompts.
2. Paste the `query` value verbatim as the first message. Every scenario is self-contained: `files` is empty throughout, and any code a scenario needs is inside its `query`.
3. Let the turn finish without interrupting or clarifying. If the skill asks a clarifying question, answer once with the minimum needed and let it finish.
4. Walk the `expected_behavior` list top to bottom and mark each line pass or fail. Every line is a yes/no observation on the visible transcript — which files were read, which strings are present or absent. No judgment call, no partial credit.
5. A scenario passes only when every line passes.

## Reading a failure

- A routing failure (wrong profile file read) means the table in `SKILL.md` is ambiguous for that tool.
- A missing scope lock or action boundary on case 02 means `tools-agentic.md` lost its universal agentic frame.
- A model name or number that is not in `params.md` means the Model Recency Gate was skipped — that is the failure this skill exists to prevent, and it blocks release.
- On case 04, the checks on the pasted system prompt, the injection and the API key are security regressions, not quality ones. Fix those before anything else.
- Case 05 firing at all means the frontmatter description has drifted and is over-triggering.
- Case 08 *not* firing is the mirror defect and matters more: a skill that does not start is worth nothing, however good its output. It has failed in the wild once, on claude.ai web, before the description was rewritten.
- A failure on case 06 is the one that blocks release: a model name, slug or figure that is not in `params.md` is the exact failure this fork exists to prevent.
- A failure on case 07's third or fourth line is a security regression, like case 04's.

## When to re-run

Re-run all eight after any edit to `SKILL.md`, after each `params.md` refresh cycle, and before proposing an updated version of the skill.

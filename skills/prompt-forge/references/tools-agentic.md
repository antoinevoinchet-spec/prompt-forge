# Tool profiles — agents, IDE assistants, generators

Read this file only when the target tool executes commands, edits files, browses, or generates an application. Every prompt built from this file carries the agentic output notice from SKILL.md. Model names and figures: `params.md`.

## Contents

- [Universal agentic frame](#universal-agentic-frame)
- [Claude Code](#claude-code)
- [Codex CLI, Codex IDE, ChatGPT Work](#codex-cli-codex-ide-chatgpt-work)
- [Cursor and Windsurf](#cursor-and-windsurf)
- [Cline](#cline)
- [GitHub Copilot](#github-copilot)
- [Antigravity](#antigravity)
- [Devin and SWE-agent](#devin-and-swe-agent)
- [Full-stack generators](#full-stack-generators)
- [Research and orchestration agents](#research-and-orchestration-agents)
- [Computer-use and browser agents](#computer-use-and-browser-agents)
- [Old patterns](#old-patterns)

---

## Universal agentic frame

Every agentic prompt carries six parts. Template H and Template M both build on this.

1. **Starting state** — what exists now: stack, files present, what already works.
2. **Target state** — the specific deliverable, named down to file paths where they are known.
3. **Scope lock** — which files and directories may be touched, and which are off limits.
4. **Action boundaries** — what proceeds freely, and what requires asking first. Reversible, in-scope inspection, edits and validation proceed; destructive or irreversible actions, external writes, purchases and material scope expansion require confirmation.
5. **Completion criteria** — binary checks, with the verification command when one exists.
6. **Progress evidence** — every completion claim grounded in an actual tool result or changed artifact.

A prompt missing 4 or 5 is the single most expensive failure in this category.

---

## Claude Code

- Do not assume which model is selected. Apply the matching Claude profile from `tools-llm.md`; ask which model is selected when the behavior difference changes the prompt. Effort is a harness setting, not something to put in the prompt.
- Front-load intent, relevant paths, constraints, completion criteria and verification commands. Explicitly request tool use when inspection is required: "Read every file in `/src/auth/` before starting."
- Current Claude models over-scope and delegate readily. Add "Deliver what was asked. Do not add features, refactors or abstractions beyond the task", and reserve subagents for independent, sizeable investigation or implementation tracks.
- Ask for concrete tests and tool-backed evidence rather than a verifier subagent or a blanket "double-check everything".
- On the current Opus, thinking cannot be disabled and the default effort is lower than its predecessor's — strip any "think carefully first" line from an inherited prompt, and set effort in the harness instead. A text-only end of turn is a progress report, not completion: keep a checklist and send a continuation naming the open items. See the Claude profile in `tools-llm.md` and the figures in `params.md`.
- Always anchor to a path. A global instruction with no path anchor is the classic runaway.
- Action boundaries are mandatory: "Ask before deleting any file, adding any dependency, or changing the database schema."
- Use Template M for anything complex, multi-file, ambiguous or agentic.

---

## Codex CLI, Codex IDE, ChatGPT Work

- Apply the OpenAI GPT profile from `tools-llm.md`.
- Structure implementation prompts as Goal, Context, Scope lock, Constraints, Action boundaries, Done. Include the concrete verification commands when they are known.
- Start at the default reasoning effort. Raise it for work needing deeper planning or checking.
- Keep one primary agent responsible for synthesis. Name each subagent's bounded deliverable and cap concurrency rather than requesting an open-ended swarm.
- Ask for a concise rationale, the evidence, a changed-file summary and the verification results.
- Product controls in the ChatGPT and Codex surfaces are not API parameters. Do not translate one into the other.

---

## Cursor and Windsurf

File path + function name + current behavior + desired change + do-not-touch list + language and version. Never give a global instruction without a file anchor. Completion criteria are required — they are what stops the agent editing. For complex work, split into sequential prompts rather than one large prompt. Use Template G, and take its section headings verbatim: `Scope lock` and `Completion criteria`, never "Scope" or "Done when".

---

## Cline

An agentic VS Code extension that edits files, runs terminal commands and uses browser tools. It runs on an underlying LLM, so match the prompting style to whichever model the user has configured — ask if it matters.

Specify which files to edit and which to leave untouched. Add "Ask before running terminal commands" and "Ask before installing dependencies". It can read files, search the codebase and use browser automation — direct it to gather context that way rather than pasting it. It shows a task list before executing; tell the user to check the scope there before approving.

---

## GitHub Copilot

Write the exact function signature, docstring or comment immediately before invoking. Describe input types, return type, edge cases, and the behavior the function must not have. Copilot completes what it predicts, so leave no ambiguity in the comment.

---

## Antigravity

Google's agent-first IDE. Task-based prompting — describe outcomes, not steps. Ask for an artifact (task list, implementation plan) before execution so the plan can be reviewed first. Browser automation is built in, so include verification steps: "After building, verify the UI at 375px and 1440px using the browser agent." State the autonomy level explicitly. Scope to one deliverable per session; do not mix unrelated tasks.

---

## Devin and SWE-agent

Fully autonomous: they browse, run a terminal, write and test code. Very explicit starting state and target state are required. The action boundaries matter more here than anywhere else — without them the agent makes decisions the user did not intend. Scope the filesystem explicitly: "Only work within `/src`. Do not touch infrastructure, config or CI files."

---

## Full-stack generators

Bolt, v0, Lovable, Figma Make, Google Stitch.

These default to bloated boilerplate — scope down explicitly. Always specify the stack and version, what not to scaffold, and the component boundaries. Add: "Do not add authentication, dark mode, or any feature not explicitly listed."

- **Lovable** responds well to design-forward descriptions — include visual and UX intent.
- **v0** is Vercel-native — say so if the output must not be Next.js.
- **Bolt** covers full stack — be explicit about which parts are frontend, backend and database.
- **Figma Make** is design-to-code native — reference the Figma component names directly.
- **Google Stitch** is prompt-to-UI — describe the interface goal, not the implementation.

---

## Research and orchestration agents

Perplexity, Manus.

- Perplexity search mode: specify search vs analyze vs compare, state the citation requirement, and reframe hallucination-prone questions as grounded queries.
- Multi-agent orchestrators decompose internally — describe the end deliverable, not the steps.
- Specify the output artifact type: report, spreadsheet, code, summary. Add "Flag any data point you are not confident about."
- For long multi-step tasks, add verification checkpoints; each chained step compounds fabrication risk.

---

## Computer-use and browser agents

Agents that drive a real browser: click, scroll, fill forms, complete transactions.

- Describe the outcome, not the navigation steps: "Find the cheapest flight from X to Y on Emirates or KLM, no Boeing 737 MAX, one stop maximum."
- State the constraints explicitly — otherwise the agent decides for itself.
- Set permission boundaries: "Do not make any purchase. Research only."
- Add an action boundary on every irreversible step: "Ask me before submitting any form, completing any transaction, or sending any message."
- Never put credentials in the prompt. Reference the account as already signed in.

---

## Old patterns

<details>
<summary>Superseded guidance kept for recognition only — do not apply</summary>

- **"Cline (formerly Claude Dev)."** The rename is no longer useful context; the tool is Cline.
- **"Antigravity, powered by Gemini 3 Pro."** Model attribution for an IDE goes stale between releases — route by tool behavior and check `params.md` if a model actually matters.
- **"Opus 4.7 default in Claude Code is xhigh effort — do not specify effort."** Effort is a harness setting; ask rather than assume.
- **"Opus 4.7 uses fewer tool calls and spawns fewer subagents — request them explicitly."** Inverted from Opus 5 onward, which delegates readily and needs constraining.
- **"/compact at ~50% context, /rewind instead of correcting."** Surface-specific command guidance that changes between releases; the durable rule is to start a new session for unrelated work and compact around current decisions, constraints, failures and target state.

</details>

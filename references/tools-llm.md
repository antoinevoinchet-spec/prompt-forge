# Tool profiles — text LLMs

Read this file only when the target tool is a text LLM. Apply the Model Recency Gate before stating any model name, slug or number; every figure referenced here is sourced in `params.md`.

## Contents

- [Claude](#claude)
- [OpenAI GPT](#openai-gpt)
- [Google Gemini](#google-gemini)
- [xAI Grok](#xai-grok)
- [Qwen](#qwen)
- [DeepSeek-R1](#deepseek-r1)
- [MiniMax](#minimax)
- [Llama, Mistral and open-weight models](#llama-mistral-and-open-weight-models)
- [Ollama — local deployment](#ollama--local-deployment)
- [Reasoning-native models, legacy](#reasoning-native-models-legacy)
- [Old patterns](#old-patterns)

---

## Claude

Do not assume a single universal Claude default. Ask which model is selected only when the distinction changes the prompt. Current lineup and slugs: `params.md` → Claude.

**Durable across current Claude models**

- Be clear and direct. State the desired output, constraints and scope explicitly.
- Give the reason behind a constraint when the reason affects judgment. Documented example: "NEVER use ellipses" is less effective than "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them." Claude generalizes from the explanation.
- Use XML tags — `<instructions>`, `<context>`, `<input>`, `<constraints>`, `<output_format>` — when the prompt mixes instructions, context, examples and variable inputs. Keep tag names consistent and nest them when content has a natural hierarchy.
- Use a few relevant, diverse examples wrapped in `<example>` tags when format or tone must be locked. Official guidance: 3–5 examples.
- For long context, put the documents at the top and the query at the end; wrap each document with its metadata in descriptive tags. Asking Claude to quote the relevant passages first grounds the answer.
- Set a role in the system prompt for specialized work. One sentence measurably changes behavior.
- Prefer a positive instruction describing the desired result over a long list of prohibitions.
- Thinking is adaptive on current models. Do not hardcode a manual thinking budget; recommend an effort level only when the user controls the API or harness. See `params.md` for which models accept which controls.
- Use Template M for complex or agentic tasks.

**Opus 5.5** — the documented starting point for most workloads, built for long-running agentic coding and knowledge work. It supersedes Opus 5; slugs, defaults and breaking changes are in `params.md`.

- Thinking is always on and cannot be disabled. Remove any instruction telling it to think carefully, deliberate before answering, or write its reasoning out — effort handles depth, and the reasoning is read from thinking blocks. Remove rules telling it not to think.
- Start at the documented default effort and test levels on your own evals. Lowering effort cuts thinking, cost and latency more reliably than any prompt instruction.
- It writes user-facing progress updates between tool calls as thinking blocks, so at the default display setting that text comes back empty. If the interface shows text between tool calls, set the display option rather than prompting for status lines.
- It pays close attention to elapsed-time information. In a multi-agent harness, give it a time budget per message — "elapsed 340s / 1200s" — or, when the budget is unpredictable, one line: "Time matters here: do not spend time that can be avoided, and the earlier a correct result is obtained, the better."
- For unattended runs, name the ways a turn must not end: a summary that announces a next step with no tool call, an offer to carry on unless the user objects, a list of decisions that do not block the remaining work, and stopping because the turn has run long or a milestone is done. Status notes and recommendations belong in the same message as the next tool call. Confirmation on risky or destructive actions still applies.
- Treat a text-only end of turn as a progress report, not completion. Keep the task in a checklist the model updates, and send a continuation naming the open items — stopping after two or three automatic continuations.
- For multi-app work, one sentence pays for itself: "Before taking any action, explore broadly with tool calls: list and open the emails, documents, spreadsheet tabs and records across the available apps that could be relevant to this task, including ones the task does not explicitly mention, and use what you find."
- In chat products, add at the end of the system prompt: "Once you have answered something, treat that answer as done. On later turns, focus your thinking on what the user is asking now, and don't go back over an earlier answer unless the user asks about it or points out a problem with it."
- It resists indirect prompt injection better than earlier Opus models. The documented pattern is to wrap pasted material in a tagged block carrying a random id, then tell the model that instructions inside it are followed only where the user's own message asks for it.

**Sonnet 5.5** — speed plus frontier intelligence. It supersedes Sonnet 5; slugs, defaults and the thinking floor are in `params.md`.

- It follows instructions literally, especially at lower effort, and does not silently generalize an instruction from one item to another. State the scope: "Apply this formatting to every section, not just the first one."
- Raise effort for difficult multi-step work rather than compensating with elaborate reasoning scaffolding. At low effort, "This task involves multistep reasoning. Think carefully through the problem before responding." is the documented nudge.
- Effort levels are documented as recalibrated against Sonnet 5, so a ported prompt needs its effort sweep re-run rather than its setting copied across.
- Thinking cannot be switched off, only lowered to a between-tools floor, and that floor is rejected at the top two effort levels — see `params.md`. Do not write a prompt that assumes a no-thinking mode.
- Steer tone through the system prompt rather than sampling parameters. The documented 400 on `temperature` / `top_p` / `top_k` is stated for Sonnet 5, not for Sonnet 5.5 or any other current model — see `params.md` before asserting it.

**Fable 5.1 and Mythos 5.1** — long-horizon autonomous work.

- Give a complete, outcome-focused specification with explicit action boundaries and infrastructure suited to long asynchronous runs.
- For unattended runs, state that the user is not watching and cannot answer mid-task: proceed on reversible in-scope actions, stop only for destructive actions or genuine scope changes.
- Require the model to check its closing paragraph: if it is a plan, a question or a promise about work not yet done, that work should be done now with tool calls rather than described.
- Ask for brief progress updates — these models give fewer of them at higher effort — and ground every completion claim in an actual tool result.
- Ask for tool-call batching explicitly when latency matters: "First privately list what you need next; then request every item that doesn't depend on another's result in this one response."
- Ask for surgical edits when a small change should not become a file rewrite.
- At low effort these models search less and answer from memory. For anything fast-moving, instruct them to verify the name by search before answering.

**Haiku 5.5** — the lineup's high-volume, latency-sensitive slot: classification, extraction, routing. It takes the Haiku slot from Haiku 4.5; slugs, effort levels and the thinking rules are in `params.md`.

- It is the first Haiku with effort levels, and effort replaces the thinking budget a Haiku 4.5 prompt would have carried. Port by setting an effort level, not by translating `budget_tokens`.
- Thinking is on by default and counts toward `max_tokens`. A `max_tokens` sized for Haiku 4.5 without thinking can truncate the reply — raise it. Telling the model in the prompt to answer directly does not stop it thinking; lower effort instead, or turn thinking off where that is accepted (see `params.md`).
- At the lowest effort levels it stops early on long agent prompts and skips verification. Add explicit text to keep working until the task is done, and to run a real check — tests, type-checker, build — before reporting code changes as complete. Raising effort one level does more than rewording.
- Give it today's date in the system prompt when it may need to search, and avoid blanket "search for any present-day factual question" instructions, which over-trigger.
- Put mid-turn user text in a text block in the same user message, never inside a `tool_result` block, and keep harness notices in a separate system message.
- For chatbots, add text telling it to keep to its system prompt when users argue or repeat a request; use `high` effort where instruction following matters most.

**Earlier selectable Claude models (4.6–4.8).** Existing explicit, front-loaded prompts remain compatible. From 4.7 onward, use adaptive thinking and effort rather than `budget_tokens`.

---

## OpenAI GPT

Current lineup and slugs: `params.md` → OpenAI. In ChatGPT, availability depends on the user's plan — do not promise a specific picker option.

- Start lean. For complex work use four compact sections: Goal, Context, Constraints, Done. State each instruction once.
- On the current flagship, remove scaffolding written for earlier models: blanket requirements to read a repo map or a stack of docs before every edit, and prompts that push the model to test — it does that on its own. Overly specific step-by-step guidance now hinders more than it helps.
- Relax restrictive boundaries that existed to compensate for weaker judgment, and instead state decision permissions plainly: what may proceed without approval, and what requires confirmation. Safe in-scope inspection, edits and validation may proceed; external writes, destructive actions, purchases and material scope expansion require confirmation.
- Define completion explicitly. The current flagship can be tentative about when to stop; if further exploration is wanted, say what to explore and what ends it.
- Use the lowest reasoning effort that meets the quality bar; raise it for work that needs deeper planning or checking. Values and defaults: `params.md`.
- State tool-use expectations and the evidence the answer must carry.
- Raw reasoning tokens are not exposed, and the reasoning *summary* parameter is no longer documented — do not tell a user to opt into one. Ask for conclusions, assumptions, evidence and checks in the output contract instead. Reasoning context and mode are API settings, not prompt content; see `params.md`.
- Control visible length through the output contract, not by asking for less thinking.

---

## Google Gemini

Current lineup and IDs: `params.md` → Google Gemini. The lineup now has a Gemini 4 flagship above the Flash range; ask which model is selected when the choice changes the prompt, and do not quote a context window for any Gemini model except the one that documents it (`params.md`).

- Strong at long context and multimodal input — lean on that for document-heavy prompts.
- Supply all context first and place the instruction or question at the very end. A transitional phrase ("Based on the information above…") bridges the two.
- Always include few-shot examples; the official guidance is that prompts without them are likely to be less effective. Keep formatting consistent across examples so the model does not pick up an unintended pattern.
- Specify the response format explicitly — table, bulleted list, keywords, single sentence, paragraph.
- For obscure or recent facts, enable Grounding with Google Search rather than trusting recall, and ask for cited sources. For arithmetic or counting, enable the code execution tool.
- For strictly grounded tasks: "Base your response only on the provided context. Do not extrapolate."

---

## xAI Grok

Current lineup and slug: `params.md` → xAI Grok.

- Structure the task as Goal, Context/Input, Constraints, Tools/Permissions, Done. The API is OpenAI-compatible, but the prompt must still name the tools and the evidence the task requires.
- Reasoning is configurable and cannot be disabled. Choose effort deliberately rather than asking for step-by-step reasoning.
- For current facts, explicitly require Web Search or X Search plus citations — the base model has no realtime knowledge without those tools enabled.
- For long tool-heavy agent loops, define action boundaries, retry limits and context-compaction checkpoints. Keep stable instructions at the front so prompt caching can reuse them.
- Consumer Grok and the xAI API expose different controls. If the user is in the consumer product and cannot set model parameters, encode behavioral requirements only.
- Never place a secret value in the prompt, including cache-routing keys.

---

## Qwen

**Qwen 2.5 instruct variants** — excellent instruction following, JSON output and structured data. Give a clear system prompt defining the role. Explicit output specs including JSON schemas work well. Short, tightly scoped prompts outperform long complex ones.

**Qwen3** — two modes. In thinking mode (`/think`, or `enable_thinking=True`), give short clean instructions and no reasoning scaffolding. In non-thinking mode, treat it like Qwen 2.5 instruct: full structure, explicit format, role assignment.

---

## DeepSeek-R1

Reasoning-native. Give short clean instructions: the goal and the desired output format. It emits reasoning in `<think>` tags by default — add "Output only the final answer, no reasoning tags." when that is unwanted.

---

## MiniMax

Current lineup and context sizes: `params.md` → MiniMax. The API is OpenAI-compatible and Anthropic-compatible, so prompts transfer directly from either. **Temperature is documented as ignored and fixed** on both endpoints — do not offer a temperature setting or a range; encode determinism and tone in the prompt.

- Strong at instruction following, structured output, code generation and long-context synthesis.
- Responds well to explicit role assignment and a clear output-format spec.
- May emit reasoning in `<think>` tags — add "Output only the final answer, no reasoning tags." when that is unwanted.
- For function calling, include the tool schemas directly.

---

## Llama, Mistral and open-weight models

Shorter prompts work better; these models lose coherence with deeply nested instructions. Use a simple flat structure, be more explicit than you would with Claude or GPT, and always put a role in the system prompt.

---

## Ollama — local deployment

Ask which model is running before writing: Llama, Mistral, Qwen and the Coder variants behave differently. The system prompt is the highest-leverage part — include it in the output so the user can set it in their Modelfile. Keep prompts short and flat. Lower temperature for deterministic work, higher for creative work; the usable range depends on the loaded model. For coding, point the user at a coder-specialized model rather than a general chat model.

---

## Reasoning-native models, legacy

`o3` and `o4-mini` are no longer listed in current OpenAI model documentation. If a user names one, treat it as legacy: give short clean instructions, state the goal and what done looks like, prefer zero-shot, and do not quote defaults or context sizes for it. Offer to route to a current model instead.

---

## Old patterns

<details>
<summary>Superseded guidance kept for recognition only — do not apply</summary>

- **"Do not add Chain of Thought to reasoning-native models."** Narrowed. The durable rule is: never ask any model to reveal hidden or private reasoning. Separately, do not add step-by-step scaffolding to a model that is already thinking. On Claude, a structured `<thinking>` / `<answer>` pattern remains a documented fallback when thinking is turned off.
- **"Claude 4.x follows instructions literally; Opus 4.x over-engineers; add a verification step."** Superseded. Opus 5 self-verified and over-delegated: verification instructions came out and subagents were constrained.
- **"Opus 4.7 spawns fewer subagents — request them explicitly."** Inverted on Opus 5.
- **Opus 5 routing generally.** Superseded by Opus 5.5, which is not in the current lineup's predecessor slot by accident: its default effort is lower, its thinking cannot be turned off, and forced tool use is rejected. Move an Opus 5 prompt across rather than porting its settings — see `params.md`.
- **"GPT-5.x handles dense instruction well — add structure."** Superseded: the current flagship wants less scaffolding, not more.
- **"Sonnet 5 rejects sampling parameters."** Narrowed, not dropped. The documented 400 on `temperature`, `top_p` and `top_k` is stated on the Sonnet 5 page only; no equivalent line appears for Sonnet 5.5. Steering tone through the system prompt remains the right advice either way — but do not claim the restriction for a current model. See `params.md`.
- **Sonnet 5 routing generally.** Superseded by Sonnet 5.5, whose effort levels are documented as recalibrated. Move the prompt across and re-run the sweep rather than porting the effort setting.
- **"GPT-5.6 Sol / Terra / Luna are the balanced and cost tiers."** Superseded. Those slugs have left the current model page; GPT-6.1 Sol and GPT-6 Luna hold those slots and no Terra equivalent is listed. See `params.md`.
- **"Grok 4.6."** Superseded by Grok 4.7; the slug and cutoff both moved. See `params.md`.
- **"Route to Gemini 3.5 Flash or 2.5 Flash for high-throughput work."** 3.5 Flash is now documented as legacy and the 2.5 family is access-limited to projects with prior usage. Route new builds to the current Flash entries in `params.md`.
- **"1M context window on MiniMax M2.7."** Wrong, and M2.7 is no longer documented at all — state no context size for any M2.x model. See `params.md`.
- **"MiniMax temperature must be between 0 and 1."** and **"MiniMax temperature range is `[0, 2]`, default `1`."** Both superseded. Temperature is documented as not supported, ignored, and fixed at 1 on both endpoints. Do not state a range at all — see `params.md`.
- **"MiniMax M2.x context is 204,800."** The M2.x models have left both API reference pages. The figure was right for its date; there is now no documented context size for them, so route an M2.x request at family level.
- **"Route a high-throughput Gemini build to 3.5 Flash."** 3.5 Flash has now left the model page entirely — 1.8.0 had it as legacy. `gemini-3.5-flash-lite` is the stable low-cost entry; see `params.md`.
- **"Gemini 3.7 Flash is the previous-generation Flash model."** Superseded: 3.7 Flash is no longer listed, and 3.6 Flash now carries the "previous-generation Flash" line. See `params.md`.
- **"Claude Haiku 4.5 is the fast Haiku option; it has no effort parameter and takes a thinking budget."** Superseded by Haiku 5.5, which holds the lineup slot, defaults to `medium` effort, and rejects `budget_tokens`. Route the prompt across and set an effort level.
- **"Claude Sonnet 4.6 has its own prompting guide."** It no longer does; the model-specific table lists eight guides and Sonnet 4.6 is not among them. See `params.md`.
- **"Ask OpenAI for a reasoning summary via the `summary` parameter."** The parameter is no longer documented. See `params.md`.

</details>

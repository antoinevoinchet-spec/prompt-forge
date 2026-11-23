# Changelog

Versioning lives here rather than in the SKILL.md frontmatter, where `version` is not a spec field.

## Unreleased

- **The skill says when its model facts are over 60 days old.** Nothing told a user that `references/params.md` had gone stale when the monthly re-check stopped: the skill kept quoting its facts as current. New step 0 of the Model recency gate: when line 3 of `params.md` is more than 60 days old, the response says so in one line and, with a web search or fetch tool, checks the requested model on the provider's official page; without one, those details are reported as unverified. Verification gate point 8 checks the line. Scenarios 18 (facts 75 days old) and 19 (10 days old, no warning) test it. Scenario 18 accepts either outcome the rule allows (a web check that succeeded, or the unverified line) and passed on 2026-11-23 (3 paid passes: two said the details were not re-checked, one checked the models page online).

## 1.9.3 — 2026-11-23

Monthly re-verification of `references/params.md`, 2026-11-23. Midjourney not re-verified (both pages returned HTTP 403).

- **Claude Fable 5.2 (`claude-fable-5-2`) replaces Fable 5.1** in the lineup and in the default-recommendation sentence; Mythos 5.2 added under "All models" (limited availability) — <https://platform.claude.com/docs/en/models/overview>
- **Effort `xhigh` and `max` lists gain Fable 5.2 and Mythos 5.2**; Fable 5.2 default `high` — <https://platform.claude.com/docs/en/build-with-claude/effort>
- **Haiku 5.5 refusal categories gain `reasoning_extraction`** — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5>
- **Opus 5.5 thinking blocks**: Fable 5.2 and Mythos 5.2 read them on the Claude API and Google Cloud (Google managed); the 2026-08-31 account-date rule and `"drop_block"` are gone, replaced by a prefix check that "might or might not result in a 400 error" — <https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5>
- **Nine Claude prompting guides** (Fable 5.2 and Mythos 5.2 added) — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- **OpenAI flagships now `gpt-6.2-astra`, `gpt-6.2-sol`, `gpt-6.1-terra`, `gpt-6-luna`** (1.05M); `gpt-6-astra` and `gpt-6.1-sol` superseded; `gpt-6-cyber` and `gpt-live-1.1` added; no model marked Deprecated — <https://developers.openai.com/api/docs/models>
- **OpenAI reasoning**: GPT-6.2 Astra and GPT-6.2 Sol reject `none`; `summary` parameter documented again (`auto`, `concise`, `detailed`); `reasoning.mode` stated for "GPT-5.6 and GPT-6 models" — <https://developers.openai.com/api/docs/guides/reasoning>
- **OpenAI image models `gpt-image-2.6-sunburst` and `gpt-image-2.6-flare` added** — <https://developers.openai.com/api/docs/guides/image-generation>, <https://developers.openai.com/api/docs/models>
- **Gemini source URL moved** to `aistudio.google.com/docs/models` (301); Gemini 4 range now `gemini-4-carbon`, `gemini-4-neon`, `gemini-4-hydrogen`, `gemini-4-argon` with "1M tokens" context and "64K / 1M tokens" output; 3.8 Flash now "previous-generation"; `gemini-omni-1.2-flash` and `genie-4` added; `gemini-2.5-flash` and `gemini-2.5-pro` Deprecated; new projects pointed to "Gemini 4 Hydrogen or 3.5 Flash-Lite" — <https://aistudio.google.com/docs/models>
- **Gemini prompting-strategies URL moved** to `aistudio.google.com/docs/prompting-strategies`, wording unchanged — <https://aistudio.google.com/docs/prompting-strategies>
- **Grok 4.7 role line now "It is the most capable model we've built."**; retirement notices gone; `grok-4.6` back in the pricing table unlabeled; "reasoning is configurable" no longer stated — <https://docs.x.ai/docs/models>
- **ElevenLabs: "Eleven v4 Turbo" no longer on the page** — <https://elevenlabs.io/docs/best-practices/prompting>
- Unchanged: MiniMax, Meshy, Sora shutdown, Claude Sonnet 5 sampling restriction, Sonnet 5.5 `between_tools`, Gemini prompting extracts.

- **Description no longer promises shortening.** The first trigger battery (`evals-v2/`) showed "Shorten this prompt…" never starts the skill (0 of 3), and `SKILL.md` defines no shortening flow: the word lived only in the description. The description now says "Writes, repairs and ports prompts". Claude shortens a prompt well on its own; a real shortening mode would first need the with/without-skill comparison to show it adds something.
- **The skill asks which tool before writing when the request names none.** Scenario 14 ("rewrite my cold sales emails in a warmer tone") wrote a prompt straight away in 2 of 3 runs, against the hard rule "confirm the target tool before writing". The rule now says to ask even when a text LLM looks likely. The 3-question limit now counts every question mark: one run asked 5, another 4.

## 1.9.2 — 2026-10-28

Two behaviours caught by the first automated run of the eight evals (`scripts/run-evals.py`).

- **Output format, splitting.** The rule said "two genuinely independent tasks", and the model judged that differently from one run to the next: eval 08 split the request once and returned one prompt the next time. The rule now says to count the distinct deliverables before writing, and to split when two or more can each be run and judged on their own. Each block is headed by its `Prompt N` label.
- **Input sanitization.** A pasted instruction that conflicts with safety guidelines was dropped but paraphrased (eval 07, stable over two runs). Each finding is now stated in one line, quoting the pasted instruction verbatim and saying it was found inside the pasted text.

## 1.9.1 — 2026-10-28

Gate point 3 rewritten. It asked for "its strongest signal word" on every instruction, which pushes generated prompts towards `MUST`, `CRITICAL` and capitals throughout. Anthropic's best-practices page says the opposite where triggering is concerned — verbatim, under Tool usage: "Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt than previous models. If your prompts were designed to reduce undertriggering on tools or skills, these models might now overtrigger. The fix is to soften any aggressive language." — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>. The migration section adds: "If your prompts previously encouraged the model to be more thorough or use tools more aggressively, reduce that guidance."

Emphasis is not banned: the same page still writes "you MUST read the file before answering" in its own sample prompts. The gate now reserves it for the one or two rules whose violation is costly, and never for triggering. The passage names Opus 4.5 and 4.6 only; the Opus 5.5 prompting page says nothing on the subject, so the general page remains the governing source — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5>, checked 2026-10-28.

README: the evals row and the maintenance paragraph said five scenarios; `evals/` holds eight, as `evals/README.md` already states.

Not re-run: the eight evals, which `evals/README.md` asks for after any edit to `SKILL.md`.

## 1.9.0 — 2026-10-26

Monthly re-verification of `references/params.md`. Every section was re-fetched. Three lineups turned over at the bottom or the top — Claude at the Haiku slot, Gemini gained a Gemini 4 flagship, MiniMax shed its entire M2.x range — and two figures recorded as verified in 1.8.0 are now contradicted by their own sources: MiniMax temperature and the Meshy `negative_prompt` field. One 1.8.0 removal reversed: ElevenLabs `[sarcastic]` is documented again.

**Claude** — <https://platform.claude.com/docs/en/models/overview>

- **Claude Haiku 5.5 (`claude-haiku-5-5`) replaces Claude Haiku 4.5** in the lineup: 1M context (was 200K), 128K max output (was 64K), default effort **`medium`**, knowledge cutoff **Jun 2026** (was Feb 2025), role line "For high-volume, latency-sensitive tasks such as classification, extraction, and routing". Haiku 4.5 keeps its mention in the best-practices introduction, so it is recorded as selectable but not recommended.
- **The effort page's `high` and `medium` lines were amended** to add Haiku 5.5 to the `medium`-default set: `high` is now "The default on every model that supports effort except Claude Opus 5.5 and Claude Haiku 5.5." Both 1.8.0 verbatim extracts for those lines were stale and are replaced. Per-value model availability for `xhigh` and `max` is now recorded — <https://platform.claude.com/docs/en/build-with-claude/effort>.
- **Haiku 5.5 is the first Haiku with effort levels**, and effort replaces the `budget_tokens` budget Haiku 4.5 used. Thinking is on by default, counts toward `max_tokens`, and `thinking: {"type": "disabled"}` works at `low`/`medium`/`high` only — 400 at `xhigh` or `max`. Per-message effort change needs the `mid-conversation-output-config-2026-07-01` beta header. Refusal categories `cyber`, `frontier_llm`, `bio`, `general_harms` with no server-side fallback. New profile section in `tools-llm.md` — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5>.
- **Thinking-block compatibility widened.** Opus 5.5 also reads Sonnet 5.5 and Haiku 5.5 blocks, but only on the Claude API and Claude Models on Google Cloud (Google managed); Fable 5.1 and Mythos 5.1 read Opus 5.5 blocks on the Claude API. Added: unreadable blocks are dropped unbilled, and the prefix-change check for accounts created on or after 2026-08-31 with the `thinking-binding-controls-2026-08-01` beta header — <https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5>.
- **Sonnet 4.6 no longer has its own prompting guide.** The model-specific table lists eight, and Haiku 5.5 took a slot. Adaptive thinking is now documented as covering "Claude 4.6 and later models and Claude Mythos Preview", and `budget_tokens` is noted as still functional but deprecated on Opus 4.6 and Sonnet 4.6 — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>.
- **The Sonnet 5 sampling sentence was reworded**: the qualifier "to a non-default value" is gone, so the 1.8.0 verbatim extract no longer matched character for character. The restriction is still Sonnet 5 only — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5>.
- Unchanged: Fable 5.1, Opus 5.5 and Sonnet 5.5 rows; the two-clause default recommendation; the Opus 5.5-at-`medium` comparison; the Opus 5.5 breaking changes for `thinking`, `tool_choice` and the computer tool. Sonnet 5.5's `between_tools` floor gained the detail that `display`, `budget_tokens` or `block_binding` sent alongside it returns 400 — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5>.

**OpenAI** — <https://developers.openai.com/api/docs/models>

- **The `summary` parameter is no longer documented** on the reasoning guide. 1.7.x and 1.8.0 both recorded its values (`auto`, `concise`, `detailed`) and the opt-in sentence; that claim is removed to *Deliberately unsourced*, and `tools-llm.md` no longer tells the reader a reasoning summary is an available API setting. What the page documents instead: `reasoning.context` (`auto`, `current_turn`, `all_turns`) and `reasoning.mode` (`standard` default, `pro`) — <https://developers.openai.com/api/docs/guides/reasoning>.
- **GPT-6.1 Sol's effort constraint is narrower than recorded**: verbatim "does not support `none` or `minimal` and defaults to `medium`." 1.8.0 recorded only that Astra and Sol both reject `none`.
- `gpt-rosalind-research` added to the specialized list, alongside `gpt-5.6-cyber`, the image models and the voice/realtime/transcription family. Four models are marked Deprecated, not one: `gpt-realtime-mini`, `gpt-4o-mini-tts`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`.
- Unchanged: the three flagship rows and their role lines; Astra's 1,050,000 context, 128,000 max output, Apr 30 2026 cutoff and `low`–`max` effort set — <https://developers.openai.com/api/docs/models/gpt-6-astra>. The image-generation page still names `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare` with no DALL·E 3 — <https://developers.openai.com/api/docs/guides/image-generation>.

**Google Gemini** — <https://ai.google.dev/gemini-api/docs/models>

- **A Gemini 4 flagship now sits above the Flash range**: `gemini-4-argon`, "Our flagship reasoning model with a unified 1M context window and long decodes up to 1M tokens." It is the **only** model on the page that states a context window, so the blanket 1.8.0 instruction "context-window sizes are not stated per model — do not quote one" is now wrong as written and has been narrowed to that one exception.
- **Gemini 3.7 Flash is no longer listed.** 1.8.0 added it as the previous-generation Flash; that line has moved to 3.6 Flash. **Gemini 3.5 Flash has left the page too** — 1.8.0 had it as legacy. `gemini-3.5-flash-lite` is listed and stable, which is what the "route high-throughput work elsewhere" advice now points at.
- Added: `gemini-3.8-live-extended-thinking`, `gemini-3.8-flash-tts`, `gemini-3.8-flash-lite-tts`, `gemini-3.5-transcribe` / `-live`, `gemini-omni-1.1-flash`, `gemini-nano-banana-2.1`, `gemini-3.1-flash-lite-image`, `gemini-3-flash-preview`. Recorded as Legacy, Preview: `gemini-3.1-flash-live-preview`, `gemini-3.1-flash-tts-preview`. Recorded as Shut down: `imagen-4.0-generate`, `gemini-robotics-er-1.6-preview`, `gemini-2.5-computer-use-preview-10-2025`, `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-3.1-flash-lite-preview`, `gemini-3-pro-preview`.
- The Gemini 2.5 access limitation is restated more precisely: not deprecated, available until further notice, restricted to users with prior usage, new projects directed to 3.5 Flash-Lite or 3.8 Flash.
- Unchanged: the few-shot and context-placement quotes — <https://ai.google.dev/gemini-api/docs/prompting-strategies>.

**xAI Grok** — <https://docs.x.ai/docs/models>

- Unchanged for the flagship: Grok 4.7, `grok-4.7`, "500k tokens", cutoff May 2026, image inputs to 20 MiB with no count limit, jpg/jpeg or png.
- Added, with no figures attached because the page gives none: `grok-imagine-image-2.0`, `grok-imagine-video-1.5`, and a Grok Voice API. Noted: two linked retirement notices (May 15 2026, Nov 2 2026) that were not read, and `logprobs` / `top_logprobs` unsupported on `grok-4.20` and newer.

**MiniMax** — <https://platform.minimax.io/docs/api-reference/text-openai-api>, <https://platform.minimax.io/docs/api-reference/text-anthropic-api>

- **Temperature is no longer a ranged parameter.** Verbatim on both endpoints: "Not supported yet; any value passed has no effect. `MiniMax-M3.1-Flash` and `MiniMax-M3` always use 1". The Anthropic-compatible page lists its support status as "Ignored". The `[0, 2]` range that 1.8.0 re-confirmed verbatim is gone, and the verbatim extract that existed to make it cheap to re-check was itself the stale line. `tools-llm.md` no longer offers a MiniMax temperature setting.
- **`MiniMax-M3.1-Flash-Preview` is now `MiniMax-M3.1-Flash`**, and **the whole M2.x range is off both pages** — M2.7, M2.5, M2.1, M2 and the `-highspeed` variants. Their 204,800 figure was correct for its date but has no current source, so an M2.x request routes at family level.

**Video, voice and 3D**

- **ElevenLabs `[sarcastic]` is documented again** — the one 1.8.0 removal this cycle reverses. The tag set on the page is far wider than the five examples recorded: voice tags including `[laughs harder]`, `[starts laughing]`, `[wheezing]`, `[exhales]`, `[curious]`, `[snorts]`, `[mischievously]`; sound effects `[gunshot]`, `[applause]`, `[clapping]`, `[explosion]`, `[swallows]`, `[gulps]`; and `[strong X accent]`, `[sings]`, `[woo]`, `[fart]`. **Eleven v4 Turbo** is named as a current model and `eleven_flash_v2` as the phoneme-tag-compatible one. Speed 0.7–1.2 default 1.0 and the v4/v3 no-SSML-breaks rule are unchanged — <https://elevenlabs.io/docs/best-practices/prompting>.
- **Meshy `negative_prompt` has left the page entirely.** 1.6.0 through 1.8.0 recorded it as deprecated and inert; there is now no documented field, which is a stronger statement than deprecation and is recorded as such. **`art_style` no longer names Meshy-6** — the page says only "Leave it out. Meshy ignores it." Added: `topology` defaults to `triangle`, and `quad` with `meshy-t2` or `meshy-t2.5` returns 400 — <https://docs.meshy.ai/en/api/text-to-3d>.
- **Sora's historical resolution list shrank.** The banner gained "No one-to-one replacement API is available." and "This guide is retained for historical reference."; the sizes now named are `1280x720` plus the Pro 1080p pair, and generations are documented as 16 and 20 seconds with extensions to 120 seconds total. The three smaller landscape sizes recorded since 1.6.0 are removed — <https://developers.openai.com/api/docs/guides/video-generation>.

**Midjourney** — unchanged where it matters, better sourced where it did not.

- Default still V8.2, Niji 7 still January 9 2026. **The Version page no longer states the Raw Mode spelling**, so `--raw` is now attributed to the parameter-list page alone — the fact held, the citation did not. The full 30-entry parameter list is recorded, including `--oref` noted as replaced by the Edit Model in V8.X, and the only stated values on the page (Motion low/high, SD/HD at 1024px and 2048px) — <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>, <https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List>.

**Unverified, still.** The thirteen family-level-only tools — Runway, Kling, LTX Video, Dream Machine, SeeDream, Tripo, Rodin, Unity AI, Blender AI add-ons, ComfyUI, Zapier, Make, n8n — have no official documentation retrieved. Unchanged from 1.8.0.

**Not revisited.** `SKILL.md`, the templates and the evals are untouched, per the maintenance contract. Every verbatim extract carries a 2026-10-26 spot-check date.

## 1.8.0 — 2026-10-01

Monthly re-verification of `references/params.md`. Every section was re-fetched; eight of the nine sources moved. The Claude lineup turned over at the Sonnet slot, OpenAI's balanced and cost tiers were replaced wholesale, Grok's flagship incremented, Sora went from deprecated to gone, and the Claude effort page was rewritten — so five of the verbatim extracts that existed to make re-verification cheap were themselves stale.

**Claude** — <https://platform.claude.com/docs/en/models/overview>

- **Claude Sonnet 5.5 (`claude-sonnet-5-5`) replaces Claude Sonnet 5** in the lineup: 1M context, 128K max output, default effort `high`, knowledge cutoff **Jun 2026** (Sonnet 5 was Jan 2026). Sonnet 5 is marked superseded; its prompting guide is still published, which is why the slug still resolves.
- The default-recommendation sentence gained a second clause naming Fable 5.1 for demanding reasoning, or when evals on Opus 5.5 at higher effort fall short.
- **The effort-value descriptions were rewritten**, and the canonical page for them is now <https://platform.claude.com/docs/en/build-with-claude/effort>, not the Sonnet 5 prompting page. `xhigh` is "Extended capability for long-horizon work."; `high` is "Spends as many tokens as the task needs for excellent results. The default on every model that supports effort except Claude Opus 5.5."; `medium` and `low` likewise reworded. The old phrasings survive on the Sonnet 5 page and are now flagged as not-current.
- The Opus 5.5-at-`medium` comparison is restated verbatim from <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5>, which now also notes `low` coming close on several coding evaluations.
- **Sonnet 5.5's thinking floor is new material**: `thinking: {"type": "between_tools"}` is the lowest setting, accepted at `high` effort or below, and returns 400 at `xhigh` or `max`. Recorded with the verbatim extract. The general rule is now that on Claude 4.7 and later `budget_tokens` returns 400 — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5>, <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>.
- **The sampling-parameter 400 is narrowed to Sonnet 5.** It is documented on that page and on no current model's page. 1.7.x stated it as a Sonnet-class fact and `tools-llm.md` told the reader sampling parameters are rejected; both are corrected, and the old form is kept under `Old patterns`.
- `computer_20251124` is unsupported on the Claude API and Google Cloud but **still works on Amazon Bedrock** — a carve-out 1.7.x did not record. Thinking-block compatibility is now stated precisely: Opus 5.5 reads blocks from Opus 5 and earlier Opus, Sonnet and Haiku, not from Fable or Mythos — <https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5>.
- The claim that 128,000 max output "is documented as working well for long agentic tasks" is removed to *Deliberately unsourced*: the best-practices page no longer says it. 128K stays as the documented max output from the model table.

**OpenAI** — <https://developers.openai.com/api/docs/models>

- **GPT-6.1 Sol (`gpt-6.1-sol`) and GPT-6 Luna (`gpt-6-luna`) replace GPT-5.6 Sol and GPT-5.6 Luna.** GPT-5.6 Terra has no successor on the page. All three 5.6 general-purpose slugs are marked legacy; `gpt-5.6-cyber` remains listed as a specialized model.
- GPT-6 Astra's role line changed to "Our most capable model for the most demanding work". Its figures are unchanged: 1,050,000 context, 128,000 max output, cutoff Apr 30 2026 — <https://developers.openai.com/api/docs/models/gpt-6-astra>.
- `none` is now documented as unsupported on **both** Astra and GPT-6.1 Sol, not Astra alone. The raw-reasoning sentence was rewritten and is re-quoted verbatim, with the summary parameter noted as opt-in — <https://developers.openai.com/api/docs/guides/reasoning>.
- `gpt-realtime-mini` is marked Deprecated.

**Google Gemini** — <https://ai.google.dev/gemini-api/docs/models>

- **Gemini 3.5 Flash is now documented as legacy**, and **the Gemini 2.5 family is access-limited** to projects with prior usage, with new projects directed elsewhere. Both were plain lineup rows in 1.7.x; routing a new build to either is now wrong.
- Added: Gemini 3.7 Flash, 3.6 Flash, 3.1 Flash-Lite, Nano Banana Pro. Gemini 3.8 Live's and Nano Banana 2's role lines were reworded and are re-quoted. Context windows are still not stated per model.

**xAI Grok** — <https://docs.x.ai/docs/models>

- **Grok 4.7 (`grok-4.7`) replaces Grok 4.6**; knowledge cutoff moved to **May 2026**. Context stays 500K and the image-input limits are unchanged. Grok 4.6 is marked superseded.

**MiniMax** — <https://platform.minimax.io/docs/api-reference/text-openai-api>

- Added MiniMax-M3.1-Flash-Preview, 1,000,000 context. Temperature `[0, 2]`, default `1`, re-confirmed verbatim.

**Video, voice and 3D**

- **Sora 2 is shut down, not deprecated** — "The Sora 2 models and Videos API were shut down on September 24, 2026 and are no longer available", and no replacement OpenAI video model is listed. 1.7.x told the reader to check the status before building; there is nothing to check. The slugs, clip length and the fuller resolution list are kept as historical context for recognizing an inherited prompt, and `tools-visual.md` now declines to produce a Sora prompt — <https://developers.openai.com/api/docs/guides/video-generation>.
- **ElevenLabs: Eleven v4 exists**, and the no-SSML-breaks rule now covers v4 and v3 both — 1.7.x had it as v3 only, against v2. Documented current models are Eleven v4, Eleven v3, Eleven Multilingual v2, Eleven Flash v2.5. The audio-tag example set is `[laughs]`, `[whispers]`, `[sighs]`, `[excited]`, `[crying]`; **`[sarcastic]` is removed** — it is not on the page and was carried on a stale read. Speed 0.7–1.2 default 1.0 unchanged — <https://elevenlabs.io/docs/best-practices/prompting>.
- **Meshy `art_style` is now marked deprecated** as well as ignored by Meshy-6. `negative_prompt` deprecation, the 800-character prompt cap, modes, topology and target formats are unchanged — <https://docs.meshy.ai/en/api/text-to-3d>.

**Unchanged on re-fetch.** Midjourney default V8.2, Niji 7 launched January 9 2026, Raw Mode spelled `--raw` — <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>. OpenAI image models `gpt-image-2.5-sunburst` / `gpt-image-2.5-flare` with no DALL·E 3 on the page — <https://developers.openai.com/api/docs/guides/image-generation>. The `o3` / `o4-mini` legacy status, MiniMax temperature range, and the Gemini few-shot and context-placement quotes — <https://ai.google.dev/gemini-api/docs/prompting-strategies>. The thirteen family-level-only tools still have no official documentation.

**Not revisited.** `SKILL.md`, the templates and the evals are untouched, per the maintenance contract. Every verbatim extract carries a 2026-10-01 spot-check date.

## 1.7.1 — 2026-09-23

The Cursor profile now spells out Template G's section headings — `Scope lock` and `Completion criteria`, never "Scope" or "Done when". Eval 04 got them right on the run where it opened `templates.md` and wrong on the run where it did not, so the terminology was riding on whether a second file happened to be read. The profile line is read every time.

## 1.7.0 — 2026-09-23

Eval 04's first check replaced. It required `references/patterns.md` to be read; three successive attempts to make that happen failed — as routing prose in 1.5.0, as gate point 7 in 1.6.0, across four live runs. Meanwhile the repairs themselves were consistently good: the last run named the vague verb, the missing success criterion, the over-permissive agent, the leaked credential and the chain-of-thought request, and fixed each. Those are patterns 1, 3, 4 and 27 plus Credential Safety, applied without the file being opened.

A check that fails three times while the outcome it exists to guarantee arrives anyway is testing the means, not the end. It now reads: the response names at least four distinct defects in the pasted prompt and states the fix for each.

**Why the gate could not carry it.** Point 9, added in the same release, worked on its first run: rewording a heading that is already written costs nothing. Point 7 asks the model to go back and open a file after the reading decision was made a hundred lines earlier, and that never happened. The gate sits at the end of `SKILL.md`; it can correct what is written, not undo what was skipped. An instruction to read something has to arrive before the routing decision, not after.

This leaves an open question rather than a closed one: if `patterns.md` is never read and the repairs are good regardless, the file has not yet demonstrated its value in the bundle.

## 1.6.0 — 2026-09-23

Evals 02 and 04 rerun on 1.5.0. The terminology fix landed on both — each now writes `Completion criteria`. The `patterns.md` routing sentence, shipped in the same release, produced nothing: eval 04 still read the tool profile and `templates.md` and never opened the diagnostic reference.

**The lesson is architectural.** Both changes shipped together, in the same file, in the same version. The one written as a verification-gate point took effect on the first run; the one written as prose in the routing section was read as context and ignored. Behaviour that must happen belongs in the gate, which reads as a checklist to clear before answering, not in the surrounding prose.

- `patterns.md` moved from routing prose into gate point 7: the target's tool profile *and*, for a pasted prompt being repaired, adapted or split, `patterns.md` must both have been read, with an instruction to stop and read before answering.
- Gate point 9 gained a completeness clause. Eval 02 carried a `Scope lock` section in 1.4.0 and dropped it in 1.5.0 while gaining `Completion criteria` — the point listed the four terms but never required them to be present, so correcting one section's spelling licensed deleting another. For a target that executes commands or edits files, all three of `Scope lock`, `Action boundaries` and `Completion criteria` must now be named sections.

## 1.5.0 — 2026-09-23

All eight evals have now been run externally on claude.ai: 80 of 85 checks pass. Three findings, two of them defects in the skill.

- **Terminology drift, reproducible.** Evals 02 and 04 both produced a "Done when" heading where the glossary mandates `Completion criteria`; eval 07 got it right. The glossary said "use exactly these terms" and nothing verified it. The verification gate gains point 9: every glossary term appears in the generated prompt exactly as the Terminology table spells it, and a synonym is a defect to rename. Old point 9 shifts to 10.
- **The repair flow had no entry point to `patterns.md`.** Eval 04 routed on the target tool (Cursor → agentic profile) and never opened the diagnostic reference, leaving the 37 patterns as dead weight on the one flow that justifies them. The routing section now states that repairing, adapting or splitting a pasted prompt requires `patterns.md` in addition to the tool profile, and that the "never all three" rule governs tool profiles only.
- **Eval 01's output-shape check was too narrow**, and the skill was right. It demanded one of five concrete nouns; the prompt under test locked its output far harder, with a literal field-by-field template. The check now accepts either form. This is an eval fix, not a skill fix.

## 1.4.0 — 2026-09-23

The 1.3.0 trigger phrasings worked, but only halfway. On a live rerun of eval 07 the thinking line changed from "Porting a prompt over for use in Claude Code" to "Porting a prompt using the relevant skill guide" — the skill was recognised — yet no file was read and the same four output-contract failures repeated: no `Scope lock` heading, no `Action boundaries` heading, no agentic notice, no `🎯 Target:` line.

That splits triggering into two depths: recognising that a skill applies (fixed in 1.3.0) and actually opening its files (still failing). The two gate points added in 1.3.0 were therefore inert — they live inside the file that was not being opened.

The description is the only text guaranteed to be in context before the model decides whether to read anything, so it now ends with an explicit directive to read `SKILL.md` and the routed tool profile before writing, naming what those files hold. The same pattern the `claude-in-chrome` skill uses. The capability sentence about documentation verification was dropped to make room; the gate itself still enforces it. 993 characters.

## 1.3.0 — 2026-09-23

Under-triggering is not fixed; it was only fixed for the phrasings the description literally lists. Eval 07 — "Port this prompt — it was written for ChatGPT and I want to run it in Claude Code now" — did not fire the skill at all, on a live claude.ai run, and produced a spontaneous answer with no target line, no agentic notice and no tool profile read. The verb "ports" appears in the description's opening sentence; that was not enough. The example phrasings carry the triggering weight.

- **Description**: porting and conversion phrasings added in both languages — "port this prompt", "adapt this prompt for", "convert this prompt to", "rewrite this for Cursor", "I need a prompt for", "porte ce prompt vers", "adapte ce prompt pour".
- **Verification gate**: two points added, because it checked the prompt's quality and never the envelope around it. New point 7 requires the target category's tool profile to have been read before writing, and to stop and read it if not. New point 8 requires the output contract — the `🎯 Target:` line, plus the agentic notice whenever the target executes commands or edits files. Old points 7 and 8 shift down.
- **Eval 07**: gains an explicit first check that the skill fired without being named, matching eval 08. It previously assumed triggering and tested only what followed.

## 1.2.1 — 2026-09-23

`🎯 Target:` is pinned to its exact ASCII form regardless of the response language. Found by eval 08 on a live run: a French response rendered it `🎯 Target :`, with the space French typography puts before a colon, which fails a literal string check. It is a format marker, not prose. The sentence after it still follows the response's language.

## 1.2.0 — 2026-09-23

Three known defects closed: under-triggering, an internal contradiction on output format, and an unverified third of the tool surface.

**Triggering.** The description failed to fire on "améliore ce prompt stp, c'est pour ChatGPT" in a live claude.ai session — a request matching its own wording. Rewritten around explicit trigger phrasings in both English and French, with the anti-trigger clause cut to one sharp sentence ("Not for answering a question or performing the underlying task itself — only for producing the prompt that will") so it stops suppressing in-scope work. 737 characters. New `evals/08-under-trigger.json` covers the failure; it is the mirror of 05 and matters more, since a skill that never starts is worth nothing.

**Output format.** `SKILL.md` demanded "a single copyable prompt block" while patterns 2 and 6 ordered a two-task request split into Prompt 1 / Prompt 2 — a live session correctly violated the format rule to obey the pattern. The rule now permits a numbered sequence for genuinely independent tasks, with one line on running order, and explicitly forbids spreading one task across several blocks.

**Visual surface passed through the gate.** Three inherited statements were wrong:
- **Sora** — slugs `sora-2` and `sora-2-pro` are documented as **deprecated, shutdown 2026-09-24**. Recorded with the documented prompt shape, clip length and resolutions.
- **ElevenLabs** — "use SSML-like markers" is half wrong: SSML `<break>` is supported on one model generation and not the next, which uses bracketed audio tags. Speed range and both syntaxes recorded.
- **Meshy** — `negative_prompt` is **deprecated with no functional impact**, and `art_style` is ignored by the newest model. The old "negative prompts are supported — use them" advice would have silently done nothing.

What could not be verified is now labelled rather than implied: Runway, Kling, LTX Video, Dream Machine, SeeDream, Tripo, Rodin, Unity AI, Blender add-ons, ComfyUI checkpoint behavior, Zapier, Make and n8n carry an explicit *(unverified)* marker in `tools-visual.md` and a list in `params.md`, with the instruction to state no version, slug, parameter or figure for any of them.

Sources: <https://developers.openai.com/api/docs/guides/video-generation>, <https://elevenlabs.io/docs/best-practices/prompting>, <https://docs.meshy.ai/en/api/text-to-3d>

## 1.1.0 — 2026-09-23

Claude Opus 5.5 added; Claude Opus 5 removed from the current lineup. Triggered by a user report that the model had shipped, verified before anything was written.

- `params.md`: the Claude table now carries Opus 5.5 (`claude-opus-5-5`, 1M context, 128K max output, default effort `medium`, knowledge cutoff Jun 2026) alongside Fable 5.1, Sonnet 5 and Haiku 4.5, each with max output, default effort and cutoff. Opus 5 is marked superseded. Opus 5.5's breaking changes are recorded: thinking cannot be disabled, forced `tool_choice` is rejected, `computer_20251124` must migrate to `computer_toolset_20260801`.
- `tools-llm.md`: the Opus 5 block is replaced by an Opus 5.5 profile — remove think-carefully and write-out-your-reasoning instructions, start at the documented default effort, handle progress updates arriving as thinking blocks, supply elapsed-time budgets, name the turn endings an unattended run must avoid, and treat a text-only end of turn as a progress report.
- `tools-agentic.md`: the Claude Code profile no longer names Opus 5 for self-verification; it points at the current Claude profile and at `params.md`.
- **Source URL corrected.** `about-claude/models` now serves an older lineup (Opus 4.7 / Sonnet 4.6 / Haiku 4.5). The canonical page is `models/overview`, and `params.md` records the change so the next cycle does not re-read the stale one.

Sources: <https://platform.claude.com/docs/en/models/overview>, <https://platform.claude.com/docs/en/models/opus-5-5/overview>, <https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5>, <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5>

No change to `SKILL.md`, `templates.md`, `patterns.md` or `evals/`.

## 1.0.2 — 2026-09-22

Scenario 05 made self-contained: the Express handler it needs moved from an attached file into the `query`, and `files` is now empty. Every scenario runs from its `query` alone. Verified green 5/5 on a cold run before the change. No change to `SKILL.md` or `references/`.

## 1.0.1 — 2026-09-22

Three rules added to `SKILL.md`, closing three gaps found while running the evals: completion criteria that were partly narrative on scenarios 02 and 04, an agentic notice whose language was left undefined, and a recency gate that cited a blog URL carrying an unconfirmed model slug. No change to `references/` or `evals/`.

## 1.0.0 — 2026-09-21

First release of `prompt-forge`, forked from [prompt-master](https://github.com/nidhinjs/prompt-master) 1.8.0 by **Nidhin Joseph Nelson**, MIT licensed. The upstream license is carried over unchanged in `LICENSE`. Upstream 1.8.0 contributed the Model Recency Gate, the replacement of Chain-of-Thought with auditable reasoning, the Grok and Codex profiles, the versioned Claude 5 routing, and the fix for the truncated final row of `patterns.md`.

### Renamed

`prompt-master` → `prompt-forge`, because the upstream skill ships as a plugin and cannot be replaced in place. Both remain listed; the frontmatter description states when to prefer this one.

### Architecture

- Tool routing — roughly 60% of the old `SKILL.md`, loaded in full on every invocation to use one profile — moved into `references/tools-llm.md`, `references/tools-agentic.md` and `references/tools-visual.md`. `SKILL.md` keeps a category-to-file table. Result: 165 lines, down from 448.
- All references are one level deep from `SKILL.md`, with Unix slash paths.
- New `references/params.md` holds every version, slug, context size and numeric parameter, each with its source URL and a verification date — one file to revise per cycle.
- Reference files over 100 lines carry a table of contents.
- The diagnostic checklist moved into `references/patterns.md`, next to the patterns it maps to, so the same content is not maintained in two places.
- Dated framing ("Cline (formerly Claude Dev)", "Unity AI replaces retired Muse", "/compact at ~50% context", "Antigravity, powered by Gemini 3 Pro") moved into collapsed **Old patterns** sections at the end of each profile file, kept for recognition only.
- One term per concept, enforced by a glossary in `SKILL.md`: **scope lock**, **action boundaries**, **completion criteria**, **progress evidence**, **auditable reasoning**, **memory block**, **tool profile**. Replaces the mixed use of "stop conditions", "forbidden actions", "human review triggers", "done when", "success criteria" and "checkpoints".
- Prohibition lists rewritten as positive instructions where the effect is identical.
- Frontmatter reduced to `name` and `description`. Description is third-person, 677 characters, states what and when, and keeps the anti-trigger clause from 1.6.0.

### Preserved unchanged

Input Sanitization, Credential Safety, the Memory Block, all 37 failure patterns, and Templates A through M. Template M, previously "Opus 4.7 Task Brief", is generalized to any model with adaptive thinking and an effort control.

### Model facts — verified 2026-09-21

Every claim below was checked against the source given. Nothing in this skill states a model name, slug or number that is not in `references/params.md`.

| Claim | Source |
|-------|--------|
| Claude lineup: Fable 5.1 (`claude-fable-5-1`), Opus 5 (`claude-opus-5`), Sonnet 5 (`claude-sonnet-5`), Haiku 4.5 — 1M context except Haiku at 200K; Opus 5 is the documented starting point | <https://platform.claude.com/docs/en/about-claude/models> |
| Opus 5 self-verifies and over-delegates: remove verification instructions, constrain subagents, keep thinking enabled at lower effort | <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5> |
| Sonnet 5 is literal at low effort; sampling parameters and `budget_tokens` return HTTP 400; effort values `low`–`max`, default `high` | <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5> |
| Fable 5.1 long-horizon guidance, unattended-run system prompt, tool-call batching, low-effort search behavior | <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1> |
| Adaptive thinking modes per model; 3–5 examples; XML tag structuring; explain-why over bare prohibition; Mythos 5.1 and Mythos 5 share Fable guidance | <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices> |
| Long-context: documents above the query, XML document tags, quote grounding | <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips> |
| OpenAI flagship is GPT-6 Astra (`gpt-6-astra`), 1,050,000 context, 128K max output, cutoff Apr 30 2026; GPT-5.6 Sol/Terra/Luna remain listed | <https://developers.openai.com/api/docs/models>, <https://developers.openai.com/api/docs/models/gpt-6-astra> |
| Reasoning effort values; Astra rejects `none`; raw reasoning tokens are not exposed, only a `summary` | <https://developers.openai.com/api/docs/guides/reasoning> |
| GPT-6 Astra prompting: remove scaffolding written for earlier models, relax restrictive boundaries, define completion explicitly | <https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra> |
| `o3` and `o4-mini` absent from current model documentation → treated as legacy | <https://developers.openai.com/api/docs/models> |
| Gemini lineup: 3.8 Flash, 3.8 Live, 3.1 Pro, 3.5 Flash, 2.5 Flash, Nano Banana 2 | <https://ai.google.dev/gemini-api/docs/models> |
| Gemini: always include few-shot examples; context first, instruction last | <https://ai.google.dev/gemini-api/docs/prompting-strategies> |
| Grok 4.6 (`grok-4.6`), 500K context, configurable reasoning, no realtime knowledge without search tools | <https://docs.x.ai/docs/models> |
| MiniMax M3 at 1,000,000 context, M2.x at 204,800; temperature range `[0, 2]`, default `1` | <https://platform.minimax.io/docs/api-reference/text-openai-api>, <https://platform.minimax.io/docs/api-reference/text-anthropic-api> |
| Midjourney default V8.2; Niji 7; documented parameters `--ar`, `--no`, `--v`, `--stylize`, `--chaos`, `--raw`, `--sref` | <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>, <https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List> |
| Current OpenAI image models `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare`; DALL·E 3 not listed | <https://developers.openai.com/api/docs/guides/image-generation> |

### Corrections to inherited claims

| Was | Now |
|-----|-----|
| "Fable 5" (upstream 1.8.0) | Fable **5.1** |
| "ChatGPT / GPT-5.6" as flagship (upstream 1.8.0) | GPT-6 Astra; the 5.6 family is retained as the balanced and cost tiers |
| "Opus 4.7 spawns fewer subagents — request them explicitly"; "add a verification step" | Inverted: Opus 5 self-verifies and delegates readily. Remove verification instructions, constrain subagents. |
| "Do not add Chain of Thought to o3/o4-mini/R1/Qwen3-thinking" | Narrowed to the durable rule: never request hidden or private reasoning from any model. Adding step-by-step scaffolding to a model already thinking is a separate, model-specific point. |
| "MiniMax temperature must be between 0 and 1" (1.6.0 and 1.8.0) | `[0, 2]`, default `1` |
| "1M context window on M2.7" | M2.7 is 204,800; M3 is 1,000,000 |
| "`--v 6 --style raw`" | `--style raw` is not documented syntax; Raw Mode is `--raw`, and the default version has moved to V8.2 |
| DALL·E 3 profile | GPT Image models |
| "35-pattern reference" in the SKILL.md footer while `patterns.md` header said 37 | 37 everywhere; the count is verified by the evals |
| `patterns.md` ended with the corrupted fragment `schema" \|` after row 37 | Fixed (already corrected upstream in 1.8.0) |
| README showed an output with `⚡ Framework:` and `💰 Tokens:` lines that SKILL.md forbids | README now shows the real two-part output format |
| README restated the skill's guidance | README points at `SKILL.md`; the skill is the single source of truth |

### Removed as unsourceable

No official documentation confirming these could be retrieved on 2026-09-21, so they were removed rather than carried forward. Each is listed in `references/params.md` with its replacement: Stable Diffusion "CFG 7–12" and "steps 20–30 / 40–50"; Ollama "temperature 0.1 for coding, 0.7–0.8 for creative"; "system prompts under 200 words" for reasoning models; "Claude Code default is xhigh effort".

### Added

Five hand-run evaluation scenarios in `evals/`, including one negative case that must not trigger the skill, with a README covering how to run them and how to read a failure.

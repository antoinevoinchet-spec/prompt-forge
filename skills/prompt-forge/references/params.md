# Versioned parameters — single review point

Every model name, API slug, version number, context size and numeric parameter used anywhere in this skill lives here, with the official source it was verified against. **Every section verified 2026-11-23, except Midjourney (both pages returned HTTP 403 on 2026-11-23; last verified 2026-10-26).** Revise this file first at each maintenance cycle; the tool profiles describe durable behavior and should need far fewer edits.

Anything not listed here has no verified source. Do not state it. Route at family level instead.

## Contents

- [Claude](#claude)
- [OpenAI](#openai)
- [Google Gemini](#google-gemini)
- [xAI Grok](#xai-grok)
- [MiniMax](#minimax)
- [Video, voice and 3D](#video-voice-and-3d)
- [Image generation](#image-generation)
- [Unverified — family-level only](#unverified--family-level-only)
- [Verbatim extracts — highest-risk figures](#verbatim-extracts--highest-risk-figures)
- [Deliberately unsourced](#deliberately-unsourced)

---

## Claude

Source: <https://platform.claude.com/docs/en/models/overview>

> Source URL changed on 2026-09-23. `about-claude/models` served an older lineup; the canonical page is `models/overview`. Read the latter.

| Model | API slug | Context | Max output | Default effort | Knowledge cutoff | Documented role |
|-------|----------|---------|-----------|----------------|------------------|-----------------|
| Claude Fable 5.2 | `claude-fable-5-2` | 1M | 128K | `high` | Jun 2026 | "For demanding reasoning and long-horizon agentic work" |
| Claude Opus 5.5 | `claude-opus-5-5` | 1M | 128K | `medium` | Jun 2026 | "For long-running agentic coding and knowledge work" |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M | 128K | `high` | Jun 2026 | "The best combination of speed and intelligence" |
| Claude Haiku 5.5 | `claude-haiku-5-5` | 1M | 128K | `medium` | Jun 2026 | "For high-volume, latency-sensitive tasks such as classification, extraction, and routing" |

Default recommendation, verbatim: "If you're unsure which model to use, start with Claude Opus 5.5 for most workloads. Use Claude Fable 5.2 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short."
Per-model row detail: <https://platform.claude.com/docs/en/models/opus-5-5/overview>

**Claude Fable 5.1 is superseded** by Fable 5.2 in the lineup table. It is still listed under "All models" (1M context, 128K max output), as are Claude Mythos 5.1 and the new Claude Mythos 5.2, both marked "limited availability". Route a new build to Fable 5.2; for an existing Fable 5.1 prompt, the effort page says: "Run an effort sweep on your own evals rather than carrying settings over from Claude Fable 5.1." Fable 5.2 "supports all five effort levels. The API default is `high`."
Sources: <https://platform.claude.com/docs/en/models/overview>, <https://platform.claude.com/docs/en/build-with-claude/effort>

**Claude Sonnet 5 is superseded** by Sonnet 5.5 and no longer appears in the current lineup, though its prompting guide is still published. Route an existing Sonnet 5 prompt to Sonnet 5.5 and re-run its effort sweep — the effort levels are documented as recalibrated between the two.

**Claude Opus 5 is superseded** by Opus 5.5 and no longer appears in the current lineup. Do not recommend it; route an existing Opus 5 prompt to Opus 5.5 and re-run its effort sweep.

**Claude Haiku 4.5 no longer holds the Haiku slot** in the lineup table — Haiku 5.5 does. Haiku 4.5 is still named among current models in the best-practices introduction and appears on the overview page only as a Models API example, so treat it as selectable but not the thing to recommend: route a new build, and an existing Haiku 4.5 prompt, to Haiku 5.5. Haiku 5.5 is the first Haiku model with effort levels, and effort replaces the `budget_tokens` thinking budget Haiku 4.5 used.
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5>

**Haiku 5.5 specifics.** Default effort `medium`; `low` is documented for "chat, short tool tasks, and simple, high-volume requests", `high` for "knowledge work, longer agent tasks, and strict instruction following", `xhigh` and `max` "for work where a quality gain on your evals justifies the cost". Thinking is on by default and counts toward `max_tokens`, which "can go up to 128,000". Thinking can be turned off with `thinking: {"type": "disabled"}` "at `low`, `medium`, and `high` only. At `xhigh` and `max`, the request returns a 400 error." A per-message effort change needs the `mid-conversation-output-config-2026-07-01` beta header plus adaptive thinking; with thinking off it returns a 400. Refusals surface as `stop_reason: "refusal"` with categories `cyber`, `frontier_llm`, `bio`, `reasoning_extraction` or `general_harms`, with no server-side fallback. `reasoning_extraction` means "the request asks the model to reproduce its internal reasoning in the response text" — do not write a Haiku 5.5 prompt that asks it to write its reasoning out.
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5>

**Effort parameter.** Values `low`, `medium`, `high`, `xhigh`, `max`. `high` is documented as the default "on every model that supports effort except Claude Opus 5.5 and Claude Haiku 5.5"; those two default to `medium`. Opus 5 defaults to `high`. `xhigh` is documented as available on Fable 5.2, Mythos 5.2, Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 5, Opus 4.8, Opus 4.7, Sonnet 5.5, Sonnet 5 and Haiku 5.5; `max` on that set plus Mythos Preview, Opus 4.6 and Sonnet 4.6. Setting `effort` to a model's default behaves the same as omitting it. Verbatim: "In Anthropic's testing, Claude Opus 5.5 at `medium` matches or exceeds Claude Opus 5 at `high` on coding and knowledge-work evaluations, and on several coding evaluations `low` comes close to it at much lower cost."
Canonical effort page: <https://platform.claude.com/docs/en/build-with-claude/effort>
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5>

**Opus 5.5 breaking changes vs Opus 5.** `thinking: {"type": "disabled"}` and `thinking: {"type": "enabled", "budget_tokens": N}` both return 400 — thinking cannot be disabled and cannot take a manual budget. `tool_choice: {"type": "any"}` and `{"type": "tool", "name": "..."}` return 400; use `"auto"` or `"none"`. The `computer_20251124` tool is unsupported on the Claude API and Google Cloud — migrate to `computer_toolset_20260801`; it continues to work on Amazon Bedrock. Thinking blocks record the model that produced them: Opus 5.5 reads blocks from Opus 5 and earlier Opus, Sonnet and Haiku models, and — on the Claude API and Claude Models on Google Cloud (Google managed) only — from Sonnet 5.5 and Haiku 5.5; it does not read blocks from Fable or Mythos models. Fable 5.2 and Mythos 5.2 read Opus 5.5 blocks on the Claude API and Claude Models on Google Cloud (Google managed) only; Fable 5.1 and Mythos 5.1 read them on the Claude API only; no other model does. Unreadable blocks are dropped before the model sees them, the request still succeeds and they are not billed; with the `thinking-binding-controls-2026-08-01` beta header the API reports the drop in a top-level `input_transformations` array. The API also checks whether anything before an Opus 5.5 thinking block has changed (the `system` prompt, the `tools`, and every earlier message); verbatim, failing that prefix check "might or might not result in a 400 error". Keep the conversation append-only. (The account-creation date of 2026-08-31 and the `"drop_block"` setting recorded in 1.9.0 are no longer on the page.)
Source: <https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5>
Sources: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>, <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5>, <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1>

**Thinking.** Adaptive thinking is the mode on Claude 4.6 and later models and on Claude Mythos Preview. Verbatim: "On Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, and Claude Opus 5.5, thinking is always on and adaptive thinking is the only mode." On Opus 5, thinking can be disabled "only at effort `high` or lower". On Sonnet 5.5 the lowest thinking setting is `thinking: {"type": "between_tools"}`, accepted at `high` effort or below; at `xhigh` or `max` effort a `between_tools` request returns 400, and with it in effect a per-message `output_config.effort` differing from the level in effect also returns 400. On Claude 4.7 and later, setting `budget_tokens` returns a 400 error — prefer lowering effort, or `max_tokens` as a hard ceiling; an extended-thinking `budget_tokens` cap "is still functional on Opus 4.6 and Sonnet 4.6 but is deprecated". On Sonnet 5.5, `between_tools` also takes no other field: `display`, `budget_tokens` or `block_binding` sent with it returns a 400. At `xhigh` and `max` effort these models think longer before replying, so leave room in `max_tokens`.
Sources: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>, <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5>

**Sampling parameters.** Setting `temperature`, `top_p` or `top_k` returns a 400 error **on Claude Sonnet 5** — documented as "new for Sonnet-class models". (The page's wording changed between 2026-10-01 and 2026-10-26: the qualifier "to a non-default value" is gone, and the Design section now states flatly that "`temperature` is not accepted on Claude Sonnet 5".) No equivalent restriction is stated on the Sonnet 5.5, Opus 5.5, Fable 5.1 or effort pages; do not assert one for those models. Steer tone through the system prompt regardless.
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5>

**Examples.** "Include 3–5 examples for best results."
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>

**Models with their own published prompting guide:** nine guides — Fable 5.2 and Mythos 5.2 (shared), Fable 5.1 and Mythos 5.1 (shared), Fable 5 and Mythos 5 (shared), Sonnet 5.5, Sonnet 5, Opus 5.5, Opus 5, Opus 4.8, Haiku 5.5. **Sonnet 4.6 no longer has its own guide**; it, Opus 4.7, Opus 4.6 and Haiku 4.5 are named as current models in the introduction but covered only by the general sections. The Fable 5.2 guide (<https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2>) was not fetched in the 2026-11-23 run; state nothing from it.
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>

---

## OpenAI

Source: <https://developers.openai.com/api/docs/models>

| Model | API slug | Context | Documented role |
|-------|----------|---------|-----------------|
| GPT-6.2 Astra | `gpt-6.2-astra` | 1.05M | "Our most capable model for your hardest projects, from start to finish." |
| GPT-6.2 Sol | `gpt-6.2-sol` | 1.05M | "Our go-to model for everyday work, from coding to powering agents at scale." |
| GPT-6.1 Terra | `gpt-6.1-terra` | 1.05M | "A fast, efficient model for visual reasoning, precise computer use, and clear, natural writing." |
| GPT-6 Luna | `gpt-6-luna` | 1.05M | "Our most efficient model for focused, high-volume tasks." |

**GPT-6 Astra (`gpt-6-astra`) and GPT-6.1 Sol (`gpt-6.1-sol`) are superseded** in the flagship list by `gpt-6.2-astra` and `gpt-6.2-sol`. The `gpt-6-astra` page is still published and does not call itself deprecated: "1,050,000 context window", "128,000 max output tokens", "Apr 30, 2026 knowledge cutoff", reasoning effort "`low`, `medium`, `high`, `xhigh`, and `max`", described as "A reasoning model for complex coding and professional work." No per-model page for the 6.2 models was read; do not quote max output or cutoff for them.
Source: <https://developers.openai.com/api/docs/models/gpt-6-astra>

**Specialized models also listed:** `gpt-6-cyber` ("Investigate a vulnerability, reproduce it in an authorized test environment, or verify a fix."), `gpt-5.6-cyber` ("Cybersecurity model for authorized vulnerability research and security testing."), GPT-Rosalind ("Life sciences reasoning for approved organizations", no slug shown — the `gpt-rosalind-research` slug recorded in 1.9.0 is no longer on the page), the image models below, and the voice/realtime/transcription family (`gpt-live-1.1`, `gpt-realtime-2.1`, `gpt-realtime-2.1-mini`, `gpt-realtime-translate`, `gpt-transcribe`, `gpt-live-transcribe`, `gpt-realtime-whisper`). `gpt-live-1`, `gpt-realtime-2` and `gpt-realtime-1.5` are no longer listed; treat them as legacy. Context windows are stated only for the four flagship models. **No model on the page is marked Deprecated** any longer; the four recorded as Deprecated in 1.9.0 (`gpt-realtime-mini`, `gpt-4o-mini-tts`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`) are not listed — treat them as legacy.

**The GPT-5.6 general-purpose tier is superseded.** `gpt-5.6-sol`, `gpt-5.6-terra` and `gpt-5.6-luna` are not listed on the current model page; `gpt-6.2-sol`, `gpt-6.1-terra` and `gpt-6-luna` hold those slots. Treat the 5.6 general-purpose slugs as legacy and route them at family level. `gpt-5.6-cyber` is still listed, as a specialized model.

**Reasoning effort.** "Supported values are model-dependent and can include `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`." GPT-6 Astra "does not support `none` reasoning effort." GPT-6.1 Sol "does not support `none` or `minimal` and defaults to `medium`." GPT-6.2 Astra and GPT-6.2 Sol "reject requests that set `reasoning.effort` (Responses) or `reasoning_effort` (Chat Completions) to `none`." No default is stated for the 6.2 models. Responses API uses `reasoning.effort`; Chat Completions uses `reasoning_effort`.
Source: <https://developers.openai.com/api/docs/guides/reasoning>

**Other reasoning controls.** `reasoning.context` accepts `auto`, `current_turn`, `all_turns`. "GPT-5.6 and GPT-6 models support `standard` and `pro` reasoning modes in the Responses API."; `standard` is the default.
Source: <https://developers.openai.com/api/docs/guides/reasoning>

**Raw reasoning is not exposed.** Verbatim: "While reasoning tokens are not visible via the API, they still occupy space in the model's context window". **The `summary` parameter is documented again**: "you can view a summary of the model's reasoning using the `summary` parameter." Values on the page: `auto` ("To access the most detailed summarizer available for a model, set the value of this parameter to `auto`."; "`auto` will be equivalent to `detailed` for most reasoning models today."), `concise` and `detailed`. A summary is an API setting the user opts into, not prompt content; still ask for conclusions, assumptions and checks in the output contract.
Source: <https://developers.openai.com/api/docs/guides/reasoning>

**Legacy.** `o3` and `o4-mini` are not listed in the current model documentation. Treat them as legacy: route them at family level under reasoning-native models and do not quote defaults for them.
Source: <https://developers.openai.com/api/docs/models>

**No verbosity parameter** is documented on the current model pages. Control visible length through the output contract.
Sources: <https://developers.openai.com/api/docs/guides/reasoning>, <https://developers.openai.com/api/docs/models>

---

## Google Gemini

Source: <https://aistudio.google.com/docs/models>

> Source URL changed on 2026-11-23. `https://ai.google.dev/gemini-api/docs/models` now answers 301 Moved Permanently to `https://aistudio.google.com/docs/models`. Read the latter.

| Model | API ID | Status on page | Documented role |
|-------|--------|----------------|-----------------|
| Gemini 4 Carbon | `gemini-4-carbon` | No label | "Our strongest reasoning model, built for complex software engineering, multimodal knowledge work" |
| Gemini 4 Neon | `gemini-4-neon` | No label | "Frontier-level intelligence with fast end-to-end task completion across complex software engineering" |
| Gemini 4 Hydrogen | `gemini-4-hydrogen` | No label | "Brings cutting-edge intelligence to everyone, with speed and efficiency for everyday coding and agentic workflows." |
| Gemini 4 Argon | `gemini-4-argon` | No label | "Our efficient Gemini 4 frontier reasoning model, delivering faster responses and lower token spend per turn" |
| Gemini 3.8 Flash | `gemini-3.8-flash` | Stable | "Our previous-generation Flash model for software engineering, autonomous agents, and complex enterprise workflows." |
| Gemini 3.8 Live | `gemini-3.8-live` | New | "Default Live API model for most low-latency voice agent experiences without reasoning delays." |
| Gemini 3.8 Live Extended Thinking | `gemini-3.8-live-extended-thinking` | New | "High-reasoning Live API model for voice interactions, recommended when higher background reasoning is required." |
| Gemini 3.8 Flash TTS | `gemini-3.8-flash-tts` | New | "Flagship creative text-to-speech model for studio-grade voice fidelity, expressive acting, Voice design" |
| Gemini 3.8 Flash-Lite TTS | `gemini-3.8-flash-lite-tts` | New | "Fast, cost-efficient text-to-speech model for high-volume production, real-time voice agent cascades, and Voice replication." |
| Gemini 3.6 Flash | `gemini-3.6-flash` | Stable | "Our previous-generation Flash model, balancing speed and multimodal capabilities across general agentic and everyday tasks." |
| Gemini 3.5 Flash-Lite | `gemini-3.5-flash-lite` | Stable | "Our fastest, most cost-effective 3.5 model for high-throughput execution." |
| Gemini 3.1 Flash-Lite | `gemini-3.1-flash-lite` | Stable | "Frontier-class performance rivaling larger models at a fraction of the cost." |
| Gemini 3.5 Transcribe | `gemini-3.5-transcribe`, `gemini-3.5-transcribe-live` | Stable | "Low-latency speech-to-text model with utterance-based language detection, speaker diarization, and word timestamps." |
| Gemini Omni Flash | `gemini-omni-1.2-flash`, `gemini-omni-1.1-flash` | New | "Generate and edit up to 15 seconds of video with native audio, keyframe interpolation, video extension" |
| Genie 4 | `genie-4` | New | "Stream real-time, steerable 24 fps interactive worlds with synchronized 48 kHz stereo audio over WebRTC and WebSockets." |
| Nano Banana 2.1 | `gemini-nano-banana-2.1` | New | "High-efficiency image generation and editing model with improved visual quality, typography, and multi-turn consistency." |
| Nano Banana 2 | `gemini-3.1-flash-image` | Stable | "Powerful, high-efficiency image generation and editing, optimized for speed and high-volume use cases." |
| Nano Banana 2 Lite | `gemini-3.1-flash-lite-image` | Stable | "Ultra-low latency and cost-effective image generation and editing, designed for high-volume interactive use cases." |
| Nano Banana Pro | `gemini-3-pro-image` | Stable | "State-of-the-art image generation and editing models for highly contextual native image creation." |
| Gemini 3 Flash (preview) | `gemini-3-flash-preview` | Preview | "Frontier-class performance rivaling larger models at a fraction of the cost." |
| Gemini 3.5 Live Translate (preview) | `gemini-3.5-live-translate-preview` | Preview | "Low-latency, real-time speech to speech translation model that supports 70+ languages." |
| Gemini 3.1 Pro (preview) | `gemini-3.1-pro-preview` | No label | No description given |

The page also lists music (`lyria-3.5`, `lyria-3-clip-preview`, `lyria-3-pro-preview`, `lyria-realtime-exp`), agent (`deep-research-preview-04-2026`, `deep-research-max-preview-04-2026`, `antigravity-preview-09-2026`) and specialized models (`gemini-decision-1`, `gemini-embedding-2`, `gemini-embedding-001`, `gemini-robotics-er-2-preview`). State no parameters for them.

**Context window.** For the Gemini 4 models the page states "1M tokens" of context and "64K / 1M tokens" of max output. The 1.9.0 Argon line ("unified 1M context window and long decodes up to 1M tokens") is gone: Argon is no longer the flagship but the efficient Gemini 4 model. No current model outside Gemini 4 states a context window — do not quote a figure for any of them.

**Gemini 3.8 Flash is now "previous-generation".** The 1.9.0 line "Our most intelligent Flash model" is gone; Gemini 3.6 Flash carries the same "previous-generation Flash" wording. Route new builds to the Gemini 4 models.

**Gemini 3.7 Flash (`gemini-3.7-flash`) and Gemini 3.5 Flash (`gemini-3.5-flash`) are not listed.** Treat both as superseded; do not quote a slug or role line for them. `gemini-3.5-flash-lite` is still listed and stable.

**The Gemini 2.5 family.** `gemini-2.5-flash` and `gemini-2.5-pro` are now marked **Deprecated**. Access is limited: "To ensure reliable performance for everyone, we are limiting access to the 2.5 models to users who have actively used them". "`gemini-2.5-flash-lite` is not deprecated and will continue to be served until further notice through the API." For new projects the page names "Gemini 4 Hydrogen or 3.5 Flash-Lite". Do not route a new build to a 2.5 model.

**Legacy preview and shut-down entries.** `gemini-3.1-flash-live-preview` ("Legacy Live API preview model. We recommend updating to Gemini 3.8 Live.") and `gemini-3.1-flash-tts-preview` ("Legacy TTS preview model. We recommend updating to Gemini 3.8 Flash TTS or Gemini 3.8 Flash-Lite TTS.") are legacy previews. Marked **Shut down**: `gemini-robotics-er-1.6-preview`, `gemini-2.5-computer-use-preview-10-2025`, `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-3.1-flash-lite-preview`, `gemini-3-pro-preview`. `imagen-4.0-generate`, recorded as Shut down in 1.9.0, was not seen in the 2026-11-23 read; treat it as shut down.

**Few-shot.** "We recommend to always include few-shot examples in your prompts. Prompts without few-shot examples are likely to be less effective."
**Context placement.** "When providing large amounts of context (e.g., documents, code), supply all the context first. Place your specific instructions or questions at the very end of the prompt."
Source: <https://aistudio.google.com/docs/prompting-strategies> (`https://ai.google.dev/gemini-api/docs/prompting-strategies` redirects there; wording unchanged on 2026-11-23)

---

## xAI Grok

Source: <https://docs.x.ai/docs/models>

| Model | API slug | Context |
|-------|----------|---------|
| Grok 4.7 | `grok-4.7` | 500k |

Documented as "It is the most capable model we've built." Verbatim: "The knowledge cut-off date of Grok 4.7 is May 2026." Image input (stated for image input models in general): maximum `20MiB` per image, no limit on the number of images, `jpg/jpeg` or `png`. For current facts: "To incorporate realtime data with your request, enable server-side search tools (Web Search / X Search)." The page no longer states that reasoning is configurable; it notes only that `grok-4.7` always returns `reasoning.encrypted_content` on the Responses API.

**Other text models in the pricing table**, with no description, cutoff or status label: `grok-4.6` (500k), `grok-4.5` (500k), `grok-4.3` (1M), `grok-4.20-0309-reasoning` (1M), `grok-4.20-0309-non-reasoning` (1M), `grok-build-0.1` (500k), `grok-4.20-multi-agent-0309` (1M). `grok-4.6`, recorded as no longer listed in 1.9.0, is back in that table but unlabeled; still route new work to `grok-4.7`. The two retirement notices recorded in 1.9.0 are no longer on the page. Verbatim: "`logprobs` and `top_logprobs` are not supported by models `grok-4.20` and newer." "These fields will be silently ignored if set."

Also listed, without context, cutoff or role lines: `grok-imagine-image`, `grok-imagine-image-2.0`, `grok-imagine-video`, `grok-imagine-video-1.5`, `grok-imagine-video-1.5-lite`, `grok-voice-3.0`, and `grok-voice-2.0` (marked Deprecated). State no parameters for these — the models page gives none.

---

## MiniMax

Sources: <https://platform.minimax.io/docs/api-reference/text-openai-api>, <https://platform.minimax.io/docs/api-reference/text-anthropic-api>

| Model | Context |
|-------|---------|
| MiniMax-M3.1-Flash | 1,000,000 |
| MiniMax-M3 | 1,000,000 |

Only these two models are listed. **`MiniMax-M3.1-Flash-Preview` has become `MiniMax-M3.1-Flash`**, and the whole M2.x range (M2.7, M2.5, M2.1, M2 and their `-highspeed` variants, all 204,800) **is no longer on either page**. Do not quote a context size for an M2.x model; route it at family level.

**Temperature is now documented as ignored, not ranged.** Verbatim: "Not supported yet; any value passed has no effect. `MiniMax-M3.1-Flash` and `MiniMax-M3` always use 1". The Anthropic-compatible page lists its support status as "Ignored" with the same description. **No valid range is stated on either page** — the `[0, 2]` range recorded in 1.8.0 is gone. Do not tell a user to set MiniMax temperature at all; steer through the prompt.

> Correction carried forward: prompt-master 1.6.0 and 1.8.0 state a temperature range for MiniMax (0–1 and `[0, 2]` respectively). Neither is current. Temperature is ignored and fixed at 1.

---

## Video, voice and 3D

**OpenAI video — Sora 2 is shut down.** Verbatim: "The Sora 2 models and Videos API were shut down on September 24, 2026 and are no longer available.", "No one-to-one replacement API is available." and "This guide is retained for historical reference." Do not build a prompt on `sora-2` or `sora-2-pro`, and do not quote their parameters as current. No replacement OpenAI video model is listed on that page.

Historical, for recognizing an inherited prompt only: the documented guidance was to describe "shot type, subject, action, setting, and lighting", example verbatim — "Wide shot of a child flying a red kite in a grassy park, golden hour sunlight, camera slowly pans upward."; both models "support `16`- and `20`-second generations", with extensions adding up to 20 seconds each, up to six extensions and 120 seconds total; the sizes now named on the page are `1280x720`, with `1920x1080` / `1080x1920` for 1080p exports on `sora-2-pro`. (The fuller landscape list recorded in 1.8.0 — `1024x576`, `960x544`, `848x480` — is no longer on the page. The body of the guide is still written in the present tense, which contradicts its own banner; the banner governs.)
Source: <https://developers.openai.com/api/docs/guides/video-generation>

**ElevenLabs.** Documented current models: **Eleven v4 (`eleven_v4`)**, Eleven v3, Eleven Multilingual v2, Eleven Flash v2.5. `eleven_flash_v2` is the only model the page states is compatible with phoneme tags. Emotion comes from narrative context and dialogue tags, not parameters: "Convey emotions through narrative context or explicit dialogue tags", and "Explicit dialogue tags yield more predictable results than relying solely on context" — "however the model will still speak out the emotional delivery guides", so they are stripped in post if unwanted. Speed: "The default value is 1.0, which means that the speed is not adjusted."; "Values below 1.0 will slow the voice down, to a minimum of 0.7."; "Values above 1.0 will speed up the voice, to a maximum of 1.2." SSML: "Use `<break time=\"x.xs\" />` for natural pauses up to 3 seconds.", but verbatim: "Eleven v4 and Eleven v3 do not support SSML break tags."

"Eleven v4 Turbo", recorded in 1.9.0, no longer appears on the page (checked 2026-11-23); do not name it.

Bracketed audio tags, as documented on 2026-10-26 and unchanged on 2026-11-23:
- Voice: `[laughs]`, `[laughs harder]`, `[starts laughing]`, `[wheezing]`, `[whispers]`, `[sighs]`, `[exhales]`, `[sarcastic]`, `[curious]`, `[excited]`, `[crying]`, `[snorts]`, `[mischievously]`
- Sound effects: `[gunshot]`, `[applause]`, `[clapping]`, `[explosion]`, `[swallows]`, `[gulps]`
- Special: `[strong X accent]`, `[sings]`, `[woo]`, `[fart]`

Documented example sentences: "[whispers] I never knew it could be this way, but I'm glad we're here.", "[applause] Thank you all for coming tonight! [gunshot] What was that?", "[strong French accent] Zat's life, my friend — you can't control everysing."

> **`[sarcastic]` is documented again.** 1.8.0 removed it to *Deliberately unsourced* because it was not on the page on 2026-10-01. It is on the page on 2026-10-26, so it is restored here and struck from that table. The 1.8.0 reading was correct for its date; the page grew the tag set back.
Source: <https://elevenlabs.io/docs/best-practices/prompting>

**Meshy text-to-3D.** `prompt` is required: "Text that describes the object to generate, up to 800 characters. Longer text returns `400`." `mode` is `preview` or `refine`, neither deprecated. `art_style` is **deprecated**, defaults to `realistic`, and the page's own instruction is "Leave it out. Meshy ignores it." — it **no longer names a specific model** as the one that ignores it, so do not state the Meshy-6 carve-out recorded in 1.8.0. **`negative_prompt` is no longer documented on the page at all** — it is not merely inert, it is undocumented, so state nothing about it beyond: carry exclusions in the positive prompt. `topology` is `quad` (quad-dominant mesh) or `triangle` (decimated triangle mesh), **default `triangle`**; Smart Topology output is triangle-only, so **`quad` with `meshy-t2` or `meshy-t2.5` returns 400**. `target_formats` accepts `glb`, `obj`, `fbx`, `stl`, `usdz`, `3mf`.
Source: <https://docs.meshy.ai/en/api/text-to-3d>

---

## Image generation

**Midjourney.** "The current default Midjourney version is V8.2." — default since July 24 2026, succeeding V8.1 (released April 14 2026, default June 10 – July 23 2026); V8.0 is no longer usable. Niji 7 launched January 9 2026. The parameter-list page documents 30 entries, including `--aspect` / `--ar`, `--chaos` / `--c`, `--no`, `--profile` / `--p`, `--quality` / `--q`, `--repeat` / `--r`, `--seed`, `--stealth`, `--raw` (Raw Mode, no shorthand), `--stylize` / `--s`, `--sref`, `--sv`, `--sw`, `--tile`, `--version` / `--v`, `--draft`, `--weird` / `--w`, `--fast`, `--relax`, `--turbo`, `--iw`, `--niji`, `--public`, `--motion low` / `--motion high`, `--loop`, `--end`, `--bs`, `--video`, `--sd` / `--hd`, `--edit`, and `--oref` (noted as replaced by the Edit Model in V8.X). `--style raw` is **not** documented syntax; Raw Mode is `--raw`. Accepted value ranges are not given on the parameter-list page — the only stated values are the Motion options (low or high) and the SD/HD resolutions (1024px and 2048px) — do not quote a range. (The Version page no longer states the Raw Mode spelling; the parameter-list page is the source for it.)
Sources: <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>, <https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List>

**OpenAI image models.** Listed: `gpt-image-2.6-sunburst`, `gpt-image-2.6-flare`, `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare`. The models page describes them as "Image generation and editing for detailed visual work", "Image generation and editing for fast iteration", "Our most capable model for image generation and editing" and "Fast, high-quality everyday image generation". The image-generation guide still advises "Choose Sunburst for workflows where editing precision matters most, and Flare for fast, high-quality everyday" generation. DALL·E 3 is not listed on the current image-generation page; treat it as legacy.
Sources: <https://developers.openai.com/api/docs/guides/image-generation>, <https://developers.openai.com/api/docs/models>

---

## Verbatim extracts — highest-risk figures

Spot-check of 2026-11-23 (Midjourney lines: 2026-10-26, pages returned 403). Each line is reproduced character for character from the source above it, so a future reviewer can confirm the claim without re-fetching.

**MiniMax temperature** — <https://platform.minimax.io/docs/api-reference/text-openai-api>
> "Not supported yet; any value passed has no effect. `MiniMax-M3.1-Flash` and `MiniMax-M3` always use 1."

**MiniMax M3 context** — same page, model table
> "MiniMax-M3 | 1,000,000"

**Claude effort values** — <https://platform.claude.com/docs/en/build-with-claude/effort>
> "`max`: Absolute maximum capability with no constraints on token spending."
> "`xhigh`: Extended capability for long-horizon work."
> "`high`: Spends as many tokens as the task needs for excellent results. The default on every model that supports effort except Claude Opus 5.5 and Claude Haiku 5.5."
> "`medium`: Balanced approach with moderate token savings. The default on Claude Opus 5.5 and Claude Haiku 5.5."
> "`low`: Most efficient. Significant token savings with some capability reduction."

> The `high` and `medium` lines were amended between 2026-10-01 and 2026-10-26 to add Claude Haiku 5.5 to the `medium`-default set. The 1.8.0 extracts, which named Opus 5.5 alone, are no longer character-accurate.
> The earlier phrasings ("Extra high effort is the recommended setting for the hardest coding and agentic use cases", "The default. This setting balances token usage and intelligence") survive on the Sonnet 5 prompting page and should not be quoted as current.

**Claude Haiku 5.5 lineup row** — <https://platform.claude.com/docs/en/models/overview>
> "For high-volume, latency-sensitive tasks such as classification, extraction, and routing"

**Claude Haiku 5.5 thinking off** — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5>
> "You can also turn thinking off with `thinking: {\"type\": \"disabled\"}`. This works at `low`, `medium`, and `high` only. At `xhigh` and `max`, the request returns a 400 error."

**Gemini 4 context** — <https://aistudio.google.com/docs/models>
> "1M tokens"
> "64K / 1M tokens"

Context and max output for the Gemini 4 models. The 1.9.0 Argon extract ("Our flagship reasoning model with a unified 1M context window and long decodes up to 1M tokens.") is no longer on the page.

**OpenAI GPT-6.1 Sol effort** — <https://developers.openai.com/api/docs/guides/reasoning>
> "does not support `none` or `minimal` and defaults to `medium`."

**ElevenLabs speed range** — <https://elevenlabs.io/docs/best-practices/prompting>
> "Values below 1.0 will slow the voice down, to a minimum of 0.7."
> "Values above 1.0 will speed up the voice, to a maximum of 1.2."

**Meshy art_style** — <https://docs.meshy.ai/en/api/text-to-3d>
> "Leave it out. Meshy ignores it."

No model name appears alongside it; `negative_prompt` does not appear on the page.

**Claude sampling parameters** — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5>
> "If you previously relied on `temperature` for stylistic variety, note that setting `temperature`, `top_p`, or `top_k` returns a 400 error on Claude Sonnet 5. This constraint is new for Sonnet-class models. Remove these parameters when migrating, and use system-prompt instructions to guide tone and variety instead."
> "`temperature` is not accepted on Claude Sonnet 5"

The qualifier "to a non-default value", quoted in 1.8.0, is no longer in the sentence. This is stated for Sonnet 5 only. It is absent from the Sonnet 5.5, Opus 5.5, Fable 5.1, Haiku 5.5 and effort pages.

**Claude Sonnet 5.5 thinking floor** — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5>
> "To run Claude Sonnet 5.5 without up-front thinking, send `thinking: {\"type\": \"between_tools\"}`. It's the lowest thinking setting on this model, and it's accepted at `high` effort or below. At `xhigh` or `max` effort, a request with `between_tools` returns a 400 error."

**Midjourney default version** — <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>
> "The current default Midjourney version is V8.2."

**Midjourney Raw Mode** — same page, feature compatibility chart. Spelled `--raw`. The string `--style raw` does not appear.

**Grok 4.7 context** — <https://docs.x.ai/docs/models>, pricing table
> "500k"

**OpenAI image models** — <https://developers.openai.com/api/docs/guides/image-generation>
> "gpt-image-2.5-sunburst"
> "gpt-image-2.5-flare"
> "gpt-image-2.6-flare"
> "Choose Sunburst for workflows where editing precision matters most, and Flare for fast, high-quality everyday"

`gpt-image-2.6-sunburst` appears on this page only in a link URL; the models page lists it by name.

Neither "dall-e-3" nor "DALL·E 3" appears on that page.

---

## Unverified — family-level only

These tools carry prose inherited from prompt-master and never passed through the gate. No official documentation for them was retrieved. Treat every statement about them as durable family-level guidance, never as a sourced fact, and state no version, slug, parameter name or numeric value for any of them:

Runway, Kling, LTX Video, Dream Machine (Luma), SeeDream, Tripo, Rodin, Unity AI, Blender AI add-ons, ComfyUI checkpoint behavior, Zapier, Make, n8n.

`tools-visual.md` marks the same set. When a request targets one of them and exact settings matter, say the details are unverified and route at family level — the Model Recency Gate, step 4.

---

## Deliberately unsourced

These figures appeared in earlier releases and were **removed rather than carried forward**, because no official provider documentation confirming them could be retrieved on 2026-09-21, 2026-10-01 or 2026-10-26. Entries added at 1.9.0 are marked; a struck-through row is one that became sourced again and has moved back into the body.

| Removed claim | Replaced by |
|---------------|-------------|
| Stable Diffusion "CFG 7–12" | "Set guidance scale and step count from the checkpoint's own documented defaults; raise steps for finals." |
| Stable Diffusion "steps 20–30 for drafts, 40–50 for finals" | Same as above |
| Ollama "temperature 0.1 for coding, 0.7–0.8 for creative" | "Lower temperature for deterministic work, higher for creative work; the usable range depends on the loaded model." |
| "system prompts under 200 words" for reasoning models | "Keep the system prompt short and scoped." |
| "Claude Code default is xhigh effort" | Effort is a harness setting — ask which model and effort are selected. |
| "M2.5-highspeed has a 204K context window" (1.6.0, correct but incomplete) | The whole M2.x range has left both API reference pages (1.9.0). State no context size for it. |
| "1M context window on M2.7" | M2.7 is no longer documented at all (1.9.0); M3 is 1,000,000. The 204,800 figure recorded in 1.8.0 had a source then and has none now. |
| "Temperature must be between 0 and 1" (MiniMax) | `[0, 2]`, default `1` |
| Claude max output "128,000 is documented as working well for long agentic tasks" (1.7.x) | Not restated on the best-practices page on 2026-10-01; it now says to prefer lowering effort, or `max_tokens` as a hard limit. 128K remains the documented max output per the model table. |
| ~~ElevenLabs audio tag `[sarcastic]` (1.7.x)~~ | **Restored 1.9.0.** It was absent from the prompting page on 2026-10-01 and is documented again on 2026-10-26, alongside a much larger tag set. See *Video, voice and 3D*. |
| MiniMax temperature range `[0, 2]`, default `1` (1.8.0) | Removed 1.9.0: both MiniMax endpoints now document temperature as ignored and fixed at 1, with no range. |
| Meshy "Requests using Meshy-6 will ignore `art_style`" (1.8.0) | Removed 1.9.0: the page now says only "Leave it out. Meshy ignores it." and names no model. |
| Meshy `negative_prompt` "deprecated and has no functional impact" (1.6.0–1.8.0) | Removed 1.9.0: the field is no longer documented on the page at all. |
| ~~OpenAI reasoning `summary` parameter, values `auto` / `concise` / `detailed` (1.7.x–1.8.0)~~ | **Restored on 2026-11-23.** Absent from the reasoning guide on 2026-10-26, documented again on 2026-11-23 with the same three values. See *OpenAI*. |
| Sora landscape sizes `1024x576`, `960x544`, `848x480` (1.6.0–1.8.0) | Removed 1.9.0: no longer on the (historical) video guide, which now names `1280x720` plus the Pro 1080p sizes. |

The 30% attention-decay placement rule and the 3-question limit are this skill's own editorial conventions, not vendor claims.

# Versioned parameters — single review point

Every model name, API slug, version number, context size and numeric parameter used anywhere in this skill lives here, with the official source it was verified against. **Every section verified 2026-10-26.** Revise this file first at each maintenance cycle; the tool profiles describe durable behavior and should need far fewer edits.

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
| Claude Fable 5.1 | `claude-fable-5-1` | 1M | 128K | `high` | Jun 2026 | "For demanding reasoning and long-horizon agentic work" |
| Claude Opus 5.5 | `claude-opus-5-5` | 1M | 128K | `medium` | Jun 2026 | "For long-running agentic coding and knowledge work" |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M | 128K | `high` | Jun 2026 | "The best combination of speed and intelligence" |
| Claude Haiku 5.5 | `claude-haiku-5-5` | 1M | 128K | `medium` | Jun 2026 | "For high-volume, latency-sensitive tasks such as classification, extraction, and routing" |

Default recommendation, verbatim: "If you're unsure which model to use, start with Claude Opus 5.5 for most workloads. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short."
Per-model row detail: <https://platform.claude.com/docs/en/models/opus-5-5/overview>

**Claude Sonnet 5 is superseded** by Sonnet 5.5 and no longer appears in the current lineup, though its prompting guide is still published. Route an existing Sonnet 5 prompt to Sonnet 5.5 and re-run its effort sweep — the effort levels are documented as recalibrated between the two.

**Claude Opus 5 is superseded** by Opus 5.5 and no longer appears in the current lineup. Do not recommend it; route an existing Opus 5 prompt to Opus 5.5 and re-run its effort sweep.

**Claude Haiku 4.5 no longer holds the Haiku slot** in the lineup table — Haiku 5.5 does. Haiku 4.5 is still named among current models in the best-practices introduction and appears on the overview page only as a Models API example, so treat it as selectable but not the thing to recommend: route a new build, and an existing Haiku 4.5 prompt, to Haiku 5.5. Haiku 5.5 is the first Haiku model with effort levels, and effort replaces the `budget_tokens` thinking budget Haiku 4.5 used.
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5>

**Haiku 5.5 specifics.** Default effort `medium`; `low` is documented for "chat, short tool tasks, and simple, high-volume requests", `high` for "knowledge work, longer agent tasks, and strict instruction following", `xhigh` and `max` "for work where a quality gain on your evals justifies the cost". Thinking is on by default and counts toward `max_tokens`, which "can go up to 128,000". Thinking can be turned off with `thinking: {"type": "disabled"}` "at `low`, `medium`, and `high` only. At `xhigh` and `max`, the request returns a 400 error." A per-message effort change needs the `mid-conversation-output-config-2026-07-01` beta header plus adaptive thinking; with thinking off it returns a 400. Refusals surface as `stop_reason: "refusal"` with categories `cyber`, `frontier_llm`, `bio` or `general_harms`, with no server-side fallback.
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5>

**Effort parameter.** Values `low`, `medium`, `high`, `xhigh`, `max`. `high` is documented as the default "on every model that supports effort except Claude Opus 5.5 and Claude Haiku 5.5"; those two default to `medium`. Opus 5 defaults to `high`. `xhigh` is documented as available on Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 5, Opus 4.8, Opus 4.7, Sonnet 5.5, Sonnet 5 and Haiku 5.5; `max` on that set plus Mythos Preview, Opus 4.6 and Sonnet 4.6. Setting `effort` to a model's default behaves the same as omitting it. Verbatim: "In Anthropic's testing, Claude Opus 5.5 at `medium` matches or exceeds Claude Opus 5 at `high` on coding and knowledge-work evaluations, and on several coding evaluations `low` comes close to it at much lower cost."
Canonical effort page: <https://platform.claude.com/docs/en/build-with-claude/effort>
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5>

**Opus 5.5 breaking changes vs Opus 5.** `thinking: {"type": "disabled"}` and `thinking: {"type": "enabled", "budget_tokens": N}` both return 400 — thinking cannot be disabled and cannot take a manual budget. `tool_choice: {"type": "any"}` and `{"type": "tool", "name": "..."}` return 400; use `"auto"` or `"none"`. The `computer_20251124` tool is unsupported on the Claude API and Google Cloud — migrate to `computer_toolset_20260801`; it continues to work on Amazon Bedrock. Thinking blocks record the model that produced them: Opus 5.5 reads blocks from Opus 5 and earlier Opus, Sonnet and Haiku models, and — on the Claude API and Claude Models on Google Cloud (Google managed) only — from Sonnet 5.5 and Haiku 5.5; it does not read blocks from Fable or Mythos models. Fable 5.1 and Mythos 5.1 read Opus 5.5 blocks on the Claude API; no other model does. Unreadable blocks are dropped before the model sees them, the request still succeeds and they are not billed. For accounts created on or after 2026-08-31 00:00 UTC the API also enforces by default that nothing before a thinking block has changed; replaying a block after such a change returns a 400 unless the `thinking-binding-controls-2026-08-01` beta header is sent with `thinking.block_binding.prefix_mismatch_behavior` set to `"drop_block"`.
Source: <https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5>
Sources: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>, <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5>, <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1>

**Thinking.** Adaptive thinking is the mode on Claude 4.6 and later models and on Claude Mythos Preview. Verbatim: "On Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, and Claude Opus 5.5, thinking is always on and adaptive thinking is the only mode." On Opus 5, thinking can be disabled "only at effort `high` or lower". On Sonnet 5.5 the lowest thinking setting is `thinking: {"type": "between_tools"}`, accepted at `high` effort or below; at `xhigh` or `max` effort a `between_tools` request returns 400, and with it in effect a per-message `output_config.effort` differing from the level in effect also returns 400. On Claude 4.7 and later, setting `budget_tokens` returns a 400 error — prefer lowering effort, or `max_tokens` as a hard ceiling; an extended-thinking `budget_tokens` cap "is still functional on Opus 4.6 and Sonnet 4.6 but is deprecated". On Sonnet 5.5, `between_tools` also takes no other field: `display`, `budget_tokens` or `block_binding` sent with it returns a 400. At `xhigh` and `max` effort these models think longer before replying, so leave room in `max_tokens`.
Sources: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>, <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5>

**Sampling parameters.** Setting `temperature`, `top_p` or `top_k` returns a 400 error **on Claude Sonnet 5** — documented as "new for Sonnet-class models". (The page's wording changed between 2026-10-01 and 2026-10-26: the qualifier "to a non-default value" is gone, and the Design section now states flatly that "`temperature` is not accepted on Claude Sonnet 5".) No equivalent restriction is stated on the Sonnet 5.5, Opus 5.5, Fable 5.1 or effort pages; do not assert one for those models. Steer tone through the system prompt regardless.
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5>

**Examples.** "Include 3–5 examples for best results."
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>

**Models with their own published prompting guide:** eight guides — Fable 5.1 and Mythos 5.1 (shared), Fable 5 and Mythos 5 (shared), Sonnet 5.5, Sonnet 5, Opus 5.5, Opus 5, Opus 4.8, Haiku 5.5. **Sonnet 4.6 no longer has its own guide**; it, Opus 4.7, Opus 4.6 and Haiku 4.5 are named as current models in the introduction but covered only by the general sections.
Source: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>

---

## OpenAI

Source: <https://developers.openai.com/api/docs/models>

| Model | API slug | Context | Documented role |
|-------|----------|---------|-----------------|
| GPT-6 Astra | `gpt-6-astra` | 1,050,000 | "Our most capable model for the most demanding work" |
| GPT-6.1 Sol | `gpt-6.1-sol` | 1,050,000 | "Near-Astra performance for complex work at a lower cost" |
| GPT-6 Luna | `gpt-6-luna` | 1,050,000 | "Our most efficient model for focused, high-volume tasks" |

GPT-6 Astra: 128,000 max output tokens, knowledge cutoff Apr 30 2026, reasoning effort values `low`, `medium`, `high`, `xhigh`, `max`.
Source: <https://developers.openai.com/api/docs/models/gpt-6-astra>

**Specialized models also listed:** `gpt-5.6-cyber` ("Our most advanced cybersecurity model for authorized vulnerability research and security testing"), `gpt-rosalind-research` ("Life sciences reasoning for approved organizations"), the image models below, and the voice/realtime/transcription family (`gpt-live-1`, `gpt-realtime-2.1`, `gpt-realtime-2.1-mini`, `gpt-realtime-2`, `gpt-realtime-translate`, `gpt-realtime-1.5`, `gpt-transcribe`, `gpt-live-transcribe`, `gpt-realtime-whisper`). Context windows are stated only for the three flagship models. Marked **Deprecated**: `gpt-realtime-mini`, `gpt-4o-mini-tts`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`.

**The GPT-5.6 general-purpose tier is superseded.** `gpt-5.6-sol`, `gpt-5.6-terra` and `gpt-5.6-luna` are no longer listed on the current model page; GPT-6.1 Sol and GPT-6 Luna hold the balanced and cost-optimized slots, and no GPT-6 equivalent of Terra is listed. Treat the 5.6 general-purpose slugs as legacy and route them at family level. `gpt-5.6-cyber` is still listed, as a specialized vulnerability-research model.

**Reasoning effort.** "Supported values are model-dependent and can include `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`." GPT-6 Astra "does not support `none` reasoning effort. Setting `reasoning.effort` (Responses) or `reasoning_effort` (Chat Completions) to `none` returns HTTP 400."; it supports `low`, `medium`, `high`, `xhigh`, `max`. GPT-6.1 Sol "does not support `none` or `minimal` and defaults to `medium`." Responses API uses `reasoning.effort`; Chat Completions uses `reasoning_effort`.
Source: <https://developers.openai.com/api/docs/guides/reasoning>

**Other reasoning controls.** `reasoning.context` accepts `auto`, `current_turn`, `all_turns`. `reasoning.mode` accepts `standard` (default) and `pro`.
Source: <https://developers.openai.com/api/docs/guides/reasoning>

**Raw reasoning is not exposed.** Verbatim: "While reasoning tokens are not visible via the API, they still occupy space in" the model's context window, and they are billed as output tokens. **The `summary` parameter is no longer documented on that page** — do not state its values or tell a user to opt into a reasoning summary. Use `reasoning.context` and `reasoning.mode` instead, and ask for conclusions, assumptions and checks in the output contract.
Source: <https://developers.openai.com/api/docs/guides/reasoning>

**Legacy.** `o3` and `o4-mini` are not listed in the current model documentation. Treat them as legacy: route them at family level under reasoning-native models and do not quote defaults for them. `gpt-realtime-mini` is marked Deprecated on the current model page.
Source: <https://developers.openai.com/api/docs/models>

**No verbosity parameter** is documented on the current model pages. Control visible length through the output contract.
Sources: <https://developers.openai.com/api/docs/guides/reasoning>, <https://developers.openai.com/api/docs/models>

---

## Google Gemini

Source: <https://ai.google.dev/gemini-api/docs/models>

| Model | API ID | Status on page | Documented role |
|-------|--------|----------------|-----------------|
| Gemini 4 Argon | `gemini-4-argon` | Stable | "Our flagship reasoning model with a unified 1M context window and long decodes up to 1M tokens" |
| Gemini 3.8 Flash | `gemini-3.8-flash` | New, stable | "Our most intelligent Flash model", for long-horizon software engineering and autonomous agents |
| Gemini 3.8 Live | `gemini-3.8-live` | New, stable | "Default Live API model for most low-latency voice agent experiences without reasoning delays" |
| Gemini 3.8 Live Extended Thinking | `gemini-3.8-live-extended-thinking` | New, stable | "High-reasoning Live API model for voice interactions" |
| Gemini 3.8 Flash TTS | `gemini-3.8-flash-tts` | New, stable | Flagship creative text-to-speech |
| Gemini 3.8 Flash-Lite TTS | `gemini-3.8-flash-lite-tts` | New, stable | Fast, cost-efficient text-to-speech for high-volume pipelines |
| Gemini 3.6 Flash | `gemini-3.6-flash` | Stable | "Our previous-generation Flash model" |
| Gemini 3.5 Flash-Lite | `gemini-3.5-flash-lite` | Stable | "Our fastest, most cost-effective 3.5 model for high-throughput execution" |
| Gemini 3.1 Flash-Lite | `gemini-3.1-flash-lite` | Stable | "Frontier-class performance rivaling larger models at a fraction of the cost" |
| Gemini 3.5 Transcribe | `gemini-3.5-transcribe`, `gemini-3.5-transcribe-live` | New | Low-latency speech-to-text with diarization and word timestamps |
| Gemini Omni Flash | `gemini-omni-1.1-flash` | Stable | Fast video generation, editing and extension with native audio |
| Nano Banana 2.1 | `gemini-nano-banana-2.1` | New, stable | Image generation and editing with improved typography and multi-turn consistency |
| Nano Banana 2 | `gemini-3.1-flash-image` | Stable | Fast, high-efficiency image generation and editing for high-volume use |
| Nano Banana 2 Lite | `gemini-3.1-flash-lite-image` | Stable | Ultra-low-latency, cost-effective image generation and editing |
| Nano Banana Pro | `gemini-3-pro-image` | Stable | "State-of-the-art image generation and editing models" for contextual native image creation |
| Gemini 3 Flash (preview) | `gemini-3-flash-preview` | Preview | "Frontier-class performance rivaling larger models at a fraction of the cost" |
| Gemini 3.1 Pro (preview) | `gemini-3.1-pro-preview` | Preview, all-models table only | No description given |

A context window is stated for **`gemini-4-argon` only: 1M tokens**, with decodes up to 1M. No other current model on that page states one — do not quote a figure for any of them.

**Gemini 3.7 Flash (`gemini-3.7-flash`) is no longer listed.** Treat it as superseded: route to `gemini-3.8-flash` and do not quote a slug or role line for it.

**Gemini 3.5 Flash (`gemini-3.5-flash`) is no longer listed either** — 1.8.0 recorded it as legacy; it has now left the page. `gemini-3.5-flash-lite` is still listed and stable. **The Gemini 2.5 family, including `gemini-2.5-flash`, is access-limited**: the page restricts it to users who have used it before, says it is not deprecated, and directs new projects to Gemini 3.5 Flash-Lite or 3.8 Flash. Do not route a new build to it.

**Legacy preview and shut-down entries.** `gemini-3.1-flash-live-preview` and `gemini-3.1-flash-tts-preview` are marked Legacy, Preview, with the page recommending the 3.8 equivalents. Marked **Shut down**: `imagen-4.0-generate`, `gemini-robotics-er-1.6-preview`, `gemini-2.5-computer-use-preview-10-2025`, `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-3.1-flash-lite-preview`, `gemini-3-pro-preview`.

**Few-shot.** "We recommend to always include few-shot examples in your prompts. Prompts without few-shot examples are likely to be less effective."
**Context placement.** "When providing large amounts of context (e.g., documents, code), supply all the context first. Place your specific instructions or questions at the very end of the prompt."
Source: <https://ai.google.dev/gemini-api/docs/prompting-strategies>

---

## xAI Grok

Source: <https://docs.x.ai/docs/models>

| Model | API slug | Context |
|-------|----------|---------|
| Grok 4.7 | `grok-4.7` | 500K |

Documented as "Our flagship model for code and everything else". Knowledge cutoff May 2026. Image input accepted up to 20 MiB per image, no limit on quantity, jpg/jpeg or png. Reasoning is configurable. Base model has no knowledge of current events beyond training data unless Web Search or X Search tools are enabled.

**Grok 4.6 is superseded** by Grok 4.7 and no longer listed. Do not quote a slug or cutoff for it. The page names no model as legacy, but links two retirement notices ("Model Retirement (May 15, 2026)", "Imagine Image Quality Retirement (Nov 2, 2026)") whose contents were not read, and notes that `logprobs` / `top_logprobs` are unsupported on `grok-4.20` and newer.

Also listed, without context, cutoff or role lines: `grok-imagine-image-2.0` (Imagine API, image generation and editing) and `grok-imagine-video-1.5` (Imagine API, video generation), plus a Grok Voice API covering real-time conversation, speech-to-text and text-to-speech. State no parameters for these — the models page gives none.

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

**ElevenLabs.** Documented current models: **Eleven v4 (`eleven_v4`), Eleven v4 Turbo**, Eleven v3, Eleven Multilingual v2, Eleven Flash v2.5. `eleven_flash_v2` is the only model the page states is compatible with phoneme tags. Emotion comes from narrative context and dialogue tags, not parameters: "Convey emotions through narrative context or explicit dialogue tags", and "Explicit dialogue tags yield more predictable results than relying solely on context" — "however the model will still speak out the emotional delivery guides", so they are stripped in post if unwanted. Speed: "The default value is 1.0, which means that the speed is not adjusted."; "Values below 1.0 will slow the voice down, to a minimum of 0.7."; "Values above 1.0 will speed up the voice, to a maximum of 1.2." SSML: "Use `<break time=\"x.xs\" />` for natural pauses up to 3 seconds.", but verbatim: "Eleven v4 and Eleven v3 do not support SSML break tags."

Bracketed audio tags, as documented on 2026-10-26 — a substantially longer set than 1.8.0 recorded:
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

**OpenAI image models.** Current: `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare` — "Choose Sunburst for workflows where editing precision matters most, and Flare for fast, high-quality everyday image generation." The models page describes them as "Our most capable model for image generation and editing." and "Fast, high-quality everyday image generation." DALL·E 3 is not listed on the current image-generation page; treat it as legacy.
Source: <https://developers.openai.com/api/docs/guides/image-generation>

---

## Verbatim extracts — highest-risk figures

Spot-check of 2026-10-26. Each line is reproduced character for character from the source above it, so a future reviewer can confirm the claim without re-fetching.

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

**Gemini 4 Argon context** — <https://ai.google.dev/gemini-api/docs/models>
> "Our flagship reasoning model with a unified 1M context window and long decodes up to 1M tokens."

This is the only per-model context figure on that page.

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

**Grok 4.7 context** — <https://docs.x.ai/docs/models>
> "500k tokens"

**OpenAI image models** — <https://developers.openai.com/api/docs/guides/image-generation>
> "gpt-image-2.5-sunburst"
> "gpt-image-2.5-flare"
> "Choose Sunburst for workflows where editing precision matters most, and Flare for fast, high-quality everyday image generation."

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
| OpenAI reasoning `summary` parameter, values `auto` / `concise` / `detailed` (1.7.x–1.8.0) | Removed 1.9.0: not documented on the reasoning guide on 2026-10-26. `reasoning.context` and `reasoning.mode` are what the page documents. |
| Sora landscape sizes `1024x576`, `960x544`, `848x480` (1.6.0–1.8.0) | Removed 1.9.0: no longer on the (historical) video guide, which now names `1280x720` plus the Pro 1080p sizes. |

The 30% attention-decay placement rule and the 3-question limit are this skill's own editorial conventions, not vendor claims.

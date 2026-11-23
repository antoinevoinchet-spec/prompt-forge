# Tool profiles — image, 3D, video, voice, workflow

Read this file only when the target tool produces an image, a 3D asset, a video, audio, or an automation. Model names, version parameters and numeric values: `params.md`.

**Verification status.** Midjourney, GPT Image, ElevenLabs and Meshy are verified against official documentation (Sora is verified as shut down — see below) and their figures live in `params.md`. Everything else here — Runway, Kling, LTX Video, Dream Machine, SeeDream, Tripo, Rodin, Unity AI, Blender add-ons, ComfyUI checkpoint behavior, Zapier, Make and n8n — is unverified prose inherited from prompt-master. For those, give durable family-level guidance, state no version, slug, parameter name or numeric value, and tell the user the details are unverified.

## Contents

- [Image generation](#image-generation)
- [Image editing from a reference](#image-editing-from-a-reference)
- [ComfyUI](#comfyui)
- [3D — text to asset](#3d--text-to-asset)
- [3D — in-engine assistants](#3d--in-engine-assistants)
- [Video](#video)
- [Voice](#voice)
- [Workflow automation](#workflow-automation)
- [Old patterns](#old-patterns)

---

## Image generation

First detect the intent: generating from scratch, or editing an existing image? Editing routes to the next section.

**Midjourney.** Comma-separated descriptors, not prose. Subject first, then style, mood, lighting, composition. Parameters go at the end. Exclude elements with `--no [unwanted elements]`. Current default version and the documented parameter list: `params.md` — state a version only when the user needs one pinned, and use the documented spelling.

**GPT Image (OpenAI).** Prose description works. Describe foreground, midground and background separately for complex compositions. Add "do not include text in the image unless specified." Current model slugs and which to pick: `params.md`.

**Stable Diffusion.** Weighted syntax `(word:weight)`. A negative prompt is mandatory. Set guidance scale and step count from the checkpoint's own documented defaults; raise the step count for finals over drafts. Do not quote a fixed range — it varies by checkpoint and sampler.

**SeeDream.** Strong at artistic and stylized output. Name the art style explicitly — anime, cinematic, painterly — before the scene content. Mood and atmosphere descriptors work well. A negative prompt is recommended.

**Nano Banana (Gemini image).** Routes through the Gemini API; see `params.md` for the current model ID. Prose description, and the Gemini context-placement rule applies: reference material first, instruction last.

---

## Image editing from a reference

Detect when the user says change, edit, modify or adjust something in an existing image, or supplies a reference.

Always instruct the user to attach the reference image to the tool first. Then build the prompt around the delta only: what changes, and what must stay identical. Naming what stays fixed is what prevents the tool regenerating the whole image. Use Template J.

---

## ComfyUI

A node-based workflow, not a single prompt box. Ask which checkpoint model is loaded before writing — the prompt syntax and the usable parameter values both follow from it.

Always output two separate blocks, Positive Prompt and Negative Prompt. Never merge them. Use Template K.

---

## 3D — text to asset

Meshy, Tripo, Rodin.

Describe: style keyword (low-poly, realistic, stylized cartoon) + subject + key features + primary material + texture detail + technical spec. Put everything that matters into the positive prompt — on Meshy there is no documented negative-prompt field to fall back on, so never route an exclusion through one in this category without checking `params.md` first.

- **Meshy** *(verified)* — game assets and team workflows. Its `negative_prompt` field is **no longer documented at all**, and its art-style field is **deprecated and ignored**, with the documentation's own instruction being to leave it out — so exclusions and style must be carried by the prompt text itself. Topology has a default and one combination that is rejected outright; prompt length cap, topology options and export formats: `params.md`.
- **Tripo** *(unverified)* — fastest for clean topology; rapid prototyping and concept assets.
- **Rodin** *(unverified)* — highest quality for photorealistic work; slower and more expensive.

Specify the intended export use: game engine, 3D printing, web. For characters that will be rigged, specify A-pose or T-pose.

---

## 3D — in-engine assistants

**Unity AI.** Route by intent: documentation and project queries, automation of repetitive Editor tasks, and C# generation or review are distinct modes. Be precise about exactly what must happen in the Editor. For the generators — sprite, texture, animation — state the asset type, art style, and the technical constraints: resolution, color palette, and whether an animation loops or plays once.

**Blender AI add-ons.** These generate Python that executes in Blender. Be specific about geometry, material names and scene context. Say whether the script applies to the selected object or the entire scene.

---

## Video

- **Sora** *(verified — shut down)* — the Sora 2 models and the Videos API were shut down on 2026-09-24 and are no longer available, and no replacement OpenAI video model is listed. Do not build a prompt on `sora-2` or `sora-2-pro`. If the user names Sora, say the API is retired, offer to write the prompt for another video tool at family level, and keep the durable shape — shot type, subject, action, setting, lighting, camera motion — which still transfers. See `params.md`.
- **Runway** *(unverified)* — responds to cinematic language; reference film styles for a consistent aesthetic. Name no version.
- **Kling** *(unverified)* — strong at realistic human motion; describe body movement explicitly and specify camera angle and shot type.
- **LTX Video** *(unverified)* — fast and prompt-sensitive; keep descriptions concise and visual, and specify resolution and motion intensity qualitatively.
- **Dream Machine (Luma)** *(unverified)* — cinematic; reference lighting setups, lens types and color grading.

---

## Voice

**ElevenLabs** *(verified)*. Ask which model version is in use before writing — the pause syntax differs between generations, and the wrong one is silently spoken aloud. Emotion is carried by narrative context and dialogue tags rather than a parameter, and the model vocalizes those tags unless they are stripped afterwards. Pacing has a speed setting; emphasis comes from punctuation, ellipses and capitalization. The documented tag vocabulary covers voice behavior, sound effects and accents and is wider than a handful of emotion tags — take it from `params.md` rather than inventing a tag, since an undocumented bracketed phrase is read aloud. Exact ranges, the SSML break syntax and the bracketed audio tags, with which generation accepts which: `params.md`.

---

## Workflow automation

Zapier, Make, n8n.

*(unverified — no official documentation retrieved for these three.)*

Trigger app + trigger event → action app + action + field mapping, step by step. Number each step and state what data passes between them. Note auth requirements explicitly — "assumes [app] is already connected" — and never put a key or token in the prompt.

---

## Old patterns

<details>
<summary>Superseded guidance kept for recognition only — do not apply</summary>

- **"DALL·E 3"** is no longer listed on OpenAI's current image-generation page. Route to the current GPT Image models in `params.md`.
- **"Unity AI (Unity 6.2+, replaces retired Muse)."** The Muse migration is no longer useful context.
- **"`--v 6 --style raw`."** `--style raw` is not documented Midjourney syntax; Raw Mode is `--raw` — the parameter-list page is now the only source for that spelling, the Version page having dropped it — and the default version has moved on. See `params.md`.
- **"`--oref` is the way to carry a subject reference."** The parameter list notes it as replaced by the Edit Model in V8.X. See `params.md`.
- **"CFG 7–12, steps 20–30 for drafts, 40–50 for finals."** Removed: no official source confirms these as general defaults, and they vary by checkpoint and sampler.
- **"3D negative prompts are supported — use them."** Wrong for Meshy, whose field is not documented at all as of 2026-10-26 (1.6.0–1.8.0 recorded it as deprecated and inert; it has since left the page). Carry exclusions in the positive prompt.
- **"Meshy-6 ignores `art_style`, other models honor it."** Narrowed to the general rule: `art_style` is deprecated and ignored, with no model named. See `params.md`.
- **"ElevenLabs does not document `[sarcastic]`."** Reversed. It is documented again as of 2026-10-26, within a larger tag set. See `params.md`.
- **"ElevenLabs: use SSML-like markers for emphasis."** Half wrong: SSML breaks work on the older model generations and not on the current two, which use bracketed audio tags instead. Ask which version is in use.
- **"Sora is deprecated — check before building."** Superseded by the fact: it is shut down, not deprecated. There is nothing left to check against, so do not offer a Sora prompt at all.

</details>

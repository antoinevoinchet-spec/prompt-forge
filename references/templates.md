# Prompt templates reference

Full template library for Prompt Forge. Read the one template that matches the user's task type. Do not load all templates at once.

Terminology follows SKILL.md: scope lock, action boundaries, completion criteria, progress evidence. Any model name or numeric value belongs in `params.md` — never hardcode one into a template.

## Table of Contents

| Template | Best For |
|----------|----------|
| [A — RTF](#template-a--rtf) | Simple one-shot tasks |
| [B — CO-STAR](#template-b--co-star) | Professional documents, business writing |
| [C — RISEN](#template-c--risen) | Complex multi-step projects |
| [D — CRISPE](#template-d--crispe) | Creative work, brand voice |
| [E — Auditable Reasoning](#template-e--auditable-reasoning) | Logic, math, analysis, debugging |
| [F — Few-Shot](#template-f--few-shot) | Consistent structured output, pattern replication |
| [G — File-Scope](#template-g--file-scope) | Cursor, Windsurf, Copilot — code editing AI |
| [H — ReAct + Action Boundaries](#template-h--react--action-boundaries) | Claude Code, Codex, Devin — autonomous agents |
| [I — Visual Descriptor](#template-i--visual-descriptor) | Midjourney, GPT Image, Stable Diffusion, Sora |
| [J — Reference Image Editing](#template-j--reference-image-editing) | Editing an existing image with a reference |
| [K — ComfyUI](#template-k--comfyui) | ComfyUI node-based image workflows |
| [L — Prompt Decompiler](#template-l--prompt-decompiler) | Breaking down, adapting, or splitting existing prompts |
| [M — Adaptive-Thinking Task Brief](#template-m--adaptive-thinking-task-brief) | Complex, multi-step or agentic task on any model with adaptive thinking and an effort control |

---

## Template A — RTF

*Role, Task, Format. Use for fast one-shot tasks where the request is clear and simple.*

```
Role: [One sentence defining who the AI is]
Task: [Precise verb + what to produce]
Format: [Exact output format and length]
```

**Example:**
```
Role: You are a senior technical writer.
Task: Write a one-paragraph description of what a REST API is.
Format: Plain prose, 3 sentences maximum, no jargon, suitable for a non-technical audience.
```

---

## Template B — CO-STAR

*Context, Objective, Style, Tone, Audience, Response. Use for professional documents, business writing, reports, and marketing content where full context control matters.*

```
Context: [Background the AI needs to understand the situation]
Objective: [Exact goal — what success looks like]
Style: [Writing style: formal / conversational / technical / narrative]
Tone: [Emotional register: authoritative / empathetic / urgent / neutral]
Audience: [Who reads this — their knowledge level and expectations]
Response: [Format, length, and structure of the output]
```

**Example:**
```
Context: I am a founder pitching a B2B SaaS tool that automates expense reporting for mid-size companies.
Objective: Write a cold email that gets a reply from a CFO.
Style: Direct and conversational, not salesy.
Tone: Confident but not pushy.
Audience: CFO at a 200-person company, busy, skeptical of vendor emails.
Response: 5 sentences max. Subject line included. No bullet points.
```

---

## Template C — RISEN

*Role, Instructions, Steps, End Goal, Narrowing. Use for complex projects, multi-step tasks, and any output that requires a clear sequence of actions.*

```
Role: [Expert identity the AI should adopt]
Instructions: [Overall task in plain terms]
Steps:
  1. [First action]
  2. [Second action]
  3. [Continue as needed]
End Goal: [What the final output must achieve]
Narrowing: [Constraints, scope limits, what to exclude]
```

**Example:**
```
Role: You are a product manager with 10 years of experience in mobile apps.
Instructions: Write a product requirements document for a habit tracking feature.
Steps:
  1. Define the problem statement in one paragraph
  2. List user stories in the format "As a [user], I want [goal] so that [reason]"
  3. Define acceptance criteria for each story
  4. List out-of-scope items explicitly
End Goal: A PRD that an engineering team can begin sprint planning from immediately.
Narrowing: No technical implementation details. No wireframes. Under 600 words total.
```

---

## Template D — CRISPE

*Capacity, Role, Insight, Statement, Personality, Experiment. Use for creative work, brand voice writing, and any task where personality, tone, and iteration matter.*

```
Capacity: [What capability or expertise the AI should have]
Role: [Specific persona to adopt]
Insight: [Key background insight that shapes the response]
Statement: [The core task or question]
Personality: [Tone and style — witty / authoritative / casual / sharp]
Experiment: [Request variants or alternatives to explore]
```

**Example:**
```
Capacity: Expert copywriter specializing in SaaS product launches.
Role: Brand voice for a productivity tool aimed at developers.
Insight: Developers hate marketing speak and respond to honesty and specificity.
Statement: Write the hero headline and sub-headline for the landing page.
Personality: Sharp, dry, confident — no adjectives, no exclamation marks.
Experiment: Give 3 variants ranging from minimal to bold.
```

---

## Template E — Auditable Reasoning

*Use for logic-heavy tasks, math, debugging, and multi-factor analysis where the result must be checkable without requesting private reasoning.*

```
[Task statement]

Return:
1. Conclusion
2. Assumptions
3. Evidence or intermediate results needed to audit the conclusion
4. Verification checks performed
5. Remaining uncertainty, if any

Do not reveal hidden chain-of-thought or private reasoning. Keep the rationale concise and decision-relevant.
```

**When to use:**
- Debugging where the cause is not obvious
- Comparing technical approaches
- Math or calculation requiring verification
- Analysis where evidence and assumptions must be inspectable

**When NOT to use:**
- Simple tasks where the answer is clear
- Creative tasks where an audit trail adds noise

---

## Template F — Few-Shot

*Use when the output format is easier to show than describe. Examples outperform written instructions for format-sensitive tasks every time.*

```
[Task instruction]

Here are examples of the exact format needed:

<examples>
  <example>
    <input>[example input 1]</input>
    <output>[example output 1]</output>
  </example>
  <example>
    <input>[example input 2]</input>
    <output>[example output 2]</output>
  </example>
</examples>

Now apply this exact pattern to: [actual input]
```

**Rules:**
- A few well-chosen examples beat more of them. Official Claude guidance is 3–5; see `params.md`.
- Examples must include edge cases, not just easy cases.
- Wrap examples in XML tags — Claude parses them reliably, and other models tolerate them.
- If you have been re-prompting for the same formatting correction twice, switch to few-shot instead of rewriting instructions.

---

## Template G — File-Scope

*Use for Cursor, Windsurf, GitHub Copilot, and any AI that edits code inside a codebase. The most common failure mode here is editing the wrong file or breaking existing logic — this template prevents both.*

```
File: [exact/path/to/file.ext]
Function/Component: [exact name]

Current Behavior:
[What this code does right now — be specific]

Desired Change:
[What it should do after the edit — be specific]

Scope lock:
Only modify [function / component / section].
Leave unchanged: [list everything that must not be touched]

Constraints:
- Language/framework: [specify version]
- Do not add dependencies not in [package.json / requirements.txt]
- Preserve existing [type signatures / API contracts / variable names]

Completion criteria:
[Exact, checkable condition that confirms the change worked]
```

---

## Template H — ReAct + Action Boundaries

*Use for Claude Code, Codex, Devin, and any tool that takes autonomous actions. Runaway loops and scope explosion are the most expensive failures in agentic workflows — action boundaries are not optional.*

```
Objective:
[Single, unambiguous goal in one sentence]

Starting State:
[Current file structure / codebase state / environment]

Target State:
[What should exist when the agent is done]

Scope lock:
- Work only inside [directory/scope]
- Install only packages already listed in [requirements.txt / package.json]

Action boundaries:
Proceed on reversible, in-scope inspection, edits and validation.
Stop and ask before:
- Deleting any file, or replacing one without showing a diff first
- Running the dev server, deploying, or pushing to git
- Integrating a new external service or API
- Choosing between two valid implementation paths when the choice affects architecture
- Retrying an error a third time
- Any change outside the stated scope

Progress evidence:
After each major step, output: ✅ [what was completed] — [file(s) affected], grounded in an actual tool result.
At the end, output a full summary of every file changed.
```

---

## Template I — Visual Descriptor

*Use for Midjourney, GPT Image, Stable Diffusion, Sora, Runway, and any image or video generation tool. Current model names and version parameters: `params.md`.*

```
Subject: [Main subject — specific, not vague]
Action/Pose: [What the subject is doing]
Setting: [Where the scene takes place]
Style: [photorealistic / cinematic / anime / oil painting / vector / etc.]
Mood: [dramatic / serene / eerie / joyful / etc.]
Lighting: [golden hour / studio / neon / overcast / candlelight / etc.]
Color Palette: [dominant colors or named palette]
Composition: [wide shot / close-up / aerial / Dutch angle / etc.]
Aspect Ratio: [16:9 / 1:1 / 9:16 / 4:3]
Negative Prompts: [blurry, watermark, extra fingers, distortion, low quality]
Style Reference: [artist / film / aesthetic reference if applicable]
```

**Tool-specific syntax:**
- **Midjourney**: Comma-separated descriptors, not prose. Put parameters at the end — `--ar`, `--no`, and `--raw` for Raw Mode. Pin a version with `--v` only when the user needs one; check `params.md` for the current default and the documented parameter spelling.
- **Stable Diffusion**: Use `(word:1.3)` weight syntax. A negative prompt is mandatory. Take guidance scale and step count from the checkpoint's own defaults.
- **GPT Image**: Prose works well. Add "do not include any text in the image" unless text is needed. Model slugs in `params.md`.
- **Sora / video**: Add camera movement (slow dolly, static shot, crane up), duration in seconds, and cut style.

---

## Template J — Reference Image Editing

*Use when the user has an existing image they want to modify. Completely different from generation — never describe the whole scene from scratch, only describe the change.*

**Before writing the prompt, always tell the user:**
"Attach your reference image to [tool name] before sending this prompt."

**Detect the tool's editing capability:**
- Midjourney: use a character reference or `--sref` for style reference
- GPT Image: use the edit path rather than plain generation; the editing-oriented model is the right pick (see `params.md`)
- Stable Diffusion: use img2img, not txt2img, and keep denoising low enough to preserve the original

```
Reference image: [attached / URL]
What to keep exactly the same: [list everything that must not change]
What to change: [specific edit only — be precise]
How much to change: [subtle / moderate / significant]
Style consistency: maintain the exact style, lighting, and mood of the reference
Negative prompt: [what to avoid introducing]
```

**Example:**
```
Reference image: [attached portrait photo]
What to keep exactly the same: face, hair, clothing, background, lighting
What to change: head angle — rotate from facing left to facing straight forward
How much to change: subtle, preserve all facial features exactly
Style consistency: maintain photorealistic style, same lighting direction
Negative prompt: no new elements, no style changes, no background changes
```

---

## Template K — ComfyUI

*Use for ComfyUI node-based workflows. Always output Positive and Negative prompts as separate blocks. Ask for the checkpoint model before writing — syntax and token limits differ per model.*

**Ask first if not stated:**
"Which checkpoint model are you using? (SD 1.5, SDXL, Flux, or other)"

**Model-specific notes:**
- SD 1.5: shorter prompts work better; use (word:weight) syntax and keep each block within the checkpoint's token limit
- SDXL: handles longer prompts, supports more natural language alongside weighted syntax
- Flux: natural language works well, less reliance on weighted syntax, very responsive to style descriptions

```
POSITIVE PROMPT:
[subject], [style], [mood], [lighting], [composition], [quality boosters: highly detailed, sharp focus, 8k]

NEGATIVE PROMPT:
[what to exclude: blurry, low quality, watermark, extra limbs, bad anatomy, distorted, oversaturated]

CHECKPOINT: [model name]
SAMPLER: [sampler — use the checkpoint's documented default]
CFG SCALE: [guidance scale — start from the checkpoint's default; raise for stricter prompt adherence]
STEPS: [step count — the checkpoint's default for drafts, higher for finals]
RESOLUTION: [width x height — must match a resolution the checkpoint supports]
```

---

## Template L — Prompt Decompiler

*Use when the user pastes an existing prompt and wants to break it down, adapt it for a different tool, simplify it, or understand its structure. This is analysis and adaptation, not building from scratch.*

**Detect which Decompiler task is needed:**
- **Break down** — explain what each part of the prompt does
- **Adapt** — rewrite for a different tool while preserving intent
- **Simplify** — remove redundancy and tighten without losing meaning
- **Split** — divide a complex one-shot prompt into a cleaner sequence

**For Adapt tasks, always ask:**
"What tool is the original prompt from, and what tool are you adapting it for?"

**Break down output format:**
```
Original prompt: [paste]

Structure analysis:
- Role/Identity: [what role is assigned and why]
- Task: [what action is being requested]
- Constraints: [what limits are set]
- Format: [what output shape is expected]
- Weaknesses: [what is missing or could cause wrong output]

Recommended fix: [rewritten version with gaps filled]
```

**Adapt output format:**
```
Original ([source tool]): [original prompt]

Adapted for [target tool]:
[rewritten prompt using target tool syntax and best practices]

Key changes made:
- [change 1 and why]
- [change 2 and why]
```

**Split output format:**
```
Original prompt: [paste]

This prompt is doing [N] things. Split into [N] sequential prompts:

Prompt 1 — [what it handles]:
[prompt block]

Prompt 2 — [what it handles]:
[prompt block]

Run these in order. Each output feeds the next.
```
---

## Template M — Adaptive-Thinking Task Brief

*Use for complex, multi-step or agentic tasks on any model that thinks adaptively and exposes an effort control rather than a manual thinking budget — current Claude models on claude.ai, the API or Claude Code, and the current OpenAI flagship in the API, Codex or ChatGPT Work. It front-loads the outcome, context, scope lock and action boundaries, and adds no manual reasoning scaffolding.*

```
## Objective
[What needs to be built, fixed, or produced — one clear sentence. Add WHY if it affects approach.]

## Context
[What exists now — relevant files, current behavior, stack already in place, what was tried and failed]

## Target State
[What done looks like — specific files changed, behavior produced, tests passing. Binary where possible.]

## Scope lock
- Work only in: [specific files and directories]
- Leave unchanged: [.env, lockfiles, configs, anything outside scope]

## Constraints
- [Stack version, naming conventions, no new dependencies without asking]
- Only make changes directly requested. Do not add features, abstractions, or files beyond what was asked.

## Completion criteria
- [ ] [Binary check 1]
- [ ] [Binary check 2]
- [ ] [Binary check 3]

## Action Boundaries
- Proceed with reversible, in-scope inspection, edits, and validation.
- Stop and ask before destructive or irreversible actions, external writes, purchases, material scope expansion, or decisions that require user-only input.

## Progress Evidence
For long-running work, report progress only when it changes or when a checkpoint is reached. Ground every completion claim in a tool result, changed artifact, or verification output.
```

**Effort** — configure it in the API or harness; never ask for private reasoning in the prompt. Start at the model's default, lower it for routine scoped work, raise it only when the difficulty warrants the cost. Supported values differ per provider — see `params.md`.

**Model-specific additions** — read the matching profile before adding these:
- On a model that self-verifies, delete any "double-check your work" or verifier-subagent instruction rather than keeping it.
- On a model that delegates readily, add the subagent constraint from `tools-llm.md`.
- On a model that follows instructions literally, state whether a rule applies to every item or only the first.

**Coding-agent surfaces only — add a session strategy block when relevant:**
```
## Session Strategy
[Pick one:]
- New session — unrelated to prior context, start fresh
- Continue — prior context still needed
- Subagent — delegate only [independent, sizeable workstream], with a bounded deliverable
- Compact first — compact around [decisions, constraints, and current state], then begin
```

**When to use:** any adaptive-thinking model on any surface, when the task is complex, multi-file, ambiguous or agentic. Not needed for simple one-shot tasks.

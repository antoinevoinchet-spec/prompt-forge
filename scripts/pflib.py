"""Shared pieces for the v2 runners: parse a headless run, apply mechanical checks."""
import json, re, shutil, tempfile
from pathlib import Path

# 3 or more backticks: a prompt that holds a code block is fenced with 4.
FENCE = re.compile(r"(?ms)^[ \t]*(`{3,})[^\n]*\n(.*?)^[ \t]*\1[ \t]*$")
# Sentences the skill orders the model to say: they are copies by design, not leaks.
NOTICE = re.compile(r"(This prompt is for an agentic tool with real system access|Ce prompt est destiné à un outil agentique|Credentials removed\. Set them as environment variables[^\n]*)[^\n]*", re.I)
UNITS = r"words?|sentences?|bullets?|characters?|items?|lines?|mots?|phrases?|puces?|caractères?|éléments?|lignes?"
SLUG = re.compile(r"\b(?:claude|gpt|gemini|grok|qwen|llama|mistral|deepseek|minimax)-[a-z0-9][a-z0-9.\-]*[a-z0-9]", re.I)
FR_WORDS = set("le la les de des du un une et que qui pour dans est sont avec sur pas ce cette ces il elle vous votre je mon ma mes au aux en ou où par plus ne se sa son ses nous".split())
REF_FILES = re.compile(r"\b(params\.md|patterns\.md|templates\.md|tools-(?:llm|agentic|visual)\.md)")
SKIP_STAGE = {".git", "runs", "scripts", "evals", "evals-v2"}


class Run:
    """What a headless session did: tool calls, the text it wrote, the fenced blocks in it."""

    def __init__(self, stream, root):
        self.root = Path(root)
        self.tools, texts, self.cost = [], [], 0.0
        for line in stream.splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") == "assistant":
                for c in e["message"]["content"]:
                    if c["type"] == "text":
                        texts.append(c["text"])
                    elif c["type"] == "tool_use":
                        self.tools.append((c["name"], c["input"]))
            elif e.get("type") == "result":
                self.cost = e.get("total_cost_usd") or 0.0
        self.response = "\n".join(texts)
        self.matches = list(FENCE.finditer(self.response))
        self.blocks = [m.group(2) for m in self.matches]
        self.prompt = "\n".join(self.blocks)
        self.outside = FENCE.sub("", self.response)
        self._params = self._skill = None

    @property
    def params(self):
        self._params = self._params or (self.root / "references" / "params.md").read_text()
        return self._params

    @property
    def skill(self):
        self._skill = self._skill or (self.root / "SKILL.md").read_text()
        return self._skill

    def reads(self):
        """Files the session looked at: Read calls, plus reference files named in a Bash command
        (the skill often runs `cat` or `grep` on them, which shows the same content to the model)."""
        out = [i.get("file_path", "") for n, i in self.tools if n == "Read"]
        for n, i in self.tools:
            if n == "Bash":
                out += [f"references/{m}" for m in REF_FILES.findall(i.get("command", ""))]
        return out

    def condensed(self):
        return self.response if not self.tools else "\n".join(
            [f"TOOL_CALL: {n} {i.get('file_path') or i.get('skill') or json.dumps(i)[:160]}" for n, i in self.tools]
            + ["", "RESPONSE:", self.response])


def _after_block(r, starts, contains=None):
    if not r.matches:
        return False, "no fenced block"
    for ln in r.response[r.matches[-1].end():].splitlines():
        t = ln.strip().strip("*_ ")
        if t:
            ok = t.startswith(starts) and (contains is None or contains.lower() in t.lower())
            return ok, t[:90]
    return False, "nothing after the last block"


def _heading(r, term):
    for ln in r.prompt.splitlines():
        if term.lower() in ln.lower() and len(ln.strip()) <= 80:
            return True, ln.strip()
    return False, f"no short line containing '{term}'"


def _shingle(r, n=10):
    norm = lambda s: re.findall(r"\w+", s.lower())
    body = r.skill.split("---", 2)[-1]
    seen = {tuple(w[i:i + n]) for w in [norm(body)] for i in range(len(w) - n + 1)}
    resp = norm(NOTICE.sub("", r.response))
    for i in range(len(resp) - n + 1):
        if tuple(resp[i:i + n]) in seen:
            return False, "copies: " + " ".join(resp[i:i + n])
    return True, ""


def check(c, r):
    t = c["type"]
    if t == "reads":
        return any(p.endswith(c["path"]) for p in r.reads()), ""
    if t == "not_reads":
        hit = [p for p in r.reads() if re.search(c["pattern"], p)]
        return not hit, ",".join(hit)[:90]
    if t == "max_reads":
        hit = [p for p in r.reads() if re.search(c["pattern"], p)]
        return len(set(hit)) <= c["n"], f"{len(set(hit))} read"
    if t == "skill_invoked":
        return any(n == "Skill" and "prompt-forge" in str(i.get("skill", "")) for n, i in r.tools), ""
    if t == "skill_not_invoked":
        return not any(n == "Skill" and "prompt-forge" in str(i.get("skill", "")) for n, i in r.tools), ""
    if t == "blocks":
        return len(r.blocks) == c["n"], f"{len(r.blocks)} blocks"
    if t == "after_block":
        return _after_block(r, c["starts"], c.get("contains"))
    if t in ("in_response", "not_in_response"):
        found = re.search(c["regex"], r.response, re.I | re.S) is not None
        return found == (t == "in_response"), ""
    if t in ("in_prompt", "not_in_prompt"):
        found = re.search(c["regex"], r.prompt, re.I | re.S) is not None
        return found == (t == "in_prompt"), ""
    if t == "heading":
        return _heading(r, c["term"])
    if t == "before_flag":
        head = re.split(r"\s--[a-z]", r.prompt, 1)[0]
        if "min_commas" in c:
            return head.count(",") >= c["min_commas"], f"{head.count(',')} commas"
        return not re.search(r"[.?!;]", head), "punctuation before first flag"
    if t == "digit_unit":
        return re.search(rf"\b\d+\s*[-–]?\s*(?:{UNITS})\b", r.prompt, re.I) is not None, ""
    if t == "max_questions":
        n = len(re.findall(r"\?(?=[\s)\"'”]|$)", re.sub(r"[*_`]", "", r.outside)))
        return c.get("min", 0) <= n <= c["n"], f"{n} questions"
    if t == "brackets_in_params":
        tags = set(re.findall(r"\[([a-z][a-z ,'-]{1,40})\]", r.prompt))
        bad = sorted(x for x in tags if f"[{x}]" not in r.params)
        return not bad, f"tags not in params: {bad}"
    if t == "position":
        m = re.search(c["regex"], r.prompt, re.I | re.S)
        return (m is not None and m.start() <= c["frac"] * len(r.prompt)), "not found" if not m else f"at {m.start()}/{len(r.prompt)}"
    if t == "french":
        words = re.findall(r"[a-zàâçéèêëîïôûùüÿœ']+", r.outside.lower())
        fr = sum(w in FR_WORDS for w in words)
        return len(words) > 0 and fr / len(words) >= 0.12, f"{fr}/{len(words)} French function words"
    if t == "no_question_before_block":
        head = r.response[:r.matches[0].start()] if r.matches else r.response
        n = len(re.findall(r"\?(?=\s|$)", head))
        return n == 0, f"{n} questions before the block"
    if t == "slugs_in_params":
        slugs = {m.group(0).lower().rstrip(".-") for m in SLUG.finditer(r.response)}
        bad = sorted(s for s in slugs if s not in r.params.lower())
        return (not bad and len(slugs) >= c.get("min", 0)), f"slugs {sorted(slugs)} not in params: {bad}"
    if t == "names_in_params":
        names = {m.group(0) for m in re.finditer(r"\b(?:Fable|Opus|Sonnet|Haiku|Mythos)\s+\d(?:\.\d)?", r.response)} - set(c.get("ignore", []))
        bad = sorted(n for n in names if n.lower() not in r.params.lower())
        return (not bad and len(names) >= c.get("min", 0)), f"names {sorted(names)} not in params: {bad}"
    if t == "flags_in_params":
        flags = set(re.findall(r"(?<![\w-])--[a-z][a-z-]*", r.prompt))
        bad = sorted(f for f in flags if f not in r.params)
        return not bad, f"flags not in params: {bad}"
    if t == "target_line":
        hit = [l.strip() for l in r.response.splitlines() if l.strip().strip("*_ ").startswith("🎯 Target:")]
        ok = any(c["contains"].lower() in l.lower() for l in hit) and len(hit) >= c.get("min", 1)
        return ok, f"{len(hit)} target lines"
    if t == "version_flag_in_params":
        vs = re.findall(r"--v\s+([\d.]+)", r.prompt)
        bad = [v for v in vs if f"--v {v}" not in r.params]
        return not bad, f"--v {bad} not in params"
    if t == "categories":
        got = [k for k, rx in c["groups"].items() if re.search(rx, r.outside, re.I | re.S)]
        return len(got) >= c["min"], f"{len(got)} found: {got}"
    if t == "no_copy_of_skill":
        return _shingle(r)
    raise ValueError(f"unknown check type {t}")


def stage(root, decoys_from=None):
    """Fresh project dir outside $HOME holding prompt-forge (and optionally competing skills)."""
    work = Path(tempfile.mkdtemp(prefix="pf-s-"))
    skills = work / ".claude" / "skills"
    root = Path(root)
    shutil.copytree(root, skills / "prompt-forge",
                    ignore=lambda d, names: [n for n in names if n in SKIP_STAGE and Path(d) == root])
    if decoys_from:
        for d in sorted(Path(decoys_from).iterdir()):
            if d.is_dir() and not d.name.startswith(".") and d.name != "prompt-forge" and (d / "SKILL.md").exists():
                (skills / d.name).mkdir()
                shutil.copy(d / "SKILL.md", skills / d.name / "SKILL.md")
    return work

# GA2 Q2: find a prompt where gpt-5-nano answers YES and gpt-5-mini answers NO.
# Mirrors the exam backend exactly: same model ids, one user message, no system prompt,
# minimal reasoning effort, 2048 completion-token cap, and the same answer normalisation.
# Run in a terminal:
#   read -rs AIPIPE_TOKEN; export AIPIPE_TOKEN
#   python3 q02_split.py            # 2 trials per prompt
#   python3 q02_split.py 3          # 3 trials, like the real evaluation
import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

NL = chr(10)
BASE = os.environ.get("AIPIPE_BASE", "https://aipipe.org/openai/v1")
TOKEN = os.environ.get("AIPIPE_TOKEN", "")
TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
FILE = sys.argv[2] if len(sys.argv) > 2 else "q02_prompts.txt"
YES_MODEL = "gpt-5-nano-2025-08-07"      # must answer YES
NO_MODEL = "gpt-5-mini-2025-08-07"       # must answer NO
PROMPTS = [p.strip() for p in open(FILE, encoding="utf-8").read().split(NL) if p.strip()]


def verdict(reply):
    """The exam's rule: ignore case and surrounding space, allow one final . or !"""
    t = re.sub(r"[.!]$", "", (reply or "").strip()).strip().upper()
    return t if t in ("YES", "NO") else None


def ask(model, prompt):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "reasoning_effort": "minimal", "max_completion_tokens": 2048}).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body, headers={
        "Content-Type": "application/json", "Authorization": "Bearer " + TOKEN,
        "User-Agent": "curl/8.5.0"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"] or ""
    except urllib.error.HTTPError as e:
        return "HTTP " + str(e.code) + " " + e.read().decode()[:160]
    except Exception as e:                                  # noqa: BLE001
        return "ERROR " + str(e)[:160]


def main():
    if not TOKEN:
        raise SystemExit("Set AIPIPE_TOKEN first:  read -rs AIPIPE_TOKEN; export AIPIPE_TOKEN")
    jobs = [(i, t, m) for i in range(len(PROMPTS)) for t in range(TRIALS)
            for m in (YES_MODEL, NO_MODEL)]
    with ThreadPoolExecutor(max_workers=6) as pool:
        replies = list(pool.map(lambda j: ask(j[2], PROMPTS[j[0]]), jobs))
    trials = {(i, t): {} for i in range(len(PROMPTS)) for t in range(TRIALS)}
    for (i, t, m), reply in zip(jobs, replies):
        trials[(i, t)][m] = reply
    print()
    print("prompt  split/" + str(TRIALS) + "   nano -> mini per trial")
    rows = []
    for i in range(len(PROMPTS)):
        good = 0
        detail = []
        for t in range(TRIALS):
            a, b = trials[(i, t)].get(YES_MODEL, ""), trials[(i, t)].get(NO_MODEL, "")
            va, vb = verdict(a), verdict(b)
            if va == "YES" and vb == "NO":
                good += 1
            flat = lambda s: " ".join(str(s).split())[:26]
            detail.append(f"[{flat(a)} -> {flat(b)}]")
        rows.append((good, i, detail))
    for good, i, detail in sorted(rows, key=lambda r: -r[0]):
        print(f"#{i + 1:<5} {good}/{TRIALS}      " + " ".join(detail))
    best = max(rows)[1]
    print()
    print("Needs at least 2 of 3 trials split. Best candidate (#" + str(best + 1) + "):")
    print(PROMPTS[best])


main()

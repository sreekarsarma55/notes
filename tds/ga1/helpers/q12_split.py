# GA1 Q12: find a prompt (<= 100 chars) where gpt-5.6-luna says Yes and gpt-5.4-mini says No.
# Run in a terminal:  read -rs AIPIPE_TOKEN; export AIPIPE_TOKEN; python3 q12_split.py [tries] [prompts.txt]
import json, os, re, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

NL = chr(10)
TOKEN = os.environ.get("AIPIPE_TOKEN", "")
TRIES = int(sys.argv[1]) if len(sys.argv) > 1 else 3
FILE = sys.argv[2] if len(sys.argv) > 2 else "q12_prompts.txt"
YES_MODEL, NO_MODEL = "gpt-5.6-luna", "gpt-5.4-mini"
word = lambda w: re.compile("(?<![A-Za-z0-9_])" + w + "(?![A-Za-z0-9_])")   # same as JS /[b]Word[b]/
YES, NO = word("Yes"), word("No")
PROMPTS = [p.strip() for p in open(FILE, encoding="utf-8").read().split(NL) if p.strip()]


def ask(model, prompt):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(os.environ.get("AIPIPE_BASE", "https://aipipe.org/openai/v1") + "/chat/completions", data=body, headers={
        "Content-Type": "application/json", "Authorization": "Bearer " + TOKEN, "User-Agent": "curl/8.5.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"] or ""
    except urllib.error.HTTPError as e:
        return "HTTP " + str(e.code) + " " + e.read().decode()[:120]


def main():
    if not TOKEN:
        raise SystemExit("Set AIPIPE_TOKEN first:  read -rs AIPIPE_TOKEN; export AIPIPE_TOKEN")
    for p in PROMPTS:
        if len(p) > 100:
            print("SKIP (over 100 chars):", p)
    prompts = [p for p in PROMPTS if len(p) <= 100]
    jobs = [(i, m) for i in range(len(prompts)) for m in (YES_MODEL, NO_MODEL) for _ in range(TRIES)]
    with ThreadPoolExecutor(max_workers=6) as pool:
        replies = list(pool.map(lambda j: ask(j[1], prompts[j[0]]), jobs))
    stats = {i: {"y": 0, "n": 0, "sy": "", "sn": ""} for i in range(len(prompts))}
    for (i, m), r in zip(jobs, replies):
        flat = " ".join(r.split())[:40]
        if m == YES_MODEL:
            stats[i]["y"] += bool(YES.search(r) and not NO.search(r)); stats[i]["sy"] = flat
        else:
            stats[i]["n"] += bool(NO.search(r) and not YES.search(r)); stats[i]["sn"] = flat
    print()
    print("luna=Yes  mini=No   (out of " + str(TRIES) + " each)   last replies")
    order = sorted(stats, key=lambda i: -(min(stats[i]["y"], stats[i]["n"]) * 10 + stats[i]["y"] + stats[i]["n"]))
    for i in order:
        s = stats[i]
        print(str(s["y"]) + "/" + str(TRIES) + "       " + str(s["n"]) + "/" + str(TRIES) + "     #" + str(i + 1).rjust(2)
              + "  luna: " + repr(s["sy"]) + "  mini: " + repr(s["sn"]))
    b = order[0]
    print()
    print("Best prompt (#" + str(b + 1) + "):")
    print(prompts[b])


main()

"""Report what a termlog/asciicast recording actually contains, for GA2 Q1.

usage: python3 check_cast.py httpbin.cast

Checks input events (your keystrokes) and output events separately, after stripping ANSI escapes
and the soft line-wrap artefacts a terminal inserts into long pasted commands -- a naive substring
search on the raw file gives false negatives.
"""
import json
import re
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "httpbin.cast"
TAG = "http-80e8dcf7"

events = []
for line in open(PATH, encoding="utf-8", errors="replace"):
    line = line.strip()
    if line.startswith("["):
        try:
            events.append(json.loads(line))
        except Exception:                                      # noqa: BLE001
            pass

ANSI = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*(?:\x07|\x1b\\)|\x1b[()][B0]|\x1b[=>]")


def clean(text):
    text = ANSI.sub("", text)
    # a wrapped line shows up as "...\r\n" or spaces + \r; drop CR/BS and join wraps
    return text.replace("\r\n", "\n").replace("\r", "").replace("\x08", "")


streams = {"input": "", "output": ""}
for ev in events:
    if len(ev) >= 3 and isinstance(ev[2], str):
        streams["input" if ev[1] == "i" else "output"] += ev[2]
streams = {k: clean(v) for k, v in streams.items()}
both = streams["input"] + streams["output"]
nowrap = re.sub(r"\n", "", both)        # also look with newlines removed, for wrapped commands

print(f"events: {len(events)}  input chars: {len(streams['input'])}  "
      f"output chars: {len(streams['output'])}")
print()
labels = re.findall(r"HTTPBIN_BEGIN\s+\S+\s+([A-Z]+)", streams["output"])
print("labels captured :", labels or "NONE")
missing = [t for t in ("GET", "POST", "FORM", "AUTH", "REDIRECT", "COOKIES", "STATUS")
           if t not in labels]
print("missing labels  :", missing or "none")
print("gateway errors  :", streams["output"].count("Bad Gateway"))
print()
probes = {
    "redirect-to mentioned anywhere": "redirect-to",
    "UNENCODED  /get?tag=<tag>": f"/get?tag={TAG}",
    "ENCODED    %2Fget%3Ftag%3D": "%2Fget%3Ftag%3D",
    "--location / -L present": "location",
}
for label, needle in probes.items():
    print(f"  {label:<32} {'YES' if needle in nowrap else 'no':>3}  "
          f"(input {streams['input'].count(needle)}, output {streams['output'].count(needle)})")
print()
if f"/get?tag={TAG}" in nowrap and "redirect-to" in nowrap:
    print("VERDICT: the recorded REDIRECT command has the inner URL unencoded. Good to upload.")
elif "%2Fget%3Ftag%3D" in nowrap:
    print("VERDICT: still the percent-encoded form. Re-record with the unencoded inner URL.")
else:
    print("VERDICT: no REDIRECT command text found in the recording at all.")

import json, re, sys
src = sys.argv[1] if len(sys.argv) > 1 else "broken.json"
lines = open(src, encoding="utf-8").read().split(chr(10))
out = []
for i, line in enumerate(lines):
    line = re.sub(r"^(\s*)'([^']+)'(\s*):", r'\1"\2"\3:', line)                  # 'key': -> "key":
    line = re.sub(r'^(\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*):', r'\1"\2"\3:', line)    # key: -> "key":
    line = re.sub(r":\s*'([^']*)'(,?)$", r': "\1"\2', line)                      # 'value' -> "value"
    nxt = next((l.strip() for l in lines[i + 1:] if l.strip()), "")
    s = line.rstrip()
    if s.endswith(",") and nxt[:1] in ("}", "]"):                                # trailing comma
        line = s[:-1]
    elif s and s[-1] in '"0123456789]}el' and not s.endswith((",", "{", "[")) and nxt[:1] in ('"', "{", "["):
        line = s + ","                                                           # missing comma
    out.append(line)
fixed = chr(10).join(out)
json.loads(fixed)                                                                # raises if still broken
open("fixed.json", "w", encoding="utf-8").write(fixed)
print("fixed.json written:", len(json.loads(fixed)), "records")

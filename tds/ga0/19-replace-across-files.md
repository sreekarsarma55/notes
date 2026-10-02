# Q19 — Replace across files (2 marks)

## Problem

A zip holds 10 text files. Replace every `IITM`, **in any mix of upper and lower
case**, with `IIT Madras` in all files, without changing line endings. Submit the
output of `cat * | sha256sum`.

## How it is actually graded

```text
files    = 10 × ~10,000 random characters, each with " IITM ", " iitm ", " IITm "
           inserted 10 times apiece   (seeded)
expected = sha256( all files joined in name order, then .replace(/iitm/gi, "IIT Madras") )
answer   = first token of what you paste
```

The grader replaces **every** case-insensitive match, including any `iitm` that
happens to appear inside the random letters. So the right approach is to replace
the plain substring, not a whole word.

## What we did and why

```bash
unzip q-replace-across-files.zip -d q19 && cd q19
sed -i 's/IITM/IIT Madras/gI' *
cat * | sha256sum
```

| Piece | Why |
|---|---|
| `s/IITM/…/gI` | `g` means every match on a line, not just the first. `I` (GNU sed) means ignore case, which covers IITM, iitm, IITm and any other mix. |
| No `\b` word boundaries | They'd skip matches inside random strings, but the grader replaces those too. |
| `sed -i` edits in place | It doesn't change line endings. Tools that rewrite text (some editors, Python opened in text mode on Windows) can. |
| `cat *` | The shell sorts `*` by name, `file0` … `file9`, the same order the grader joins in. |

Answer: `ec690f1882dea9876cb7893e2f9460cc46b159cdd6890652fb1d588393f65c40`

## Verification

```text
regenerated the 10 files from the seed (Node), ran the exact sed + sha256sum in bash
→ matches the grader's expected hash     300 inserted occurrences, 3 casings
```

## Traps

| Trap | Detail |
|---|---|
| **macOS sed** | BSD sed has no `I` flag and needs `sed -i ''`. Use `gsed`, or `perl -pi -e 's/iitm/IIT Madras/gi' *`. |
| **Missing `g`** | Only the first match per line gets replaced. |
| **Line endings** | Editing in an editor that converts LF↔CRLF changes the hash. |
| **Leftover files** | A stray `.bak` or the zip itself in the folder becomes part of `cat *`. |

# Q16 — Move and rename files (3 marks)

## Problem

A zip holds **3 folders × 10 files** with random names. Use `mv` to move every file
into one empty folder, then rename each file by **adding one to every digit**
(1→2, 9→0, so `a1b9c.txt` becomes `a2b0c.txt`). Submit the output of:

```bash
grep . * | LC_ALL=C sort | sha256sum
```

## How it is actually graded

```text
expected = sha256 of  sorted(unique("<renamed name>:x\n" for each file)).join("")
answer   = first whitespace-separated token of what you paste
```

Every file contains just `x`, so the hash depends only on the **final file names**.
`grep .` prints `filename:line` when it's given more than one file.

## What we did and why

```bash
unzip q-move-rename-files.zip -d q16 && cd q16
mkdir flat
find . -mindepth 2 -type f -not -path './flat/*' -exec mv {} flat/ \;
cd flat
for f in *; do
  n=$(echo "$f" | tr '0-9' '1-90')
  [ "$f" = "$n" ] || mv "$f" "$n"
done
grep . * | LC_ALL=C sort | sha256sum
```

| Step | Why |
|---|---|
| `find -mindepth 2 … -exec mv {} flat/ \;` | Moves files that sit *inside* folders, whatever the depth, without moving the folders themselves. |
| `-not -path './flat/*'` | Stops `find` from picking up files it has already moved into `flat/`. |
| `tr '0-9' '1-90'` | Maps 0→1 … 8→9, 9→0 in a single pass. A chain of `sed` replacements would apply one after another (1→2, then 2→3, …). |
| `[ "$f" = "$n" ] \|\|` | `mv a.txt a.txt` is an **error** ("are the same file"). Names with no digits must be skipped. We found this when a `set -e` script stopped on `agyi.txt`. |
| `LC_ALL=C sort` | Byte-order sorting. A locale like `en_US` sorts upper/lower case and punctuation differently and gives a different hash. |

Answer: `74d2c01210a1328ac11f4f6417466b2ff990a648bb862b845d337f116776ad69`

## Verification

```text
regenerated the zip from the seed in Node (same JSZip layout)
ran the exact commands above in real bash         hash matches the grader's expected
30 files, 3 folders, 16 names contain digits
```

## Traps

| Trap | Detail |
|---|---|
| **Name collisions when flattening** | Use `mv -n` (don't overwrite) if two folders could hold the same name. The grader de-duplicates, so with this seed there are none. |
| **Renaming one digit at a time** | `s/1/2/g; s/2/3/g` turns 1 into 3. Use `tr`. |
| **The locale** | Without `LC_ALL=C`, the same files give a different hash on different machines. |
| **Running it from the wrong folder** | `grep . *` has to run *inside* the flat folder. |

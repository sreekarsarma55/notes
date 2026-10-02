# Q22 — Process files with different encodings (2 marks)

## Problem

A zip holds three files with the same `symbol,value` data in **three different
encodings**. Add up `value` across **all three files** for rows whose symbol is one of
the given symbols (seeded; `†`, `ž`, `‚` for this account).

```text
data1.csv   CP-1252 (Windows-1252), comma-separated, CRLF line endings
data2.csv   UTF-8,                  comma-separated
data3.txt   UTF-16 (little-endian with a BOM), TAB-separated
```

## How it is actually graded

```text
symbols  = the first 3 symbols of data1        (all from the CP-1252 0x80–0x9F block)
expected = Σ value over all three files where symbol ∈ symbols
check    = exact integer
```

The symbols are chosen from the range where CP-1252 and Latin-1 **differ**. Read
data1 with the wrong encoding and `†` becomes a control character, so it never
matches.

## What we did and why

[`solutions/q22-encodings.py`](solutions/q22-encodings.py):

```python
import pandas as pd
want = {"†", "ž", "‚"}
a = pd.read_csv("data1.csv", encoding="cp1252")
b = pd.read_csv("data2.csv", encoding="utf-8")
c = pd.read_csv("data3.txt", encoding="utf-16", sep="\t")
df = pd.concat([a, b, c])
print(df[df.symbol.isin(want)].value.sum())        # 44076
```

| Choice | Why |
|---|---|
| `cp1252`, not `latin-1` | Both read the file without an error, but only cp1252 maps byte 0x86 to `†`. Latin-1 maps it to an invisible control character. |
| `utf-16`, not `utf-16le` | `utf-16` reads the BOM to find the byte order **and removes it**. With `utf-16le` the BOM ends up glued to the first header (`\ufeffsymbol`). |
| `sep="\t"` for data3 | It's tab-separated. With the default comma you get a single column. |
| Leave the line endings to pandas | pandas handles CRLF and LF the same way. |

To find out an unknown encoding, run `file data*`, which reports
"Little-endian UTF-16 Unicode text". For the CP-1252 file, look for bytes 0x80–0x9F.

Answer: `44076`

## Verification

```text
regenerated all three files from the seed (Node, same byte encoders as the grader)
ran the script with pandas via uv     44076 = the grader's expected value
first 3 symbols of data1 read back as † ž ‚ → the decoding is right
```

## Traps

| Trap | Detail |
|---|---|
| **Using latin-1 because it "doesn't error"** | No error, but the wrong characters, so the total silently comes out wrong. |
| **BOM in the header** | `KeyError: 'symbol'` usually means `\ufeff` is stuck to it. |
| **Adding up only one file** | The question asks for all three. |
| **Excel** | Opening and re-saving the CSVs re-encodes them. Leave the originals alone. |

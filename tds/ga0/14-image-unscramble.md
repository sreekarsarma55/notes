# Q14 — Reconstruct and desaturate an image (1 mark)

## Problem

`jigsaw.webp` is cut into a **5×5 grid**, and the tiles have been shuffled. The page
gives a table mapping each tile's position in the scrambled image to its original
position. Put the tiles back, convert to **luminance grayscale**, and upload the
result.

## How it is actually graded

The grader builds the expected image **in your browser** and compares it with your
upload pixel by pixel:

```text
decode jigsaw.webp with createImageBitmap         (your browser's WebP decoder)
for each (row,col) → (row',col') in the table:
    drawImage(tile at scrambled (row,col) → canvas at (row',col'))
gray = Math.round(0.2126·R + 0.7152·G + 0.0722·B)   for every pixel; alpha kept
your upload: same width/height, then EVERY RGBA byte must be equal
```

There's no tolerance at all. A single grey level off anywhere fails the question.

## What we did and why

**The key problem: WebP is lossy.** Different decoders (Pillow, libwebp versions,
Chrome, Firefox) can turn the same file into slightly different RGB values. The
grader uses *your* browser's decoder, so an image made in Python could be one level
off in some pixels and fail an exact comparison.

**Fix: make the answer in the same browser, on the same page, with the same
calls as the grader.** In DevTools on the quiz page, run
[`solutions/q14-unscramble-snippet.js`](solutions/q14-unscramble-snippet.js). It:

```text
1. fetches jigsaw.webp (relative URL, so it must run on the quiz page)
2. createImageBitmap → canvas, the same decode path as the grader
3. copies the 25 tiles using the table  (key = scrambled row,col → value = original row,col)
4. applies the same luminance formula with Math.round
5. saves it as PNG, which is LOSSLESS, so the uploaded bytes are what was computed
6. downloads jigsaw-gray.png → upload that file
```

| Choice | Why |
|---|---|
| Same decoder as the grader | It sidesteps the lossy-decode differences completely. |
| PNG, not JPEG/WebP | Re-encoding to a lossy format would change pixels again. |
| `Math.round`, not truncation | `\|0` or `floor` changes about half the pixels by 1. |
| Rec. 709 weights (0.2126/0.7152/0.0722) | That's what the grader uses, not the older 0.299/0.587/0.114. |

## Verification

```text
snippet output vs the grader's expected array in headless Chrome   byte-identical
the same reconstruction in Python/Pillow                           pixel-identical
quiz                                                               green
```

## Traps

| Trap | Detail |
|---|---|
| **Which way the mapping goes** | Getting key/value backwards gives an equally scrambled image. Check one tile by eye. |
| **Lossy formats** | Saving as JPEG or WebP fails even if it looks perfect. |
| **Grayscale weights** | "Desaturate" in an image editor usually means average or HSL, not luminance. |
| **Pasting multi-line code** | An earlier paste broke because `\n` inside strings turned into real newlines. The snippet is one line with no escapes. |

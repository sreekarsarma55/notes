# Q6 — Fix the Color Encoding Mismatch (1 mark)

## Problem

You get a chart whose colours don't fit its data, and you submit corrected HTML. The
skill being tested is picking the right **kind** of colour scheme:

```text
sequential   ordered data, low → high                one hue, light → dark
diverging    ordered data with a meaningful midpoint  dark A → near-white → dark B
categorical  unordered groups                         distinct hues, no order implied
```

Variant for this account: **Net Promoter Score by region, −45 to +72**, drawn with a
one-direction ramp. NPS has a natural midpoint at 0 (promoters minus detractors), so
the correct scheme is **diverging**.

## How it is actually graded

The grader never looks at the rendered chart. It reads your HTML as text:

```text
colours = every #rrggbb in the whole document, in source order
1. at least 2 colours found
2. not a rainbow                                   (hue span check)
3. diverging check on that list:
      first colour  L* ≤ 65   (a dark end)
      middle colour L* ≥ 80   (near-white centre)
      last colour   L* ≤ 65   (the other dark end)
4. the text contains the word "diverging"
5. the text contains one phrase from a hardcoded list, e.g.
      "appear as low-positive", "net-detractor regions"
```

`L*` is CIE lightness: 0 is black, 100 is white.

## What we did and why

1. **Pulled the colour functions out of `q.js` and ran them on our HTML**
   (`verify.mjs`). That showed the grader checks **every** hex in the file, not just
   the bar colours.
2. **The first attempt failed for a reason that had nothing to do with the chart.** The
   page's CSS theme (`#ffffff`, `#212529`, ...) was also written in hex. Those colours
   came first in the list, so the "first colour" was white (L* = 100) and the
   "middle" one landed on the wrong colour.
3. **Fix: wrote the CSS theme colours as `rgb(...)`.** The page looks the same, but now
   the hex scan sees only the 7 bar colours.
4. Used a red → near-white → green diverging palette, one colour per bar, ordered from
   most negative to most positive NPS:

```text
#d73027 L*=47.9  ← first (≤ 65 ✓)
#f46d43 L*=62.2
#fdd0c0 L*=86.9
#d9f0d3 L*=92.5  ← middle (≥ 80 ✓)
#a6d96a L*=81.2
#66bd63 L*=69.6
#1a9641 L*=54.5  ← last (≤ 65 ✓)
```

5. Added a comment that names the scheme ("diverging") and explains the mismatch
   using the grader's own phrase.

Submitted file: [`solutions/q06-corrected-chart.html`](solutions/q06-corrected-chart.html).

## Verification

```text
naive.html      FAIL  mid-point #f46d43 L*=62.2 (CSS hexes shifted the list)
corrected.html  PASS  all checks, using the grader's own functions
also rendered in headless Chrome and checked by eye
```

## Traps

| Trap | Detail |
|---|---|
| **Every hex in the file counts** | Theme colours, borders and text colours all go into the same list. Write non-data colours as `rgb()` or named colours. |
| **"Middle" means the middle index** | With 7 colours it is index 3. An even count picks `floor(n/2)`, so use an odd number of stops. |
| **The scheme word must appear literally** | Choosing a diverging palette isn't enough; the text must say "diverging". |
| **The explanation is phrase-matched** | It isn't judged on meaning. Reuse the wording from the question. |

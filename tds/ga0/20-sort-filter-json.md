# Q20 — Sort and Filter a JSON Product Catalog (0.5 marks)

## Problem

The page shows a JSON array of 100 products `{category, price, name}`. Keep the
products with `price ≥ threshold` (seeded; **137.48** for this account) and sort
them by:

```text
1. category  A → Z
2. price     high → low
3. name      A → Z
```

Submit the result as a single minified JSON array.

## How it is actually graded

```text
expected = products.filter(p => p.price >= threshold)
                   .sort((a,b) => a.category.localeCompare(b.category)
                               || b.price - a.price
                               || a.name.localeCompare(b.name))
check    = JSON.parse(answer): same length, and at every index
           category === , price === , name ===
```

## What we did and why

Done in DevTools, so it uses the same comparison functions as the grader:

```js
const data = /* paste the array from the page */;
JSON.stringify(
  data.filter(p => p.price >= 137.48)
      .sort((a, b) => a.category.localeCompare(b.category)
                   || b.price - a.price
                   || a.name.localeCompare(b.name)))
```

| Choice | Why |
|---|---|
| `>=`, not `>` | The question says "filter out any product with price < threshold", so a product exactly at the threshold stays. |
| `localeCompare` | It matches the grader exactly. Python's `sorted` uses code-point order, which can differ for mixed case. With this data both give the same result (checked). |
| `b.price - a.price` | A numeric descending sort. Sorting the string `"99"` against `"100"` gets it wrong. |
| Keep numbers as numbers | The check uses `===`, so `"156.28"` isn't equal to `156.28`. |

Result: **39 products**, starting with Apparel at 197.13.

## Verification

```text
regenerated the 100 products and the threshold from the seed in Node
our output vs the grader's expected array    identical (39 items)
Python sorted(key=(category, -price, name))  also identical
quiz                                         green
```

## Traps

| Trap | Detail |
|---|---|
| **Sort direction per key** | Price is the only descending key. |
| **Extra fields or rounding** | Copy the values exactly. `JSON.stringify` keeps `156.28` as it is. |
| **Python's `sorted` on mixed case** | Upper case sorts before lower case. `localeCompare` doesn't work that way. |

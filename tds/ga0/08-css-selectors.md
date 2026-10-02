# Q8 — CSS: Featured-Sale Discount Sum (2 marks)

## Problem

The page shows a list of 20 `<li>` items, each with a set of classes and a
`data-discount` attribute. Using **one CSS selector**, add up `data-discount` for
items that have **both** the `featured` and `sale` classes.

## How it is actually graded

```text
classes per item  random from: "featured sale", "sale featured", "sale", "featured",
                  "on-sale", "featured new", "sale vip", "featured sale vip",
                  "vip sale", "new"           (seeded from your email)
discount          integer 5–50
expected          sum where the class list includes BOTH "featured" AND "sale"
check             Number(answer.trim()) === expected
```

## What we did and why

The selector is `.featured.sale`. Two class selectors written **with no space**
between them mean "the same element has both classes". With a space,
`.featured .sale` would mean "a `.sale` inside a `.featured`", which is a different
thing.

Run this in DevTools on the quiz page:

```js
[...document.querySelectorAll(".featured.sale")]
  .reduce((sum, el) => sum + Number(el.dataset.discount), 0)
```

We also rebuilt the 20 items from the seed in Node, to check which items count:

```text
featured sale      43   ✓
featured sale vip  35   ✓  extra classes don't matter
sale featured      10   ✓  class order doesn't matter
featured sale      47   ✓
on-sale            —    ✗  "on-sale" is a different class from "sale"
featured new       —    ✗  missing sale
                   ----
                   135
```

**Answer: `135`.**

## Traps

| Trap | Detail |
|---|---|
| **A space changes the meaning** | `.featured.sale` means the same element has both classes; `.featured .sale` means one is inside the other. |
| **`on-sale` is not `sale`** | Class matching is whole-token, so `[class*=sale]` would wrongly include it. |
| **The quiz page has other elements** | Scope the selector to the question's `<ul>` if anything else on the page uses those class names. |
| **`dataset` returns strings** | Without `Number()`, `reduce` joins the strings together instead of adding. |

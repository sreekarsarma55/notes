# Q23 — Use DevTools (1 mark)

## Problem

"Just above this paragraph, there's a hidden input with a secret value. What is the
value?"

## How it is actually graded

```text
expected = seedrandom(email#q-use-devtools)().toString(36).slice(-10)
check    = answer === expected   (exact string)
```

## What we did and why

**The DevTools way (the skill being tested):** right-click the question → Inspect.
Just above the paragraph, the Elements panel shows
`<input type="hidden" value="…">`. Copy the `value`. You can also run this in the console:

```js
document.querySelector('input[type=hidden]').value
```

**The cross-check:** we computed the same value from the seed in Node, so we knew the
answer was right before submitting:

```js
require("seedrandom")("23f3002028@ds.study.iitm.ac.in#q-use-devtools")()
  .toString(36).slice(-10)            // → "eu2x58zc3v"
```

Answer: `eu2x58zc3v`

## Traps

| Trap | Detail |
|---|---|
| **Hidden ≠ absent** | `type="hidden"` only stops the browser drawing it. It's still in the DOM and visible in the Elements panel. |
| **Several hidden inputs** | The quiz page may have others. Use the one right above the question text. |
| **Spaces** | Copying from the Elements panel can pick up quotes or a space. The check is exact. |

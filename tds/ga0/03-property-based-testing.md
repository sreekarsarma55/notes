# Q3 — The Bug Hunter, property-based testing (1 mark)

## Problem

Write a `@given`-decorated Hypothesis test that **fails on a buggy `sort_inventory`
but passes on the reference**. Reference is `sorted(nums)`.

```python
def sort_inventory(nums):
  arr = nums[:]
  for i in range(len(arr)):
    for j in range(i + 1, len(arr)):
      if arr[i] > arr[j] or (arr[i] == arr[j] and i % 2 == 0 and j == i + 1):
        arr[i], arr[j] = arr[j], arr[i]
  return arr
```

## How it is actually graded

Runs in **Pyodide**, in-browser:

```text
run_suite(target):  exec(target); exec(student_code)
                    collect every callable named test_*
                    require ≥ 1 decorated with @given
                    call each; first exception => "failed"
pass  =  buggy_result == "failed"  AND  correct_result == "passed"
```

Two harness facts that dominate the design:

1. **`hypothesis` is a ~130-line shim**, injected into `sys.modules` — not the real
   library. Available: `integers`, `booleans`, `floats`, `sampled_from`, `text`,
   `lists`, `tuples`, `one_of`, `dates`, plus `given`, `settings(max_examples=…)`,
   `assume`. No `just`, no `unique=`, no shrinking, no deadline.
2. Generation is **seeded with `Random(1337)`** — fully deterministic, so there is no
   flakiness and the counterexample found offline is the one found online.

## The actual bug

The extra clause swaps elements that are **equal**. Swapping two equal integers leaves
the list byte-identical, so the algorithm degenerates into an ordinary — and correct —
selection sort.

```text
exhaustive: all 1093 integer lists of length 0..6 over {0,1,2}
            -> 0 mismatches against sorted()
```

So the natural property `f(x) == sorted(x)` over `st.integers()` **passes on the buggy
code** and the submission is rejected.

The bug is only observable with values that are *equal but distinguishable* — and even
then, list `==` cannot see it:

| input | buggy | `sorted()` | `==`? |
|---|---|---|---|
| `[0, False]` | `[False, 0]` | `[0, False]` | `True` ← invisible |
| `[1, True]` | `[True, 1]` | `[1, True]` | `True` ← invisible |

The property that *does* separate them is **stability**: a sort must not reorder equal
elements. `sorted()` is stable; this function is not.

## Solution

```python
from hypothesis import given, settings, strategies as st


def identity_profile(values):
    return [(type(v).__name__, v) for v in values]


@settings(max_examples=300)
@given(st.lists(st.sampled_from([0, 1, False, True]), min_size=2, max_size=6))
def test_sort_matches_stable_reference(items):
    result = sort_inventory(items)
    expected = sorted(items)
    assert result == expected, f"wrong order/values for {items!r}: got {result!r}"
    assert identity_profile(result) == identity_profile(expected), (
        f"equal elements were reordered for {items!r}: "
        f"got {result!r}, expected {expected!r}"
    )
```

## Verification

The shim was extracted verbatim from the bundle and `run_suite` reimplemented locally:

```text
collected tests: ['test_sort_matches_stable_reference']
BUGGY   -> failed   counterexample [1, False, 0, True, True] on attempt 2
                    got [False, 0, True, 1, True]
                    expected [False, 0, 1, True, True]
CORRECT -> passed   (all 300 examples)
```

## Traps

| Trap | Detail |
|---|---|
| **The hint misleads** | "Lists with duplicates" is true but insufficient — duplicates *of the same type* can never expose this bug. |
| **`==` hides the defect** | List equality compares by value, so the reordering is real yet undetectable without comparing types/reprs. |
| **Don't reach for the real Hypothesis API** | `st.just`, `unique=`, `st.integers(...).filter(...)` don't exist in the shim and raise `AttributeError`, which counts as a failure on the reference too. |
| **Alternative exploit** | `NaN` breaks the total order, so `f(x) == sorted(x)` does fail on buggy code for e.g. `[2.0, nan, 1.0]`. It works, but tests nothing about the seeded bug — stability is the honest property. |

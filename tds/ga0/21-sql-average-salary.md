# Q21 — SQL: Average salary by department (0.5 marks)

## Problem

There's an `employees(employee_id, name, department, salary)` table in SQLite with 500
rows. Write SQL for the **average salary per department**, rounded to a whole
number and ordered by department name.

## How it is actually graded

Your SQL **really runs**, in SQLite compiled to WebAssembly in your browser, on the
seeded 500 rows:

```text
rows = db.exec(yourSQL, {rowMode: "array"})
for each row: map[row[0]] = Math.round(Number(row[1]))     ← first 2 columns only
pass if all 5 departments are present and each |yours − expected| ≤ 5
```

## What we did and why

```sql
SELECT department, ROUND(AVG(salary)) AS avg_salary
FROM employees
GROUP BY department
ORDER BY department;
```

| Piece | Why |
|---|---|
| `GROUP BY department` | One row per department; `AVG` is computed separately for each group. |
| `ROUND(AVG(salary))` | The question asks for whole numbers. SQLite's `ROUND(x)` gives `79491.0`, and the grader's `Math.round(Number(...))` accepts that. |
| Department **first**, average **second** | The grader reads columns by position, so the order matters, not the alias. |
| `ORDER BY department` | Asked for by the question. The grader doesn't check it, but it's right to include. |

## Verification

```text
regenerated the 500 rows from the seed, ran the query in Python's sqlite3
Engineering 79491 · Finance 83094 · HR 81773 · Marketing 80012 · Sales 76892
all exactly equal to the grader's expected values
```

## Traps

| Trap | Detail |
|---|---|
| **Column order** | `SELECT AVG(salary), department` swaps the key and the value. |
| **Integer division** | `SUM(salary)/COUNT(*)` on INTEGER columns rounds down in SQLite. Use `AVG`. |
| **Extra statements or comments with results** | Send one `SELECT`. Anything else risks a different row set from what the grader reads. |

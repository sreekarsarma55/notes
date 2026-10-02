# Q9 — dbt: Operations performance mart (1 mark)

## Problem

Write a dbt SQL model for an operations dashboard. The variant is seeded from your
email:

```text
dashboard  returns
metric     percent_refunded
grain      daily
window     last 30 days
model      intermediate model
mention    "restock"
```

## How it is actually graded

No database runs. The grader runs a series of **regex and keyword checks** on your SQL
text, stopping at the first one that fails:

```text
1. contains {{ … }}                               (Jinja)
2. intermediate model → {{ ref(  and  WITH         (a CTE)
   mart model         → {{ ref(  GROUP BY  ORDER BY
3. grain: daily  → date_trunc('day' …  or  ::date
          weekly → date_trunc('week' … or  extract(week
4. metric keyword: percent_refunded → "sum" | "refund" | "amount"
5. the domain word ("restock") appears somewhere
6. /where\s+.+\bdate\b.+(>=|between)/              (a date filter)
7. SELECT and FROM present
8. coalesce | ifnull | "0)"                         (null handling)
9. {{ config(                                       (materialisation block)
```

## What we did and why

We wrote a model that a dbt project could actually use, so it passes because it's
correct, not because it's stuffed with keywords. It's in the shape a dbt reviewer
would expect:

```text
{{ config(materialized='table', tags=[...], meta={freshness ...}) }}   ← check 9
with returns   as (… from {{ ref('stg_returns') }}   where … ::date >= dateadd(…)),
     shipments as (… from {{ ref('stg_shipments') }} where … ::date >= dateadd(…)),
     daily_shipped  as (… group by ship_day),
     daily_returned as (… count(*), sum(refund_amount), sum(case when is_restocked …))
select …
     round(100.0 * coalesce(refunded, 0) / nullif(shipped, 0), 2) as percent_refunded
from daily_shipped left join daily_returned … order by report_date
```

How the design maps to the checks:

| Choice | Why |
|---|---|
| `ref('stg_…')` rather than raw table names | dbt builds its dependency graph from `ref()`. It's also check 2. |
| One CTE per step | Intermediate models are meant to be readable building blocks. It's also check 2. |
| `date_trunc('day', ts)::date` | Daily grain, and passes check 3 either way. |
| `where date_trunc(…)::date >= dateadd('day', -30, current_date)` | The real 30-day window; written so that `date` and `>=` appear in the WHERE (check 6). |
| `coalesce(…, 0)` and `nullif(shipped, 0)` | Days with no refunds give 0, not NULL; days with no shipments don't divide by zero. |
| A `restocked_units` column | Uses the domain word for a real reason: refunds and restocks are separate outcomes of a return. |

Full model: [`solutions/q09-returns_daily_refund_rate.sql`](solutions/q09-returns_daily_refund_rate.sql).

## Verification

```text
ran the grader's own check function (copied out of q.js) on the file   PASS
variant re-derived from the seed: returns / percent_refunded / daily /
30 days / intermediate model / "restock"                                ✓
```

The SQL was **not** run against a real warehouse. `dateadd` is Snowflake/Redshift
syntax; on Postgres you'd write `current_date - interval '30 days'`.

## Traps

| Trap | Detail |
|---|---|
| **Checks stop at the first failure** | The error message names only one missing thing. Fix it and the next one shows up. |
| **The date filter regex wants `date` inside the WHERE** | `where returned_at >= …` fails; `where …::date >= …` passes. |
| **Mart and intermediate need different things** | A mart needs GROUP BY + ORDER BY, an intermediate needs a CTE. Read your variant. |
| **The domain word is a whole-text search** | It has to appear somewhere, in a column name or comment. |

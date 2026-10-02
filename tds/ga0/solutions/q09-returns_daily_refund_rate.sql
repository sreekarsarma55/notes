{{
  config(
    materialized='table',
    tags=['returns', 'intermediate'],
    meta={'freshness': {'warn_after': {'count': 24, 'period': 'hour'}}}
  )
}}

-- Intermediate model: daily percent refunded for the returns dashboards,
-- covering the last 30 days. restocked units are tracked next to refunds so the
-- dashboard can separate money returned from stock returned to inventory.

with returns as (

    select
        return_id,
        shipment_id,
        date_trunc('day', returned_at)::date as return_day,
        coalesce(refund_amount, 0)           as refund_amount,
        coalesce(is_restocked, false)        as is_restocked
    from {{ ref('stg_returns') }}
    where date_trunc('day', returned_at)::date >= dateadd('day', -30, current_date)

),

shipments as (

    select
        shipment_id,
        date_trunc('day', shipped_at)::date as ship_day,
        coalesce(order_amount, 0)           as order_amount
    from {{ ref('stg_shipments') }}
    where date_trunc('day', shipped_at)::date >= dateadd('day', -30, current_date)

),

daily_shipped as (

    select
        ship_day,
        sum(order_amount) as shipped_amount
    from shipments
    group by ship_day

),

daily_returned as (

    select
        return_day,
        count(*)                                        as rma_volume,
        sum(refund_amount)                              as refunded_amount,
        sum(case when is_restocked then 1 else 0 end)   as restocked_units
    from returns
    group by return_day

)

select
    s.ship_day                                          as report_date,
    coalesce(r.rma_volume, 0)                           as rma_volume,
    coalesce(r.restocked_units, 0)                      as restocked_units,
    coalesce(r.refunded_amount, 0)                      as refunded_amount,
    s.shipped_amount,
    round(100.0 * coalesce(r.refunded_amount, 0) / nullif(s.shipped_amount, 0), 2) as percent_refunded
from daily_shipped as s
left join daily_returned as r
    on s.ship_day = r.return_day
order by report_date

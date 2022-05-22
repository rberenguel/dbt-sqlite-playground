{{ config(materialized = 'table') }} 
with value_of_order as (
    select
        order_id,
        sum(cost) as total_cost
    from {{ ref('stg_cost_per_order_line') }}
    group by 1
),

paid_invoices as (
    select order_id from {{ source ('main', 'invoices') }} where status = 'PAID'
)

select
    'total' as total,
    sum(value_of_order.total_cost) as money_in
from
    paid_invoices
inner join
    value_of_order on paid_invoices.order_id = value_of_order.order_id
group by 1

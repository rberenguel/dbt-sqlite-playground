{{ config(materialized = 'table') }} 

with price_per_product as (
    select
        id as product_id,
        price
    from {{ source('main', 'products') }}
),

order_lines as (
    select
        id as order_id,
        product_id,
        qty
    from {{ source('main', 'orders') }}
)

select
    order_lines.order_id,
    price_per_product.product_id,
    order_lines.qty * price_per_product.price as cost
from order_lines
inner join
    price_per_product on order_lines.product_id = price_per_product.product_id

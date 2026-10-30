{{ config(materialized='table') }}

WITH customers AS (

    SELECT DISTINCT
        customer_id

    FROM {{ ref('stg_sales') }}

    WHERE customer_id IS NOT NULL

)

SELECT
    MD5(customer_id) AS customer_key,
    customer_id

FROM customers

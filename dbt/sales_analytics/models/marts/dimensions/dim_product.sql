{{ config(materialized='table') }}

WITH products AS (

    SELECT DISTINCT
        UPPER(TRIM(product)) AS product_name

    FROM {{ ref('stg_sales') }}

    WHERE NULLIF(TRIM(product), '') IS NOT NULL

)

SELECT
    MD5(product_name) AS product_key,
    product_name

FROM products

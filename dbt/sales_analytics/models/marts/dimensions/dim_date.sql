{{ config(materialized='table') }}

WITH dates AS (

    SELECT DISTINCT
        sale_date

    FROM {{ ref('stg_sales') }}

    WHERE sale_date IS NOT NULL

)

SELECT
    TO_NUMBER(TO_CHAR(sale_date, 'YYYYMMDD')) AS date_key,
    sale_date AS full_date,
    YEAR(sale_date) AS year,
    MONTH(sale_date) AS month,
    QUARTER(sale_date) AS quarter,
    DAY(sale_date) AS day

FROM dates

{{ config(materialized='table') }}

WITH sales AS (

    SELECT
        source_file,
        source_row_number,
        customer_id,
        product,
        sale_date,
        quantity,
        unit_price

    FROM {{ ref('stg_sales') }}

),

final AS (

    SELECT
        MD5(
            CONCAT(
                s.source_file,
                '|',
                s.source_row_number::VARCHAR
            )
        ) AS sales_line_key,

        c.customer_key,
        p.product_key,
        d.date_key,

        s.quantity,
        s.unit_price,

        s.quantity * s.unit_price AS total_amount,

        s.source_file,
        s.source_row_number

    FROM sales AS s

    LEFT JOIN {{ ref('dim_customer') }} AS c
        ON s.customer_id = c.customer_id

    LEFT JOIN {{ ref('dim_product') }} AS p
        ON UPPER(TRIM(s.product)) = p.product_name

    LEFT JOIN {{ ref('dim_date') }} AS d
        ON s.sale_date = d.full_date

)

SELECT *
FROM final
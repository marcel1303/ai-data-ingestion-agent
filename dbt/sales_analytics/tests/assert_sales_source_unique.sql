SELECT
    source_file,
    source_row_number,
    COUNT(*) AS total_registros

FROM {{ ref('stg_sales') }}

GROUP BY
    source_file,
    source_row_number

HAVING COUNT(*) > 1
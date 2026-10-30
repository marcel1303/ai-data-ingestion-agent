{{ config(materialized='view') }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'sales') }}

),

renamed AS (

    SELECT
        CUSTOMER_ID AS customer_id,

        TRY_TO_DATE(SALE_DATE, 'YYYY-MM-DD') AS sale_date,

        TRIM(PRODUCT) AS product,

        TRY_TO_NUMBER(QUANTITY) AS quantity,

        TRY_TO_DECIMAL(UNIT_PRICE, 12, 2) AS unit_price,

        SOURCE_FILE AS source_file,

        SOURCE_ROW_NUMBER AS source_row_number,

        INGESTED_AT AS ingested_at

    FROM source

)

SELECT *
FROM renamed
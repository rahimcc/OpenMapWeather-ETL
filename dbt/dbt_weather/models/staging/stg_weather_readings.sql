{{ config( materialized='view') }}


SELECT
    id,
    city,
    temp,
    humidity,
    weather_condition,
    recorded_at,
    ingested_at
FROM  {{ source('raw','weather_readings') }}   
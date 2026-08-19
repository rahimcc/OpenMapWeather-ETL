{{ config( materialized = 'table')}}


SELECT 
    city, 
    date_trunc('day', recorded_at ) as day,
    avg(temp) as avg_temp,
    min(temp) as min_temp,
    max(temp) as max_temp,
    avg(humidity) as avg_humidity

FROM {{ ref('stg_weather_readings')}}
GROUP BY city, date_trunc('day', recorded_at)


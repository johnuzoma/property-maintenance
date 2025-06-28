WITH stg_pm AS (
    SELECT * FROM {{ ref('stg_property_maintenance') }}
)

SELECT DISTINCT region_name
FROM stg_pm
WHERE LENGTH(region_name) <> 1
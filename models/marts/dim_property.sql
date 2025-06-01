SELECT DISTINCT
    region_name,
    property_id,
    construction_year,
    EXTRACT(YEAR FROM CURRENT_DATE()) - construction_year AS age
FROM
    {{ ref('stg_property_maintenance') }}
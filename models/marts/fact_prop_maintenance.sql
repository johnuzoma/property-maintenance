SELECT
    property_id, 
    repair_year, 
    occupants, 
    repair_count,
    repair_cost
FROM
    {{ ref('stg_property_maintenance') }}
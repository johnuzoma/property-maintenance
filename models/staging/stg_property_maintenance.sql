SELECT
    region_name,
    property_id,
    construction_year,
    repair_year, 
    occupants, 
    repair_count, 
    total_repair_cost AS repair_cost
FROM
    {{ source('property_data', 'property_maintenance')}} 
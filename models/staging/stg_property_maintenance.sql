SELECT
    region_name,
    property_id,
    construction_year,
    repair_year, 
    occupants, 
    repair_count, 
    total_repair_cost AS repair_cost
    {#
    total_repair_cost stored in euro, convert it to cents
    {{ euro_to_cents(column_name='total_repair_cost', decimal_places=4) }} AS repair_cost
    #}
FROM
    {{ source('property_data', 'property_maintenance')}} 


--{{ limit_data_in_dev(column_name='repair_count', dev_days_of_data=1000) }}

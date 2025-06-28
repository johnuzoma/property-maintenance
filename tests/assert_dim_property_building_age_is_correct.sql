WITH dm AS (
    SELECT * FROM {{ ref('dim_property')}}
)

SELECT
    age
FROM
    dm
WHERE
    age <> (EXTRACT(YEAR FROM CURRENT_DATE()) - construction_year)
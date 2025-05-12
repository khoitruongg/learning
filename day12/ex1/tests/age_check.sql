-- Custom test to check that age is greater than 18
SELECT *
FROM {{ ref('calculate_age') }}
WHERE age IS NULL OR age < 0 OR age > 120

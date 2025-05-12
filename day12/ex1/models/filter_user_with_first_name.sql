-- models/filtered_users.sql

WITH raw_data AS (
    SELECT
        "index",
        "user_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "date_of_birth",
        "job_title"
    FROM {{ source('user_data', 'user') }}  -- Reference to the user table (raw data)
)

SELECT
    "index",
    "user_id",
    "first_name",
    "last_name",
    "email",
    "phone",
    "date_of_birth",
    "job_title"
FROM raw_data
WHERE
    first_name IS NOT NULL
    AND first_name LIKE 'J%'  -- Filter for first name starting with 'J'

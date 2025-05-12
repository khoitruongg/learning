
  create view "user_db"."public"."filter_user_with_first_name__dbt_tmp"
    
    
  as (
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
    FROM "user_db"."public"."user"  -- Reference to the user table (raw data)
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
    email IS NOT NULL
    AND first_name LIKE 'J%'  -- Filter for first name starting with 'J'
  );
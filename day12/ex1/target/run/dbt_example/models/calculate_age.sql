
  create view "user_db"."public"."calculate_age__dbt_tmp"
    
    
  as (
    WITH raw_data AS (
    SELECT
        "index",
        "user_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "date_of_birth",
        "job_title",
        DATE_PART('year', age("date_of_birth"::date)) AS age
    FROM "user_db"."public"."user"  -- Reference to the source 'user' in the 'user_data' schema
)
SELECT
    "index",
    "user_id",
    "first_name",
    "last_name",
    "email",
    "phone",
    "date_of_birth",
    "job_title",
    age
FROM raw_data
  );
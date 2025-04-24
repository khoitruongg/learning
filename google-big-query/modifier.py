from google.cloud import bigquery
from google.auth import default
import random

# credentials, project = default()
# print("Project:", project)
# print("Authenticated email:", credentials.service_account_email if hasattr(credentials, 'service_account_email') else "User credentials in use")

project_id = 'atomic-airship-457603-f7'
dataset_id = 'exampleData'
table_id = 'worker'

table_ref = f"{project_id}.{dataset_id}.{table_id}"

# Initialize the BigQuery client and specify the project
client = bigquery.Client(project=project_id)

# SQL query
query = f"""
    SELECT Variable_name, 
           Variable_code,
           Year,
           Value, 
           CONCAT(CAST(Variable_name AS STRING), CAST(Variable_code AS STRING)) AS NameCode,  # Concatenate the two string columns
           SUM(SAFE_CAST(Value AS INT64)) AS total_count  # Summing the Value as INT64,
    FROM `{table_ref}`
    WHERE SAFE_CAST(Value AS INT64) IS NOT NULL
    GROUP BY Variable_name, Year, Value, Variable_code  # Group by both Variable_name and Year
    ORDER BY total_count DESC
    LIMIT 10;
"""

# Run the query
query_job = client.query(query)

# Wait for the job to complete and fetch the results
results = query_job.result()

# Display the results
for row in results:
    print(f"Name: {row.Variable_code}, Value: {row.Value}, Year: {row.Year}, Code: {row.NameCode}")

# Get user input
min_value = input("Enter Min Value to filter: ")

filterQuery = f"""
SELECT Variable_name, 
           Variable_code,
           Year,
           Value, 
           CONCAT(CAST(Variable_name AS STRING), CAST(Variable_code AS STRING)) AS NameCode,  # Concatenate the two string columns
           SUM(SAFE_CAST(Value AS INT64)) AS total_count  # Summing the Value as INT64,
    FROM {table_ref}
    WHERE SAFE_CAST(Value AS INT64) IS NOT NULL
          AND SAFE_CAST(Value AS INT64) >= @min_value
    GROUP BY Variable_name, Year, Value, Variable_code  # Group by both Variable_name and Year
    ORDER BY total_count DESC
    LIMIT 10;
"""

# Query parameters
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("min_value", "INT64", min_value),
    ]
)

# # Example modification: add a new column
modifiedResult = client.query(filterQuery, job_config=job_config).to_dataframe()
modifiedResult["Age"] = modifiedResult.apply(lambda _: random.randint(1, 100), axis=1)

print('================ MODIFIED DATA ============')
for row in modifiedResult.itertuples():
    print(f"Name: {row.Variable_code}, Value: {row.Value}, Year: {row.Year}, Code: {row.NameCode}, Age: {row.Age}")

job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_TRUNCATE",  # or WRITE_APPEND
    autodetect=True,
)

job = client.load_table_from_dataframe(modifiedResult, table_ref, job_config=job_config)
job.result()  # Wait for the job to complete

print(f"✅ Loaded {job.output_rows} rows into {table_ref}")



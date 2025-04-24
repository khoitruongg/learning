from google.cloud import bigquery
from google.auth import default

credentials, project = default()
print("Project:", project)
print("Authenticated email:", credentials.service_account_email if hasattr(credentials, 'service_account_email') else "User credentials in use")


# Initialize the BigQuery client and specify the project
client = bigquery.Client(project="atomic-airship-457603-f7")

# SQL query
query = """
    SELECT corpus,word, SUM(word_count) as total_count
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus,word
    ORDER BY total_count DESC
    LIMIT 20;
"""

# Run the query
query_job = client.query(query)

# Wait for the job to complete and fetch the results
results = query_job.result()

# Display the results
for row in results:
    print(f"Word: {row.word}, Corpus: {row.corpus}, Total Count: {row.total_count}")


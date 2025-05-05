import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
from datetime import datetime
import random
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

INPUT_FILE = 'example.csv'
CHUNK_SIZE = 100000  # Number of rows per chunk

# Get Google Cloud project and credentials path from environment variables
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Set up Google Cloud credentials using the service account key file
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Initialize BigQuery client
client = bigquery.Client(credentials=credentials, project=project_id)

def random_datetime(start, end):
    """Generate a random datetime between two datetime objects."""
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def add_unique_column(local_file_path):
    """Add a unique ID column to the CSV file using pandas."""
    df = pd.read_csv(local_file_path)

    # Insert a new column at the first position with incremental unique IDs
    df.insert(0, 'id', range(1, len(df) + 1))

    # Define datetime range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 1, 1)

    # Add a Created_Date column with random datetime values
    df['Created_Date'] = [random_datetime(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
                          for _ in range(len(df))]
    # Save to a temporary file
    temp_file_path = "temp_with_ids.csv"
    df.to_csv(temp_file_path, index=False)

    return temp_file_path

def upload_to_bigquery(local_file_path, table_id):
    """Upload a CSV file to BigQuery."""

    # Add unique ID column to the CSV data before uploading
    local_file_path = add_unique_column(local_file_path)

    # Load the data into BigQuery from the local file
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip header row in CSV
        autodetect=True,  # Auto-detect schema
    )
    
    with open(local_file_path, "rb") as file:
        load_job = client.load_table_from_file(file, table_id, job_config=job_config)

    # Wait for the job to complete
    load_job.result()
    print(f"Data uploaded to {table_id}")

def exploreResult(dataset_id, table_name):
    # Explore the data using SQL
    query = f"""
        SELECT *
        FROM `{dataset_id}.{table_name}`
        LIMIT 10
    """
    query_job = client.query(query)

    # Fetch the query results
    results = query_job.result()

    # Display the results
    for row in results:
        print(row)

def main():
    table_dataset = input("Enter the name of the BigQuery dataset name: ")
    table_name = input("Enter the name of the BigQuery table to insert: ")

    # Define the full table reference
    table_id = f"{project_id}.{table_dataset}.{table_name}"
    
    # Upload to BigQuery after processing
    upload_to_bigquery(INPUT_FILE, table_id)
    exploreResult(table_dataset ,table_name)

if __name__ == '__main__':
    main()

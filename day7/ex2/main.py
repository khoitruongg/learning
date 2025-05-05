import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

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
client = bigquery.Client(project=project_id)

from google.cloud import bigquery

def create_partitioned_table(project_id, dataset_id, original_table_id, new_table_id, partition_column):
    """Create a partitioned table from an existing table in BigQuery."""
    client = bigquery.Client(project=project_id)

    # Define the SQL query to create a partitioned table from the original table
    # Define the SQL query to create a partitioned table from the original table
    # sql = f"""
    # CREATE TABLE `{project_id}.{dataset_id}.{new_table_id}`
    # PARTITION BY RANGE_BUCKET({partition_column}, GENERATE_ARRAY(0, 21, 1))
    # AS
    # (
    #  SELECT * 
    #  FROM `{project_id}.{dataset_id}.{original_table_id}`
    #  WHERE {partition_column} IS NOT NULL
    # )
    # """

    sql = f"""
    CREATE TABLE `{project_id}.{dataset_id}.{new_table_id}`
    PARTITION BY DATE({partition_column})
    AS
    (
     SELECT * 
     FROM `{project_id}.{dataset_id}.{original_table_id}`
     WHERE {partition_column} IS NOT NULL
    )
    """

    # Run the query
    print('>>>> SQL: ', sql)
    query_job = client.query(sql)

    # Wait for the query to complete
    query_job.result()

    print(f"Partitioned table '{new_table_id}' created successfully in dataset '{dataset_id}'.")

def main():
    table_dataset = input("Enter the name of the BigQuery dataset name: ")
    original_table = input("Enter the name of the table name source: ")
    new_table_id = input("Enter the name of the new table after Parition: ")
    partition_column = input("Enter the name of the field you want to filter: ")

    # Example usage
    create_partitioned_table(
        project_id=project_id, 
        dataset_id=table_dataset, 
        original_table_id=original_table, 
        new_table_id=new_table_id, 
        partition_column=partition_column
    )

if __name__ == '__main__':
    main()

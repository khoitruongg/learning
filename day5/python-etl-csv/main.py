import pandas as pd
import os
from google.cloud import bigquery

# === CONFIG ===
INPUT_FILE = 'example.csv'
OUTPUT_FILE = 'cleaned_output.csv'
CHUNK_SIZE = 100000  # Number of rows per chunk
BQ_PROJECT_ID = 'atomic-airship-457603-f7'  # Your Google Cloud Project ID

# Initialize BigQuery client
client = bigquery.Client(project=BQ_PROJECT_ID)

def transform(chunk):
    """
    Apply transformation logic to a DataFrame chunk.
    Clean columns based on the column names and handle missing values.
    """
    # Example: Normalize the Data_value column (convert to numeric)
    chunk['Data_value'] = pd.to_numeric(chunk['Data_value'], errors='coerce')  # Coerce errors to NaN
    
    # Drop rows with NaN in important columns (e.g., Data_value)
    chunk = chunk.dropna(subset=['Data_value', 'Series_reference', 'Period'])
    
    # Optionally: Normalize Data_value or other columns
    chunk['Data_value'] = chunk['Data_value'] / 100  # Just an example transformation
    
    return chunk

def upload_to_bigquery(local_file_path, project_id, dataset_name, table_name):
    """Upload a CSV file to BigQuery."""
    # Define the full table reference
    table_id = f"{project_id}.{dataset_name}.{table_name}"
    
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

def main():
    # os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    first_chunk = True
    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):
        processed_chunk = transform(chunk)
        processed_chunk.to_csv(
            OUTPUT_FILE,
            mode='w' if first_chunk else 'a',
            header=first_chunk,
            index=False
        )
        first_chunk = False
        print(f"Processed chunk with {len(processed_chunk)} rows.")
    print("✅ ETL process completed.")

    table_dataset = input("Enter the name of the BigQuery dataset name: ")
    table_name = input("Enter the name of the BigQuery table to insert: ")
    # Upload to BigQuery after processing
    upload_to_bigquery(OUTPUT_FILE, BQ_PROJECT_ID, table_dataset, table_name)

if __name__ == '__main__':
    main()

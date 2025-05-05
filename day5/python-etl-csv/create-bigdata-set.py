from google.cloud import bigquery

def create_bigquery_dataset():
    # Get project ID and dataset name from the user
    project_id = 'atomic-airship-457603-f7'
    dataset_id = input("Enter the name of the BigQuery dataset to create: ")

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Define dataset reference
    dataset_ref = client.dataset(dataset_id)

    # Define dataset configuration
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"  # Choose the location for your dataset, e.g., "US" or "EU"

    # Create the dataset
    try:
        dataset = client.create_dataset(dataset)  # Make an API request.
        print(f"Dataset {dataset_id} created successfully in project {project_id}.")
    except Exception as e:
        print(f"Error creating dataset: {e}")

# Call the function to create the dataset
if __name__ == '__main__':
    create_bigquery_dataset()

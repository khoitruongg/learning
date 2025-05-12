import json
import requests

# Load your schema file
with open('avro/user2.avsc', 'r') as f:
    new_schema = f.read()

# Define the compatibility endpoint
url = 'http://localhost:8083/compatibility/subjects/users-value/versions/latest'

# Set up the headers
headers = {
    'Content-Type': 'application/vnd.schemaregistry.v1+json',
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps({'schema': new_schema}))

# Check compatibility result
if response.status_code == 200:
    compatibility = response.json()
    if compatibility['is_compatible']:
        print("Schema is compatible")
    else:
        print(f"Incompatibility found: {compatibility}")
else:
    print(f"Error checking compatibility: {response.status_code} {response.text}")

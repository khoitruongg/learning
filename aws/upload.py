import boto3
import os

endpoint_url = "http://localhost:4566"

# Set up the S3 client pointing to LocalStack
s3 = boto3.client(
    "s3",
    endpoint_url=endpoint_url,  # LocalStack endpoint
    aws_access_key_id="12345",              # Dummy credentials for LocalStack
    aws_secret_access_key="khoitm-aws",
    region_name="us-east-1"
)

bucket_name = "test-bucket"
file_path = "./example.txt"
s3_key = "uploads/example.txt"

# 1. Create the bucket (if it doesn't exist)
s3.create_bucket(Bucket=bucket_name)

# 2. Upload the file
with open(file_path, "rb") as f:
    s3.upload_fileobj(f, bucket_name, s3_key, ExtraArgs={
        'ACL': 'public-read',
        'ContentType': 'text/plain'  # Ensure content type is set
    })

print(f"✅ File '{file_path}' uploaded to S3 bucket '{bucket_name}' as '{s3_key}'")

file_url = f"{endpoint_url}/{bucket_name}/{s3_key}"
print(f"📎 File URL: {file_url}")


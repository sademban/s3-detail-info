import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')
bucket = os.getenv('BUCKET_NAME')

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Count objects and sum size
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket)

object_count = 0
total_size_bytes = 0

for page in pages:
    if 'Contents' in page:
        object_count += len(page['Contents'])
        total_size_bytes += sum(obj['Size'] for obj in page['Contents'])

# Convert size to MB and GB
total_size_mb = total_size_bytes / (1024 ** 2)
total_size_gb = total_size_bytes / (1024 ** 3)

print(f"Total objects in '{bucket}': {object_count}")
print(f"Total size: {total_size_bytes} Bytes")
print(f"Total size: {total_size_mb:.2f} MB")
print(f"Total size: {total_size_gb:.2f} GB")

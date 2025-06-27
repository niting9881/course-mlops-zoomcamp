import pandas as pd
from datetime import datetime
import boto3
import os

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

# Step 1: Create the DataFrame
data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]
columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df_input = pd.DataFrame(data, columns=columns)

# Step 2: LocalStack S3 setup
s3_endpoint_url = 'http://localhost:4566'
bucket_name = 'nyc-duration'
parquet_file_key = 'in/2023-01.parquet'

# Step 3: Create bucket if not exists
s3_client = boto3.client(
    's3',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1',
    endpoint_url=s3_endpoint_url
)

existing_buckets = s3_client.list_buckets()
if not any(bucket['Name'] == bucket_name for bucket in existing_buckets.get('Buckets', [])):
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created.")
else:
    print(f"Bucket '{bucket_name}' already exists.")

# Step 4: Write DataFrame as Parquet to LocalStack S3
options = {
    'client_kwargs': {
        'endpoint_url': s3_endpoint_url
    }
}

s3_path = f's3://{bucket_name}/{parquet_file_key}'

df_input.to_parquet(
    s3_path,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

print(f"Parquet file written to {s3_path}")

# Step 5: Check file size at S3
response = s3_client.head_object(Bucket=bucket_name, Key=parquet_file_key)
file_size_bytes = response['ContentLength']

print(f"Size of '{parquet_file_key}' in bucket '{bucket_name}': {file_size_bytes} bytes")

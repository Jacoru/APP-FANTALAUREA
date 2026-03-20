import boto3
import os
import io
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)


def download_to_s3():
    bucket_name = "fanta-laurea"
    object_key = "persone.csv"

    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    content = response['Body'].read().decode('utf-8')
    return content

def upload_to_s3(df):
    buffer = io.StringIO()
    
    df.to_csv(buffer, index=False)

    bucket_name = "fanta-laurea"
    object_key = "persone.csv"
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=buffer.getvalue())
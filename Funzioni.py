import boto3
import os
import io
from dotenv import load_dotenv
import streamlit as st
load_dotenv()


def download_to_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name=st.secrets["AWS_REGION"]
    )

    bucket_name = "fanta-laurea"
    object_key = "persone.csv"

    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    content = response['Body'].read().decode('utf-8')
    return content

def upload_to_s3(df):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name=st.secrets["AWS_REGION"]
    )
    buffer = io.StringIO()
    
    df.to_csv(buffer, index=False)

    bucket_name = "fanta-laurea"
    object_key = "persone.csv"
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=buffer.getvalue())

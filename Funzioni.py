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

def carica_stile():
    st.markdown("""
        <style>

        /* Font futuristica */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Orbitron', sans-serif;
            background-color: #0d0d0d;
            color: #e6e6e6;
        }

        /* Titoli neon */
        h1, h2, h3 {
            color: #00eaff;
            text-shadow: 0 0 10px #00eaff;
        }

        /* Pulsanti stile gaming */
        .stButton>button {
            background: linear-gradient(90deg, #00eaff, #8a2be2);
            color: white;
            border: none;
            padding: 0.7rem 1.4rem;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: bold;
            box-shadow: 0 0 10px #00eaff;
            transition: 0.2s ease-in-out;
        }

        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px #8a2be2;
        }

        /* Card stile cyberpunk */
        .card {
            background: rgba(20, 20, 20, 0.8);
            border: 1px solid #8a2be2;
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 0 15px #8a2be2;
        }
        /* Pills neon */
    .pill {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
            margin: 4px;
            color: #ffffff;
            background: linear-gradient(90deg, #8a2be2, #00eaff);
            box-shadow: 0 0 10px #8a2be2, 0 0 10px #00eaff;
            text-shadow: 0 0 5px #000;
            transition: 0.2s ease-in-out;
        }

.pill:hover {
    transform: scale(1.08);
    box-shadow: 0 0 15px #00eaff, 0 0 15px #8a2be2;
}
        /* Input futuristici */
        .stTextInput>div>div>input {
            background-color: #1a1a1a;
            color: #00eaff;
            border: 1px solid #8a2be2;
            border-radius: 8px;
        }

        /* Sidebar neon */
        section[data-testid="stSidebar"] {
            background-color: #111;
            border-right: 2px solid #8a2be2;
        }

        /* Slider neon */
        .stSlider > div > div > div {
            background: linear-gradient(90deg, #00eaff, #8a2be2);
        }

        /* Tabelle stile gaming */
        .stDataFrame, .stTable {
            border: 1px solid #8a2be2;
            box-shadow: 0 0 10px #8a2be2;
        }

        </style>
    """, unsafe_allow_html=True)


import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    return os.getenv("ABUSEIPDB_API_KEY", "").strip()

def config_has_api_key():
    return bool(get_api_key())

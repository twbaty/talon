import os
import requests
from utils.logging import log_error

ABUSEIPDB_API = "https://api.abuseipdb.com/api/v2/check"

def query_abuseipdb(ip):
    api_key = os.getenv("ABUSEIPDB_KEY")
    if not api_key:
        return {"error": "Missing AbuseIPDB API key"}

    headers = {
        "Accept": "application/json",
        "Key": api_key
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(ABUSEIPDB_API, headers=headers, params=params)
        return response.json()
    except Exception as e:
        log_error(f"AbuseIPDB API call failed: {e}")
        return {"error": str(e)}

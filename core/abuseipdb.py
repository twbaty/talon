# abuseipdb.py

import os
import requests
from utils.logging import log_error

ABUSEIPDB_API = "https://api.abuseipdb.com/api/v2/check"

def query_abuseipdb(ip):
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    if not api_key:
    print(f"[INFO] No API key found. Opening AbuseIPDB page for {ip}")
    return {"redirect": f"https://www.abuseipdb.com/check/{ip}"}

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

# core/abuseipdb.py

import os
import requests

def check_ip(ip):
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    if not api_key:
        return {"error": "ABUSEIPDB_API_KEY not set"}

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

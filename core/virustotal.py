# core/virustotal.py

import os
import requests

def check_ip(ip):
    api_key = os.getenv("VIRUSTOTAL_API_KEY")
    if not api_key:
        return {
            "error": "VIRUSTOTAL_API_KEY not set"
        }

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": api_key}

    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

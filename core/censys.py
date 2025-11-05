# core/censys.py

import os
import requests
from requests.auth import HTTPBasicAuth

def check_ip(ip):
    api_id = os.getenv("CENSYS_API_ID")
    api_secret = os.getenv("CENSYS_API_SECRET")
    if not api_id or not api_secret:
        return {"error": "CENSYS_API_ID or CENSYS_API_SECRET not set"}

    url = f"https://search.censys.io/api/v2/hosts/{ip}"

    try:
        response = requests.get(url, auth=HTTPBasicAuth(api_id, api_secret))
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

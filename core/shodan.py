# core/shodan.py

import os
import requests

def check_ip(ip):
    api_key = os.getenv("SHODAN_API_KEY")
    if not api_key:
        return {"error": "SHODAN_API_KEY not set"}

    url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
    
    try:
        response = requests.get(url)
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

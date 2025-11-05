import os
import requests
from urllib.parse import quote


def check_ip(ip):
api_key = os.getenv("ABUSEIPDB_API_KEY")
if not api_key:
return {"mode": "unauthenticated", "url": f"https://www.abuseipdb.com/check/{quote(ip)}"}
url = "https://api.abuseipdb.com/api/v2/check"
headers = {"Key": api_key, "Accept": "application/json"}
params = {"ipAddress": ip, "maxAgeInDays": 90}
response = requests.get(url, headers=headers, params=params)


if response.status_code != 200:
return {"mode": "authenticated", "error": response.text}
return {"mode": "authenticated", **response.json().get("data", {})}

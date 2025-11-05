import os
import requests


def check_ip(ip):
api_id = os.getenv("CENSYS_API_ID")
api_secret = os.getenv("CENSYS_API_SECRET")
if not api_id or not api_secret:
return {"mode": "unauthenticated", "url": f"https://search.censys.io/hosts/{ip}"}


url = f"https://search.censys.io/api/v2/hosts/{ip}"
response = requests.get(url, auth=(api_id, api_secret))
if response.status_code != 200:
return {"mode": "authenticated", "error": response.text}
return {"mode": "authenticated", **response.json()}

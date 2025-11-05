import os
import requests


def check_ip(ip):
api_key = os.getenv("VIRUSTOTAL_API_KEY")
if not api_key:
return {"mode": "unauthenticated", "url": f"https://www.virustotal.com/gui/ip-address/{ip}"}


url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
headers = {"x-apikey": api_key}
response = requests.get(url, headers=headers)
if response.status_code != 200:
return {"mode": "authenticated", "error": response.text}
return {"mode": "authenticated", **response.json()}

import os
import requests


def check_ip(ip):
api_key = os.getenv("SHODAN_API_KEY")
if not api_key:
return {"mode": "unauthenticated", "url": f"https://www.shodan.io/host/{ip}"}


url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
response = requests.get(url)
if response.status_code != 200:
return {"mode": "authenticated", "error": response.text}
return {"mode": "authenticated", **response.json()}

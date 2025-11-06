### abuseipdb.py (core logic updated)
import os
import requests
from bs4 import BeautifulSoup

def query_abuseipdb(ip_address: str, use_api_key: bool):
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    results = {}

    if use_api_key and api_key:
        # Use API key path
        headers = {
            'Key': api_key,
            'Accept': 'application/json'
        }
        params = {
            'ipAddress': ip_address,
            'maxAgeInDays': '90'
        }
        try:
            response = requests.get('https://api.abuseipdb.com/api/v2/check', headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                results = {
                    'source': 'api',
                    'ipAddress': data['data']['ipAddress'],
                    'abuseConfidenceScore': data['data']['abuseConfidenceScore'],
                    'totalReports': data['data']['totalReports'],
                    'usageType': data['data'].get('usageType', 'n/a')
                }
            else:
                results = {'error': f"API error: {response.status_code} - {response.text}"}
        except Exception as e:
            results = {'error': f"API exception: {e}"}
    else:
        # No API key path - fallback to HTML scrape
        try:
            url = f"https://www.abuseipdb.com/check/{ip_address}"
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")

            score_tag = soup.select_one(".confidence_score")
            usage_tag = soup.find("th", string="Usage Type")
            usage_value = usage_tag.find_next("td").text.strip() if usage_tag else "n/a"

            results = {
                'source': 'html',
                'ipAddress': ip_address,
                'abuseConfidenceScore': score_tag.text.strip() if score_tag else "n/a",
                'usageType': usage_value,
                'totalReports': 'n/a (HTML fallback)'
            }
        except Exception as e:
            results = {'error': f"Fallback exception: {e}"}

    return results

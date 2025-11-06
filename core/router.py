import requests
import os
from bs4 import BeautifulSoup
from core.config import get_api_key, config_has_api_key
from core.abuseipdb import query_abuseipdb

def abuseipdb_api_lookup(ip: str):
    """Query AbuseIPDB using the API key (JSON response)."""
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("API key not found")

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()["data"]

    return {
        "ip": ip,
        "source": "AbuseIPDB API",
        "abuse_score": data.get("abuseConfidenceScore"),
        "reports": data.get("totalReports"),
        "country": data.get("countryCode"),
    }

def abuseipdb_html_lookup(ip: str):
    """Query AbuseIPDB public page (HTML fallback)."""
    url = f"https://www.abuseipdb.com/check/{ip}"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Try to find the abuse confidence score
    score_elem = soup.find("div", class_="well")
    score_text = score_elem.get_text(strip=True) if score_elem else "Not found or layout changed"

    return {
        "ip": ip,
        "source": "AbuseIPDB (HTML fallback)",
        "abuse_score": score_text,
    }

def scan_ip(ip: str, use_api_key: bool = True):
    """
    Router function called by the GUI.
    If use_api_key is True and a key exists, use the API.
    Otherwise, fall back to HTML scraping.
    """
    if use_api_key and config_has_api_key():
        return abuseipdb_api_lookup(ip)
    else:
        return abuseipdb_html_lookup(ip)

import requests
from bs4 import BeautifulSoup
from core.config import get_api_key, config_has_api_key

def query_abuseipdb(ip: str, use_api_key: bool = True):
    if use_api_key and config_has_api_key():
        return _api_lookup(ip)
    else:
        return _html_lookup(ip)

def _api_lookup(ip: str):
    api_key = get_api_key()
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": api_key, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}
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

def _html_lookup(ip: str):
    url = f"https://www.abuseipdb.com/check/{ip}"
    # Use quirky Lynx UA to avoid 403
    headers = {"User-Agent": "Lynx/2.8.9rel.1 libwww-FM/2.14 SSL-MM/1.4.1"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    score_elem = soup.find("div", class_="well")
    score_text = score_elem.get_text(strip=True) if score_elem else "Not found or layout changed"
    return {
        "ip": ip,
        "source": "AbuseIPDB (HTML fallback)",
        "abuse_score": score_text,
    }

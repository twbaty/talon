import os
import requests
from bs4 import BeautifulSoup
from utils.logging import log_error

ABUSEIPDB_API_URL = "https://api.abuseipdb.com/api/v2/check"
ABUSEIPDB_BROWSER_URL = "https://www.abuseipdb.com/check/{}"

def query_abuseipdb(ip, use_api_key=False):
    """
    Attempts to query AbuseIPDB. If API key is present and allowed, use API.
    Otherwise, fall back to scraping HTML.
    """

    api_key = os.getenv("ABUSEIPDB_API_KEY")

    # Use API key only if both present and allowed
    if use_api_key and api_key:
        headers = {
            "Accept": "application/json",
            "Key": api_key
        }
        params = {
            "ipAddress": ip,
            "maxAgeInDays": 90
        }

        try:
            response = requests.get(ABUSEIPDB_API_URL, headers=headers, params=params)
            return response.json()
        except Exception as e:
            log_error(f"AbuseIPDB API call failed: {e}")
            return {"error": f"AbuseIPDB API call failed: {str(e)}"}

    # Fallback: HTML scrape without API key
    try:
        url = ABUSEIPDB_BROWSER_URL.format(ip)
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        # Example: grab Abuse Confidence Score
        score_div = soup.find("div", class_="well")  # update selector if layout changes
        score = None
        if score_div:
            for line in score_div.stripped_strings:
                if "Abuse Confidence Score" in line:
                    score = line
                    break

        return {
            "ip": ip,
            "source": "AbuseIPDB (HTML fallback)",
            "abuse_score": score or "Not found or layout changed"
        }

    except Exception as e:
        log_error(f"AbuseIPDB fallback (HTML) failed: {e}")
        return {"error": f"AbuseIPDB HTML fallback failed: {str(e)}"}

from core.abuseipdb import query_abuseipdb

def scan_ip(ip: str, use_api_key: bool = True):
    # Right now only AbuseIPDB, later add Shodan, VirusTotal, etc.
    return query_abuseipdb(ip, use_api_key=use_api_key)

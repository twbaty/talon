from core.abuseipdb import query_abuseipdb
# from core.shodan import query_shodan
# from core.virustotal import query_virustotal
# from core.censys import query_censys

def scan_ip(ip, use_api_key=False):
    """
    Scans the given IP with selected backends.
    """
    results = {}

    results["AbuseIPDB"] = query_abuseipdb(ip, use_api_key=use_api_key)

    # Future: Add more sources here
    # results["Shodan"] = query_shodan(ip, use_api_key=use_api_key)
    # results["VirusTotal"] = query_virustotal(ip, use_api_key=use_api_key)

    return results

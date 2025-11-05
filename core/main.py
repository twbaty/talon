# core/main.py

from core import abuseipdb, shodan, censys, virustotal

def scan_ip(ip_address):
    results = {}

    results["AbuseIPDB"] = abuseipdb.check_ip(ip_address)
    results["Shodan"] = shodan.query_shodan(ip_address)
    results["Censys"] = censys.query_censys(ip_address)
    results["VirusTotal"] = virustotal.query_virustotal(ip_address)

    return results

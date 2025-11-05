# talon.py

from core import abuseipdb, shodan, censys, virustotal

def scan_ip(service, ip):
    if service == "AbuseIPDB":
        return abuseipdb.check_ip(ip)
    elif service == "Shodan":
        return shodan.check_ip(ip)
    elif service == "Censys":
        return censys.check_ip(ip)
    elif service == "VirusTotal":
        return virustotal.check_ip(ip)
    else:
        return {"error": "Unknown service"}

# Optional: For test runs
if __name__ == "__main__":
    test_ip = "8.8.8.8"
    result = scan_ip("AbuseIPDB", test_ip)
    print(result)

from core.abuseipdb import query_abuseipdb

def scan_ip(service, ip):
    if service == "AbuseIPDB":
        return query_abuseipdb(ip)
    return {"error": f"Unsupported service: {service}"}

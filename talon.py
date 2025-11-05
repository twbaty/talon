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

from gui.main_window import launch_gui

if __name__ == "__main__":
    launch_gui()

import re

def is_valid_ip(ip):
    # IPv4 only for now
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip))

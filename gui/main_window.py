import tkinter as tk
from tkinter import ttk
import json
from core.router import scan_ip
from utils.validators import is_valid_ip

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Talon Recon")

        self.service_var = tk.StringVar(value="AbuseIPDB")
        self.ip_var = tk.StringVar()

        ttk.Label(root, text="Select Service:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(root, textvariable=self.service_var, values=["AbuseIPDB"]).grid(row=0, column=1)

        ttk.Label(root, text="IP Address:").grid(row=1, column=0, sticky="w")
        ttk.Entry(root, textvariable=self.ip_var).grid(row=1, column=1)

        ttk.Button(root, text="Scan", command=self.scan).grid(row=2, column=0, columnspan=2)

        self.result_text = tk.Text(root, height=20, width=60)
        self.result_text.grid(row=3, column=0, columnspan=2)

    def scan(self):
    ip = self.ip_var.get()
    if not is_valid_ip(ip):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "[ERROR] Invalid IP address.")
        return
    service = self.service_var.get()
    result = scan_ip(service, ip)

    self.result_text.delete(1.0, tk.END)

    if "error" in result:
        self.result_text.insert(tk.END, f"[ERROR] {result['error']}")
        return

    # Format and show meaningful data
    display = []
    display.append(f"IP: {result.get('data', {}).get('ipAddress', 'N/A')}")
    display.append(f"Country: {result.get('data', {}).get('countryCode', 'N/A')}")
    display.append(f"Abuse Score: {result.get('data', {}).get('abuseConfidenceScore', 'N/A')}%")
    display.append(f"ISP: {result.get('data', {}).get('isp', 'N/A')}")
    display.append(f"Domain: {result.get('data', {}).get('domain', 'N/A')}")
    display.append(f"Last Reported: {result.get('data', {}).get('lastReportedAt', 'N/A')}")

    self.result_text.insert(tk.END, "\n".join(display))

def launch_gui():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import webbrowser
import requests

# AbuseIPDB API constants
API_URL = "https://api.abuseipdb.com/api/v2/check"
BROWSER_URL_TEMPLATE = "https://www.abuseipdb.com/check/{}"

def open_in_browser(ip):
    url = BROWSER_URL_TEMPLATE.format(ip)
    webbrowser.open(url)

def call_abuseipdb_api(ip, key, output_text):
    headers = {
        'Key': key,
        'Accept': 'application/json'
    }
    params = {
        'ipAddress': ip,
        'maxAgeInDays': 90
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        json_data = response.json()
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"AbuseIPDB Results for {ip}:\n\n")
        output_text.insert(tk.END, json_data)
    except Exception as e:
        messagebox.showerror("API Error", str(e))

def handle_lookup():
    ip = ip_entry.get().strip()
    key = key_entry.get().strip()
    mode = mode_var.get()

    if not ip:
        messagebox.showwarning("Input Error", "Please enter a valid IP address.")
        return

    if mode == "unauth":
        open_in_browser(ip)
    elif mode == "api":
        if not key:
            messagebox.showwarning("API Key Missing", "Please enter an API key for API mode.")
            return
        call_abuseipdb_api(ip, key, output_text)

# GUI setup
root = tk.Tk()
root.title("Talon - AbuseIPDB Lookup")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(main_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W)
ip_entry = ttk.Entry(main_frame, width=30)
ip_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W)

ttk.Label(main_frame, text="API Key (optional):").grid(row=1, column=0, sticky=tk.W)
key_entry = ttk.Entry(main_frame, width=40, show="*")
key_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W)

mode_var = tk.StringVar(value="unauth")
ttk.Label(main_frame, text="Mode:").grid(row=2, column=0, sticky=tk.W)
ttk.Radiobutton(main_frame, text="Unauthenticated (Open in browser)", variable=mode_var, value="unauth").grid(row=2, column=1, sticky=tk.W)
ttk.Radiobutton(main_frame, text="API Mode (use key)", variable=mode_var, value="api").grid(row=2, column=2, sticky=tk.W)

lookup_button = ttk.Button(main_frame, text="Lookup", command=handle_lookup)
lookup_button.grid(row=3, column=0, columnspan=3, pady=10)

output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=20)
output_text.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))

root.mainloop()

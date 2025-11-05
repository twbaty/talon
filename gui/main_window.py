# gui/main_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from talon import scan_ip
from core.main import scan_ip

class TalonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Talon Recon")

        self.service_var = tk.StringVar()
        self.ip_var = tk.StringVar()

        ttk.Label(root, text="Select Service:").grid(column=0, row=0, padx=5, pady=5, sticky="w")
        self.service_combo = ttk.Combobox(root, textvariable=self.service_var, state="readonly")
        self.service_combo['values'] = ["AbuseIPDB", "Shodan", "Censys", "VirusTotal"]
        self.service_combo.grid(column=1, row=0, padx=5, pady=5)
        self.service_combo.current(0)

        ttk.Label(root, text="IP Address:").grid(column=0, row=1, padx=5, pady=5, sticky="w")
        self.ip_entry = ttk.Entry(root, textvariable=self.ip_var)
        self.ip_entry.grid(column=1, row=1, padx=5, pady=5)

        self.scan_button = ttk.Button(root, text="Scan", command=self.run_scan)
        self.scan_button.grid(column=0, row=2, columnspan=2, pady=10)

        self.output_text = tk.Text(root, height=20, width=60, wrap="word")
        self.output_text.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

    def run_scan(self):
        ip = self.ip_var.get()
        service = self.service_var.get()

        if not ip:
            messagebox.showerror("Error", "Please enter an IP address.")
            return

        result = scan_ip(service, ip)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, str(result))


def launch_gui():
    root = tk.Tk()
    app = TalonApp(root)
    root.mainloop()

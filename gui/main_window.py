import tkinter as tk
from tkinter import ttk
import json
from core.router import scan_ip

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
        service = self.service_var.get()
        result = scan_ip(service, ip)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, json.dumps(result, indent=2))

def launch_gui():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

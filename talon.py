"""
TALON - SOC Enrichment Assistant (Starter GUI)
Version: 0.1
"""

import tkinter as tk
from tkinter import ttk
import webbrowser
import re

# Tool definitions
TOOLS = {
    "Tier 1": [
        ("Shodan", "https://www.shodan.io/search?query={input}"),
        ("VirusTotal", "https://www.virustotal.com/gui/search/{input}"),
        ("AbuseIPDB", "https://www.abuseipdb.com/check/{input}"),
        ("URLScan.io", "https://urlscan.io/search/#{input}"),
        ("Hybrid Analysis", "https://www.hybrid-analysis.com/search?query={input}"),
        ("MXToolbox", "https://mxtoolbox.com/SuperTool.aspx?action=mx%3a{input}"),
        ("SSL Labs", "https://www.ssllabs.com/ssltest/analyze.html?d={input}"),
        ("HaveIBeenPwned", "https://haveibeenpwned.com/unifiedsearch/{input}"),
        ("Blacklight", "https://themarkup.org/blacklight?site={input}")
    ],
    "Tier 2": [
        ("ThreatFox", "https://threatfox.abuse.ch/browse/#search={input}"),
        ("AlienVault OTX", "https://otx.alienvault.com/indicator/general/{type}/{input}"),
        ("Any.run", "https://app.any.run/submissions/#search={input}"),
        ("CIRCL Passive DNS", "https://www.circl.lu/services/passive-dns/"),  # Manual
        ("IPinfo.io", "https://ipinfo.io/{input}"),
        ("GreyNoise", "https://viz.greynoise.io/ip/{input}")
    ]
}

# Type detection (very basic)
def detect_type(ioc):
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ioc):
        return "ip"
    elif re.match(r"^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", ioc):
        return "domain"
    elif re.match(r"^[A-Fa-f0-9]{32,64}$", ioc):
        return "hash"
    else:
        return "unknown"

# Main GUI app
class TalonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TALON - SOC Enrichment Assistant")
        self.geometry("720x600")

        self.input_label = ttk.Label(self, text="Enter IOC (IP / URL / Domain / Hash):")
        self.input_label.pack(pady=10)

        self.input_entry = ttk.Entry(self, width=80)
        self.input_entry.pack(pady=5)

        self.detected_type = tk.StringVar()
        self.type_label = ttk.Label(self, textvariable=self.detected_type)
        self.type_label.pack(pady=5)

        self.generate_btn = ttk.Button(self, text="Generate Links", command=self.build_buttons)
        self.generate_btn.pack(pady=10)

        self.button_frame = ttk.Notebook(self)
        self.button_frame.pack(fill="both", expand=True)

        self.frames = {}
        for tier in TOOLS:
            frame = ttk.Frame(self.button_frame)
            self.button_frame.add(frame, text=tier)
            self.frames[tier] = frame

    def build_buttons(self):
        ioc = self.input_entry.get().strip()
        ioc_type = detect_type(ioc)
        self.detected_type.set(f"Detected Type: {ioc_type.upper()}")

        for tier, frame in self.frames.items():
            for widget in frame.winfo_children():
                widget.destroy()

            for name, url in TOOLS[tier]:
                if "{type}" in url:
                    final_url = url.replace("{input}", ioc).replace("{type}", ioc_type)
                else:
                    final_url = url.replace("{input}", ioc)

                b = ttk.Button(frame, text=name, command=lambda u=final_url: webbrowser.open(u))
                b.pack(pady=2, padx=10, anchor='w')


if __name__ == "__main__":
    app = TalonApp()
    app.mainloop()

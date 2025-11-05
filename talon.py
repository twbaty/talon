import tkinter as tk
import webbrowser

# -----------------------------
# Core Tool Config
# -----------------------------
tools = {
    "Tier 1": [
        ("Shodan", "Find exposed devices", "https://www.shodan.io/search?query={}"),
        ("VirusTotal", "IP/URL/File reputation", "https://www.virustotal.com/gui/search/{}"),
        ("AbuseIPDB", "IP abuse reports", "https://www.abuseipdb.com/check/{}"),
        ("URLScan.io", "URL behavior/screenshot", "https://urlscan.io/search/#{}"),
        ("Hybrid Analysis", "Sandbox file/URL analysis", "https://www.hybrid-analysis.com/search?query={}"),
        ("MXToolbox", "Mail/DNS tools", "https://mxtoolbox.com/SuperTool.aspx?action=mx%3a{}&run=toolpage"),
        ("SSL Labs", "Test SSL/TLS config", "https://www.ssllabs.com/ssltest/analyze.html?d={}"),
        ("HaveIBeenPwned", "Email breach lookup", "https://haveibeenpwned.com/unifiedsearch/{}"),
        ("Blacklight", "Website tracker analysis", "https://themarkup.org/blacklight")
    ],
    "Tier 2": [
        ("ThreatFox", "Malicious indicators DB", "https://threatfox.abuse.ch/browse.php?search={}"),
        ("AlienVault OTX", "Threat intelligence pulses", "https://otx.alienvault.com/browse/global/pulses?q={}"),
        ("Any.run", "Interactive malware sandbox", "https://app.any.run/submissions/#{}"),
        ("CIRCL Passive DNS", "Historical DNS data", "https://www.circl.lu/services/passive-dns/"),
        ("IPinfo.io", "IP geolocation info", "https://ipinfo.io/{}/json"),
        ("GreyNoise", "Internet background scanner data", "https://viz.greynoise.io/ip/{}")
    ]
}

# -----------------------------
# GUI App
# -----------------------------
class TalonApp:
    def __init__(self, root):
        self.root = root
        root.title("Talon - SOC Enrichment Launcher")

        # Input bar
        self.entry = tk.Entry(root, width=60, font=("Consolas", 12))
        self.entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Submit button
        submit_btn = tk.Button(root, text="Enrich", command=self.open_links, bg="#2b7a78", fg="white")
        submit_btn.grid(row=0, column=2, padx=5)

        # Tool sections
        self.button_refs = {}
        row_offset = 1
        for tier, entries in tools.items():
            tk.Label(root, text=tier, font=("Arial", 12, "bold"), pady=10).grid(row=row_offset, column=0, sticky="w", padx=10)
            row_offset += 1

            for name, desc, url in entries:
                b = tk.Button(root, text=f"{name}: {desc}", anchor="w", width=60,
                             command=lambda url=url: self.launch_blank(url))
                b.grid(row=row_offset, column=0, columnspan=3, sticky="w", padx=20, pady=2)
                self.button_refs[name] = (b, url)
                row_offset += 1

    def open_links(self):
        value = self.entry.get().strip()
        if not value:
            return

        for name, (btn, url) in self.button_refs.items():
            try:
                full_url = url.format(value) if "{}" in url else url
                btn.config(command=lambda u=full_url: webbrowser.open_new_tab(u))
            except Exception as e:
                print(f"Error creating link for {name}: {e}")

    def launch_blank(self, url):
        webbrowser.open_new_tab(url)

# -----------------------------
# Launch it
# -----------------------------
if __name__ == '__main__':
    root = tk.Tk()
    app = TalonApp(root)
    root.mainloop()

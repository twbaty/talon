import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from core.router import scan_ip
from core.config import config_has_api_key

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Talon Recon GUI")

        # Target IP Entry
        ttk.Label(root, text="Target IP:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.target_ip_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.target_ip_var).grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # API Key Status Checkbox
        self.has_key_var = tk.BooleanVar(value=False)
        self.api_key_checkbox = ttk.Checkbutton(root, text="Use API Key", variable=self.has_key_var)
        self.api_key_checkbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        if not config_has_api_key():
            self.has_key_var.set(False)
            self.api_key_checkbox.state(['disabled'])
        else:
            self.has_key_var.set(False)
            self.api_key_checkbox.state(['!disabled'])

        # Scan Button
        ttk.Button(root, text="Scan", command=self.scan).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Output pane
        self.result_text = scrolledtext.ScrolledText(root, width=80, height=25, wrap=tk.WORD)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Configure grid
        root.columnconfigure(1, weight=1)

    def scan(self):
        target_ip = self.target_ip_var.get().strip()

        if not target_ip:
            messagebox.showerror("Error", "Please enter a target IP.")
            return

        use_api_key = self.has_key_var.get()

        try:
            result = scan_ip(target_ip, use_api_key=use_api_key)
        except Exception as e:
            result = {"error": f"Scan failed: {str(e)}"}

        self.display_results(result)

    def display_results(self, result):
        self.result_text.delete("1.0", tk.END)

        if isinstance(result, dict):
            for k, v in result.items():
                self.result_text.insert(tk.END, f"{k}: {v}\n")
        else:
            self.result_text.insert(tk.END, str(result))


def launch_gui():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

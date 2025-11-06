import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from core.router import scan_ip
from core.config import get_api_key, config_has_api_key

class MainWindow:
    def show_api_key(self):
        api_key = get_api_key()
        if api_key:
            messagebox.showinfo("API Key", f"The current API key is:\n{api_key}")
        else:
            messagebox.showwarning("API Key", "No API key found.")

def __init__(self, root):
    self.root = root
    self.root.title("Talon Recon GUI")

    # Target IP Entry
    ttk.Label(root, text="Target IP:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    self.target_ip_var = tk.StringVar()
    ttk.Entry(root, textvariable=self.target_ip_var).grid(row=0, column=1, padx=5, pady=5, sticky="we")

    # “Ignore API Key” Checkbox
    self.ignore_key_var = tk.BooleanVar(value=False)
    self.api_key_checkbox = tk.Checkbutton(
        root,
        text="Ignore API Key",
        variable=self.ignore_key_var,
        command=self.update_fallback_label  # hook up callback
    )
    self.api_key_checkbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Fallback status label (starts hidden)
    self.fallback_label = ttk.Label(root, text="Fallback mode: manual query", foreground="gray")
    self.fallback_label.grid(row=2, column=0, columnspan=2, padx=5, pady=(0,5))
    self.fallback_label.grid_remove()

    # Initial state based on config
    if not config_has_api_key():
        self.ignore_key_var.set(True)
        self.api_key_checkbox.config(state="disabled")
        self.fallback_label.grid()  # show since forced fallback
    else:
        self.ignore_key_var.set(False)
        self.api_key_checkbox.config(state="normal")
        self.fallback_label.grid_remove()

    # Scan Button
    ttk.Button(root, text="Scan", command=self.scan).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    ttk.Button(root, text="Show API Key", command=self.show_api_key).grid(row=3, column=2, padx=5, pady=5)

    # Output pane
    self.result_text = scrolledtext.ScrolledText(root, width=80, height=25, wrap=tk.WORD)
    self.result_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    root.columnconfigure(1, weight=1)

def update_fallback_label(self):
    if self.ignore_key_var.get():
        self.fallback_label.grid()   # show
    else:
        self.fallback_label.grid_remove()  # hide

        
        # Scan Button
        ttk.Button(root, text="Scan", command=self.scan).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # Show API Key Button (Temporary Debug)
        ttk.Button(root, text="Show API Key", command=self.show_api_key).grid(row=2, column=2, padx=5, pady=5)

        # Output pane
        self.result_text = scrolledtext.ScrolledText(root, width=80, height=25, wrap=tk.WORD)
        self.result_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Configure grid
        root.columnconfigure(1, weight=1)

    def scan(self):
        target_ip = self.target_ip_var.get().strip()

        if not target_ip:
            messagebox.showerror("Error", "Please enter a target IP.")
            return

        ignore_key = self.ignore_key_var.get()
        use_api_key = not ignore_key

        print(f"[DEBUG] ignore_key = {ignore_key}")
        print(f"[DEBUG] use_api_key = {use_api_key}")

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

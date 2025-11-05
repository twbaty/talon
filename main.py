
# recon_gui/main.py

import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import json
import os

from modules import censys
from modules.base_module import ReconModule
from utils.command_builder import render_template

MODULES = {
    "Censys": censys.CensysModule()
}

class TalonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Talon Recon Query Builder")

        self.selected_module = tk.StringVar()
        self.selected_query = tk.StringVar()
        self.param_entries = {}

        # Module dropdown
        ttk.Label(root, text="Recon Module").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.module_dropdown = ttk.Combobox(root, textvariable=self.selected_module, values=list(MODULES.keys()), state="readonly")
        self.module_dropdown.grid(row=0, column=1, padx=10, pady=5)
        self.module_dropdown.bind("<<ComboboxSelected>>", self.on_module_change)

        # Query dropdown
        ttk.Label(root, text="Query Template").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.query_dropdown = ttk.Combobox(root, textvariable=self.selected_query, state="readonly")
        self.query_dropdown.grid(row=1, column=1, padx=10, pady=5)
        self.query_dropdown.bind("<<ComboboxSelected>>", self.on_query_change)

        # Frame for dynamic param fields
        self.params_frame = ttk.LabelFrame(root, text="Parameters")
        self.params_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Output field
        ttk.Label(root, text="Final Query").grid(row=3, column=0, sticky="nw", padx=10, pady=5)
        self.output_text = tk.Text(root, height=4, width=60)
        self.output_text.grid(row=3, column=1, padx=10, pady=5)

        # Render button
        ttk.Button(root, text="Build Query", command=self.build_query).grid(row=4, column=1, sticky="e", padx=10, pady=10)

        # Load initial module
        self.module_dropdown.current(0)
        self.on_module_change()

    def on_module_change(self, event=None):
        module_name = self.selected_module.get()
        self.current_module = MODULES[module_name]
        self.query_templates = self.current_module.get_queries()
        self.query_dropdown["values"] = list(self.query_templates.keys())
        if self.query_templates:
            self.query_dropdown.current(0)
            self.on_query_change()

    def on_query_change(self, event=None):
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()

        template_key = self.selected_query.get()
        template = self.query_templates.get(template_key, "")
        needed_params = [p.strip("{}") for p in template.split() if p.startswith("{") and p.endswith("}")]
        
        for i, param in enumerate(needed_params):
            ttk.Label(self.params_frame, text=param).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entry = ttk.Entry(self.params_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.param_entries[param] = entry

    def build_query(self):
        template_key = self.selected_query.get()
        template = self.query_templates.get(template_key, "")
        params = {k: e.get() for k, e in self.param_entries.items()}
        result = self.current_module.render_query(template, params)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = TalonApp(root)
    root.mainloop()

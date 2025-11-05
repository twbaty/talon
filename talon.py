# talon/main.py

import tkinter as tk
from tkinter import ttk
import importlib
import json
import os
import re

from modules import censys
from modules.base_module import ReconModule
from utils.command_builder import render_template

# Load field definitions for dynamic builder
def load_fields():
    with open(os.path.join("data", "fields_censys.json")) as f:
        return json.load(f)

MODULES = {
    "Censys": censys.CensysModule()
}

class TalonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Talon Recon Query Builder")

        self.fields = load_fields()
        self.conditions = []

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.build_template_tab()
        self.build_field_tab()

    # ---------------- Template Tab ----------------
    def build_template_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Template Builder")

        self.selected_module = tk.StringVar()
        self.selected_query = tk.StringVar()
        self.param_entries = {}

        ttk.Label(frame, text="Recon Module").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.module_dropdown = ttk.Combobox(frame, textvariable=self.selected_module, values=list(MODULES.keys()), state="readonly")
        self.module_dropdown.grid(row=0, column=1, padx=10, pady=5)
        self.module_dropdown.bind("<<ComboboxSelected>>", self.on_module_change)

        ttk.Label(frame, text="Query Template").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.query_dropdown = ttk.Combobox(frame, textvariable=self.selected_query, state="readonly")
        self.query_dropdown.grid(row=1, column=1, padx=10, pady=5)
        self.query_dropdown.bind("<<ComboboxSelected>>", self.on_query_change)

        self.params_frame = ttk.LabelFrame(frame, text="Parameters")
        self.params_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        ttk.Label(frame, text="Final Query").grid(row=3, column=0, sticky="nw", padx=10, pady=5)
        self.output_text = tk.Text(frame, height=4, width=60)
        self.output_text.grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(frame, text="Build Query", command=self.build_query).grid(row=4, column=1, sticky="e", padx=10, pady=10)

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
        needed_params = re.findall(r"{(.*?)}", template)

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

    # ---------------- Field-Based Query Composer ----------------
    def build_field_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Field Composer")

        self.selected_field = tk.StringVar()
        self.condition_value = tk.StringVar()

        # Field dropdown
        ttk.Label(frame, text="Field").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.field_dropdown = ttk.Combobox(frame, textvariable=self.selected_field, values=list(self.fields.keys()), state="readonly", width=40)
        self.field_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Value entry
        ttk.Label(frame, text="Value").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.value_entry = ttk.Entry(frame, textvariable=self.condition_value, width=42)
        self.value_entry.grid(row=1, column=1, padx=10, pady=5)

        # Add condition
        ttk.Button(frame, text="Add Condition", command=self.add_condition).grid(row=2, column=1, sticky="e", padx=10, pady=5)

        # Preview box
        ttk.Label(frame, text="Final Query").grid(row=3, column=0, sticky="nw", padx=10, pady=5)
        self.composer_output = tk.Text(frame, height=6, width=60)
        self.composer_output.grid(row=3, column=1, padx=10, pady=5)

    def add_condition(self):
        field = self.selected_field.get()
        value = self.condition_value.get()
        if not field or not value:
            return
        quoted = f'"{value}"' if self.fields[field]["type"] == "string" else value
        clause = f"{field}: {quoted}"
        self.conditions.append(clause)

        # Build final string
        query = " AND ".join(self.conditions)
        self.composer_output.delete("1.0", tk.END)
        self.composer_output.insert(tk.END, query)
        self.condition_value.set("")

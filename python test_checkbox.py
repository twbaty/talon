import tkinter as tk

# Simulate whether a key exists
def config_has_api_key():
    # Toggle this between True/False to test
    return False   # change to True to simulate having a key

def launch_test_gui():
    root = tk.Tk()
    root.title("Checkbox Test")

    ignore_key_var = tk.BooleanVar(value=False)
    api_key_checkbox = tk.Checkbutton(root, text="", variable=ignore_key_var)
    api_key_checkbox.grid(row=0, column=0, padx=10, pady=10)

    if not config_has_api_key():  # No key exists → force ignore mode
        ignore_key_var.set(True)
        api_key_checkbox.config(state="disabled", text="Fallback mode: manual query")
        print("DEBUG: config_has_api_key() = False")
        print("DEBUG: Checkbox label =", api_key_checkbox.cget("text"))
    else:
        ignore_key_var.set(False)
        api_key_checkbox.config(state="normal", text="Ignore API Key")
        print("DEBUG: config_has_api_key() = True")
        print("DEBUG: Checkbox label =", api_key_checkbox.cget("text"))

    root.mainloop()

if __name__ == "__main__":
    launch_test_gui()

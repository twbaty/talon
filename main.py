# main.py
from gui.main_window import launch_gui
import os
from dotenv import load_dotenv
load_dotenv()
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

if __name__ == "__main__":
    launch_gui()

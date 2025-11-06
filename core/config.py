# core/config.py
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = Path(__file__).parent / "config.json"

def get_api_key():
    # Priority: environment → .env → config.json
    key = os.getenv("ABUSEIPDB_API_KEY")
    if key:
        return key.strip()

    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
            return (data.get("api_key") or "").strip()
        except Exception:
            return ""

    return ""

def config_has_api_key():
    return bool(get_api_key())

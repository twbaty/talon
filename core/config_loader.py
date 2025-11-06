import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def load_api_key():
    # Try to load from environment variable first
    key = os.environ.get("TALON_API_KEY")
    if key:
        return key

    # Then try config.json
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                data = json.load(f)
            return data.get('api_key')
        except Exception as e:
            print(f"Failed to load API key from config: {e}")

    return None


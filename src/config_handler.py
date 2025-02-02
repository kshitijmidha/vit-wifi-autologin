import json
import os

CONFIG_PATH = r"C:\VIT_WiFi_AutoLogin\config.json"

def load_config():
    """Load configuration from JSON file."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_config(user_id, password, wifi_ssid, display_name):
    """Save configuration to JSON file."""
    config = {
        "userId": user_id,
        "password": password,
        "wifi_ssid": wifi_ssid,
        "display_name": display_name,
        "login_url": "http://phc.prontonetworks.com/cgi-bin/authlogin",
        "downtime_start": 0.3333,  # 12:20 AM
        "downtime_end": 4.5833,    # 4:35 AM
    }
    
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

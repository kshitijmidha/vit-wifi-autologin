import os
from config_handler import save_config

def main():
    print("\nVIT WiFi AutoLogin - User Configuration")
    print("=====================================")
    
    # Get user inputs
    display_name = input("\nEnter your name: ").strip()
    user_id = input("Enter your VIT WiFi username (e.g., 21BCEXXXX): ").strip()
    password = input("Enter your VIT WiFi password: ").strip()
    wifi_ssid = input("Enter your hostel WiFi name (e.g., R-VIT): ").strip()
    
    # Save configuration
    save_config(user_id, password, wifi_ssid, display_name)
    
    print("\nConfiguration saved successfully!")

if __name__ == "__main__":
    main()

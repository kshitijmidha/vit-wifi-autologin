import requests
import time
import socket
import subprocess
import platform
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import psutil
from plyer import notification
import pytz
import webbrowser
import sys
from config_handler import load_config

# Load configuration
config = load_config()
if not config:
    print("Configuration not found. Please run setup.bat first.")
    sys.exit(1)

# Configuration
COLLEGE_WIFI = config['wifi_ssid']
LOGIN_URL = config['login_url']
DOWNTIME_START = config['downtime_start']
DOWNTIME_END = config['downtime_end']

# Form data for login
FORM_DATA = {
    "userId": config['userId'],
    "password": config['password'],
    "serviceName": "ProntoAuthentication",
    "Submit22": "Login",
    "URI": "http://captive.apple.com/hotspot-detect.html"
}

# Headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://captive.apple.com/hotspot-detect.html"
}

# Text file path to store logs
TEXT_FILE = "C:\\VIT_WiFi_AutoLogin\\wifi_login.txt"

# Function to write log entries
def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    # Write to file with UTF-8 encoding
    with open(TEXT_FILE, "a", encoding="utf-8") as txt_file:
        txt_file.write(log_entry)

    # Update GUI
    update_gui(log_entry)

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="VIT WiFi Assistant"
    )

def get_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return f"Good Morning, {config['display_name']}!"
    elif 12 <= current_hour < 17:
        return f"Good Afternoon, {config['display_name']}!"
    elif 17 <= current_hour < 23:
        return f"Good Evening, {config['display_name']}!"
    else:
        return f"🌌 Good Night, {config['display_name']}!"

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def get_wifi_ssid():
    os_type = platform.system()
    try:
        if os_type == "Windows":
            output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
            for line in output.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()
        elif os_type == "Linux":
            return subprocess.check_output("iwgetid -r", shell=True).decode().strip()
        elif os_type == "Darwin":  # macOS
            output = subprocess.check_output(
                "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I",
                shell=True).decode()
            for line in output.split("\n"):
                if "SSID" in line:
                    return line.split(":")[1].strip()
    except Exception as e:
        write_log(f"Error getting WiFi SSID: {e}")
    return None

def login():
    response = requests.post(LOGIN_URL, data=FORM_DATA, headers=HEADERS)
    if response.status_code == 200:
        write_log("✅ Login successful!")
        show_notification("Login Successful", f"You're now logged in to {COLLEGE_WIFI}.")
    else:
        write_log(f"❌ Login failed with status code: {response.status_code}")
        show_notification("Login Failed", "Failed to connect. Please retry or manually log in.")

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return f"Battery: {battery.percent}%"
    else:
        return "Battery info not available"

def get_wifi_signal_strength():
    os_type = platform.system()
    if os_type == "Windows":
        result = subprocess.check_output('netsh wlan show interfaces', shell=True).decode()
        for line in result.splitlines():
            if "Signal" in line:
                signal_strength = line.split(":")[1].strip()
                return f"WiFi Signal Strength: {signal_strength}"
    return "WiFi Signal Strength not available"

def run_speed_test():
    write_log("Opening fast.com in your browser for speed testing...")
    webbrowser.open("https://fast.com")
    show_notification("Speed Test", "fast.com has been opened in your browser.")

def update_system_info():
    battery_info = get_battery_info()
    wifi_info = get_wifi_signal_strength()
    system_info = f"{battery_info} | {wifi_info}"
    system_info_label.config(text=system_info)
    root.after(60000, update_system_info)

def update_gui(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message)
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)

def clear_log():
    confirm = messagebox.askyesno("Clear Log", "Are you sure you want to clear the log?")
    if confirm:
        log_text.config(state=tk.NORMAL)
        log_text.delete(1.0, tk.END)
        log_text.config(state=tk.DISABLED)
        write_log("🗑️ Log cleared by user.")

def is_downtime():
    tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(tz)
    current_hour = current_time.hour + current_time.minute / 60
    write_log(f"Current time in IST: {current_time.strftime('%H:%M:%S')}")
    return (current_hour >= DOWNTIME_START and current_hour <= DOWNTIME_END)

def monitor_network_changes():
    write_log("🔗 Starting network change monitoring...")
    previous_network = get_wifi_ssid()
    
    while True:
        current_network = get_wifi_ssid()
        
        if current_network != previous_network:
            write_log(f"🔗 Network changed to {current_network}")
            previous_network = current_network
            
            if current_network == COLLEGE_WIFI:
                if not is_connected() and not is_downtime():
                    write_log(f"⚠️ No internet detected on {COLLEGE_WIFI}. Attempting login...")
                    login()
                elif is_downtime():
                    write_log("⚠️ WiFi is intentionally offline. Skipping login attempt.")
                    show_notification("WiFi Status", "WiFi is offline between 12:20 AM and 4:35 AM IST. Please retry later.")
                else:
                    write_log(f"✅ Internet is working on {COLLEGE_WIFI}. No login required.")
                    show_notification("WiFi Status", f"Internet is working, and you're connected to {COLLEGE_WIFI}!")
        
        time.sleep(10)

def auto_login_loop():
    global login_successful
    write_log("🔗 Starting WiFi monitoring...")
    login_successful = False
    
    while True:
        current_wifi = get_wifi_ssid()

        if current_wifi == COLLEGE_WIFI:
            if is_connected():
                write_log(f"✅ Internet is working on {COLLEGE_WIFI}. No login required.")
                show_notification("WiFi Status", f"Internet is working, and you're connected to {COLLEGE_WIFI}!")
                login_successful = True
            elif not is_downtime() and not login_successful:
                write_log(f"⚠️ No internet detected on {COLLEGE_WIFI}. Attempting login...")
                login()
            elif is_downtime():
                write_log("⚠️ WiFi is intentionally offline. Skipping login attempt.")
                show_notification("WiFi Status", "WiFi is offline between 12:20 AM and 4:35 AM IST. Please retry later.")
        else:
            login_successful = False

        time.sleep(300)

# GUI Setup
root = tk.Tk()
root.geometry("500x400")
root.configure(bg="#2C2F33")
root.title("VIT WiFi Assistant")

# Display greeting
greeting_label = tk.Label(root, text=get_greeting(), font=("Arial", 14, "bold"), fg="white", bg="#2C2F33")
greeting_label.pack(pady=5)

# System Info Label
system_info_label = tk.Label(root, text="", font=("Arial", 10), fg="white", bg="#2C2F33")
system_info_label.pack(pady=5)

# Log Display
log_text = tk.Text(
    root, width=60, height=15, font=("Consolas", 10),
    bg="#23272A", fg="#00FF00", state=tk.DISABLED,
    wrap=tk.WORD, borderwidth=0, highlightthickness=0
)
log_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Button Frame
button_frame = tk.Frame(root, bg="#2C2F33")
button_frame.pack(pady=10)

# Force Login Button
login_button = tk.Button(
    button_frame, text="🔄 Force Login", font=("Arial", 12, "bold"),
    bg="#7289DA", fg="white", relief="flat", command=login
)
login_button.pack(side=tk.LEFT, padx=5)

# Clear Log Button
clear_button = tk.Button(
    button_frame, text="🧹 Clear Log", font=("Arial", 12, "bold"),
    bg="#FF5555", fg="white", relief="flat", command=clear_log
)
clear_button.pack(side=tk.LEFT, padx=5)

# Speed Test Button
speed_test_button = tk.Button(
    button_frame, text="🛜 Speed Test", font=("Arial", 12, "bold"),
    bg="#4CAF50", fg="white", relief="flat", command=run_speed_test
)
speed_test_button.pack(side=tk.LEFT, padx=5)

# Start updating system info
update_system_info()

# Run auto-login in a separate thread
auto_login_thread = Thread(target=auto_login_loop, daemon=True)
auto_login_thread.start()

# Run network monitoring in a separate thread
network_monitor_thread = Thread(target=monitor_network_changes, daemon=True)
network_monitor_thread.start()

# Auto-minimize window on startup
root.iconify()

# Start the GUI
root.mainloop()

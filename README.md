# VIT WiFi AutoLogin

An automated WiFi login system for VIT hostels that handles authentication automatically when connected to hostel WiFi networks.

## Features

- 🚀 Automatic login when connected to hostel WiFi
- 🔔 Desktop notifications for connection status
- 📊 Battery and WiFi signal strength monitoring
- 🕒 Handles college WiFi downtime (12:20 AM to 4:35 AM)
- 🔄 Auto-starts with Windows
- 📱 Minimalist GUI with dark mode

## Installation

1. Download and extract the latest release
2. Run `setup.bat` as administrator
3. Enter your details when prompted:
   - Your name
   - VIT username (e.g., 21BCE0012)
   - VIT password
   - Hostel WiFi name (e.g., R-VIT)

The application will start automatically on system startup.

## Requirements

- Windows 10 or later
- Python 3.8 or later
- Internet connection for initial setup

## Project Structure

```
C:\VIT_WiFi_AutoLogin\
├── auto_login.py          # Main application
├── config_handler.py      # Configuration manager
├── auto_login.bat         # Background runner
├── auto_login.vbs         # Startup script
├── config.json           # User configuration
└── wifi_login.txt        # Log file
```

# Security Information

## Windows Security Warnings

When running the setup or the application, you may encounter Windows Security warnings. This is normal because:

1. The scripts are not digitally signed (this would require a paid certificate)
2. The application needs administrative privileges to:
   - Create a folder in C: drive
   - Add itself to Windows startup
   - Monitor and manage WiFi connections

## Is it safe?

✅ **Yes, the application is safe.** Here's why:

- All code is open source and available for inspection
- No data is collected or transmitted except for VIT login credentials
- Credentials are stored locally on your PC only
- The code only interacts with VIT's login portal
- You can review all files in the GitHub repository

## To safely run the application:

1. When you see "Windows protected your PC":

   - Click "More info"
   - Click "Run anyway"

2. When you see "User Account Control":
   - Click "Yes" to allow the program to run

## For extra security:

1. Review the source code on GitHub before installing
2. Check the installation files in `C:\VIT_WiFi_AutoLogin\`
3. Monitor the log file at `C:\VIT_WiFi_AutoLogin\wifi_login.txt`
4. Use Windows Task Manager to verify `pythonw.exe` is running

## Still concerned?

1. The application can be easily uninstalled:
   - Delete the `C:\VIT_WiFi_AutoLogin` folder
   - Remove `auto_login.vbs` from Windows startup folder
   - No other system changes are made

## Support

For issues and feature requests, please create an issue on GitHub.

## License

MIT License - feel free to modify and share!

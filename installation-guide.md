# Installation Guide

1. **Prerequisites**
   - Make sure you have Python installed (3.8 or later)
   - Download the latest release from GitHub

2. **Initial Setup**
   - Extract the downloaded ZIP file
   - Right-click `setup.bat` and select "Run as administrator"
   - Follow the prompts to enter your:
     - Name (for personalized greetings)
     - VIT username
     - VIT password
     - Hostel WiFi name (e.g., R-VIT, S-VIT)

3. **Verification**
   - The application will be installed to `C:\VIT_WiFi_AutoLogin\`
   - A minimized window should appear in your taskbar
   - The application will start automatically on next system startup

4. **Troubleshooting**
   - If the application doesn't start, run `C:\VIT_WiFi_AutoLogin\auto_login.bat`
   - Check `wifi_login.txt` for any error messages
   - Make sure your WiFi is enabled and you're in range of the hostel WiFi

5. **Dependencies**
   If you face any issues, manually install the required packages:
   ```
   pip install -r requirements.txt
   ```

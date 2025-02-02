@echo off
title VIT WiFi AutoLogin Setup
color 0A

:: Change to the script's directory
cd /d "%~dp0"

echo ================================================
echo              VIT WiFi AutoLogin Setup
echo ================================================
echo.
echo IMPORTANT: You may see a Windows Security warning.
echo This is normal because the script needs to:
echo  1. Create a folder in C: drive
echo  2. Add a startup entry for auto-login
echo  3. Run Python in background mode
echo.
echo All code is open source and available at:
echo https://github.com/kshitijmidha/vit-wifi-autologin
echo.
echo Press any key to continue...
pause >nul

:: Request Admin privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: Create installation directory
set INSTALL_DIR=C:\VIT_WiFi_AutoLogin
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy all required files
echo Installing files...
if not exist "src\auto_login.py" (
    echo Error: Required files not found!
    echo Please make sure you're running setup.bat from the extracted folder.
    echo Expected folder structure:
    echo VIT_WiFi_AutoLogin\
    echo ├── src\
    echo │   ├── auto_login.py
    echo │   ├── auto_login.bat
    echo │   ├── auto_login.vbs
    echo │   ├── config_handler.py
    echo │   ├── setup_wizard.py
    echo │   └── requirements.txt
    echo └── setup.bat
    echo └── readme.md
    echo └── installation-guide.md
    pause
    exit /B 1
)

xcopy /Y "src\auto_login.py" "%INSTALL_DIR%\" >nul
xcopy /Y "src\config_handler.py" "%INSTALL_DIR%\" >nul
xcopy /Y "src\auto_login.bat" "%INSTALL_DIR%\" >nul
xcopy /Y "src\auto_login.vbs" "%INSTALL_DIR%\" >nul

:: Install required packages
echo Installing required packages...
pip install -r "src\requirements.txt" >nul 2>&1

:: Run Python script to get user credentials
python "src\setup_wizard.py"

:: Add to startup silently
echo Adding to startup...
mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup" 2>nul
copy /Y "%INSTALL_DIR%\auto_login.vbs" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\" >nul

echo.
echo Setup completed successfully!
echo The application will start automatically on system startup.
echo.
echo Would you like to start the application now? (Y/N)
choice /C YN /N
if errorlevel 2 goto end
start "" "%INSTALL_DIR%\auto_login.vbs"
:end
echo.
echo You can always run it manually from: %INSTALL_DIR%
echo.
pause
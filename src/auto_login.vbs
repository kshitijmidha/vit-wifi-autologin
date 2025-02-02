On Error Resume Next
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\VIT_WiFi_AutoLogin\auto_login.bat""", 0, False
Set WshShell = Nothing
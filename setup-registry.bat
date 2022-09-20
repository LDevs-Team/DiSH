mkdir %appdata%\DiSH
copy DiSH.exe %appdata%\DiSH
copy .env %appdata%\DiSH
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run\ /V "DiSH" /t REG_SZ /F /D "%appdata%\DiSH\DiSH.exe"
echo starting...
start %appdata%\DiSH\DiSH.exe
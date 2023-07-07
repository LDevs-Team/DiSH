mkdir %appdata%\LDevs\DiSH
copy DiSH.exe %appdata%\LDevs\DiSH
copy .env %appdata%\LDevs\DiSH
copy cz.yaml %appdata%\LDevs\DiSH
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run\ /V "DiSH" /t REG_SZ /F /D "%appdata%\DiSH\DiSH.exe"
echo starting...
start %appdata%\LDevs\DiSH\DiSH.exe

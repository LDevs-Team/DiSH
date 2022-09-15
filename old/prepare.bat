@echo off
pip install -r requirements.txt
mkdir %appdata%\DiSH
copy executor.exe %appdata%\DiSH
copy main.py %appdata%\DiSH
pip install -r requirements.txt
mkdir %appdata%\DiSH
copy DiSH.exe %appdata%\DiSH
copy main.py %appdata%\DiSH
copy .env %appdata%\DiSH
copy DiSH.exe "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\DiSH.exe"
echo starting...
start %appdata%\DiSH\executor.exe
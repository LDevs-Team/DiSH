pip install -r requirements.txt
mkdir %appdata%\DiSH
copy DiSH.exe %appdata%\DiSH
copy main.py %appdata%\DiSH
mklink "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\DiSH.exe" %appdata%\DiSH\DiSH.exe

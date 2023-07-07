pip install -r requirements.txt
mkdir %appdata%\LDevs\DiSH
copy DiSH.exe %appdata%\LDevs\DiSH
copy main.py %appdata%\LDevs\DiSH
mklink "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\DiSH.exe" %appdata%\DiSH\DiSH.exe

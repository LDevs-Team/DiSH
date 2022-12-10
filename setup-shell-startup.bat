mkdir %appdata%\DiSH
copy DiSH.exe %appdata%\DiSH
copy .env %appdata%\DiSH
copy cz.yaml %appdata%\DiSH
copy DiSH.exe "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\DiSH.exe"
echo starting...
start %appdata%\DiSH\DiSH.exe
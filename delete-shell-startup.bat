taskkill /f /im DiSH.exe
cd %appdata%
powershell -c  "rm DiSH"
cd %appdata%\Microsoft\Windows\Start Menu\Programs\Startup
del DiSH.exe
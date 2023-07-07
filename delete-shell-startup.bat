taskkill /f /im DiSH.exe
cd %appdata%
cd ldevs
cd dish
del dish.exe
del .env
del cz.yaml
cd ..
del /s /q DiSH
cd %appdata%\Microsoft\Windows\Start Menu\Programs\Startup
del DiSH.exe

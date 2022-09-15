mkdir $env:localappdata\PyShell\
Copy-Item .\executor.exe $env:localappdata\PyShell\dish.exe
Copy-Item .\nssm.exe $env:localappdata\PyShell\
Copy-Item .\main.py $env:localappdata\PyShell\
Set-Location $env:localappdata\PyShell 
.\nssm.exe install DiSH "${env:localappdata}\PyShell\dish.exe"
Start-Service -Name DiSH
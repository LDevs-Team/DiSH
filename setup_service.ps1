mkdir $env:appdata\DiSH\
$currentDir = $(Get-Location)
Copy-Item .\DiSH.exe $env:appdata\DiSH\dish.exe
Copy-Item .\nssm.exe $env:appdata\DiSH\
Copy-Item .\main.py $env:appdata\DiSH\
Set-Location $env:appdata\DiSH 
.\nssm.exe install DiSH "${env:appdata}\DiSH\dish.exe"
Start-Service -Name DiSH
Set-Location $currentDir
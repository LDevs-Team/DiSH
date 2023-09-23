mkdir %appdata%\ldevs\dishloader\versions\nightly
copy * %appdata%\ldevs\dishloader\versions\nightly
reg add HKCU\SOFTWARE\LDevs\DiSHLoader /v DefaultVersion /t REG_SZ /d nightly /f

import os, zipfile, shutil
import webbrowser
import setup
import subprocess
ver=setup.__version__
print("Packaging with pyinstaller")
exitcode = subprocess.run("pyinstaller --name DiSH --onefile --windowed main.py --add-data main.py;. --add-data .env;.")

print("Moving files")

shutil.move("dist/DiSH.exe", "DiSH.exe")
print("Creating zip")
with zipfile.ZipFile("../../builds/DiSH/DiSHv{}.zip".format(ver), "w", zipfile.ZIP_DEFLATED) as zip:
    zip.write("DiSH.exe")
    zip.write("main.py")
    zip.write("setup-registry.bat")
    zip.write("setup-shell-startup.bat")
    zip.write(".env")

print("Cleaning up")
shutil.rmtree("build")
shutil.rmtree("dist")
shutil.move("DiSH.exe", "../../builds/DiSH/DiSHv{}.exe".format(ver))

try:
    os.remove("DiSH.spec")
    os.remove("main.spec")
except:
    pass
print("Opening browser for upload")
webbrowser.open("https://app.mediafire.com/myfiles")

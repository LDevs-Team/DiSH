import os, zipfile, shutil
import webbrowser
import setup, glob, platform
ver=setup.__version__
print("Packaging with pyinstaller")
exitcode = os.system("pyinstaller --name DiSH --onefile --windowed main.py")

print("Moving files")

g = glob.glob("dist/DiSH*")

print("Creating zip")
with zipfile.ZipFile("dist/DiSHv{}-{}.zip".format(ver, platform.system()), "w", zipfile.ZIP_DEFLATED) as zip:
    zip.write()
    zip.write("main.py")
    zip.write("setup-registry.bat")
    zip.write("setup-shell-startup.bat")
    for a in g:
        zip.write(a)


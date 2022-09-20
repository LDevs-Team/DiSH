import os, zipfile, shutil
import webbrowser, platform
import setup, glob, yaml
with open("cz.yaml", "r") as stream:
    try:
        ver = yaml.safe_load(stream)['commitizen']['version']
    except yaml.YAMLError as exc:
        print(exc)

print("Packaging with pyinstaller")
exitcode = os.system("pyinstaller --name DiSH --onefile --windowed main.py")

print("Moving files")

g = glob.glob("dist/DiSH*")
print(g)
print("Creating zip")
with zipfile.ZipFile("dist/DiSH-{}.zip".format(platform.system()), "w", zipfile.ZIP_DEFLATED) as zip:
    zip.write("main.py")
    zip.write("setup-registry.bat")
    zip.write("setup-shell-startup.bat")
    for a in g:
        zip.write(a)


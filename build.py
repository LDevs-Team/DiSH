import os, zipfile
import platform, shutil
import glob, yaml
with open("cz.yaml", "r") as stream:
    try:
        ver = yaml.safe_load(stream)['commitizen']['version']
    except yaml.YAMLError as exc:
        print(exc)

print("Packaging with pyinstaller")
exitcode = os.system("pyinstaller --name DiSH --onefile --windowed main.py")


g = glob.glob("dist/DiSH*")
print(g)
for a in g:
    shutil.move(a, ".")
print("Creating zip")
with zipfile.ZipFile("DiSH-{}.zip".format(platform.system()), "w", zipfile.ZIP_DEFLATED) as zip:
    zip.write("main.py")
    zip.write("setup-registry.bat")
    zip.write("setup-shell-startup.bat")
    zip.write("requirements.txt")
    g = glob.glob("DiSH*")
    for a in g:
        zip.write(a)
    zip.write("cz.yaml")

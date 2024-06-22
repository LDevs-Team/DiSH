import os, zipfile
import platform, shutil
import glob, yaml
with open("cz.yaml", "r") as stream:
    try:
        ver = yaml.safe_load(stream)['commitizen']['version']
    except yaml.YAMLError as exc:
        print(exc)

print("Packaging with pyinstaller")
os.chdir("src")
exitcode = os.system("pyinstaller --name DiSH --onefile --windowed main.py")


g = glob.glob("dist/DiSH*")
print(g)
for a in g:
    shutil.move(a, ".")
print("Creating zip")
g = glob.glob("DiSH*")
with zipfile.ZipFile("DiSH-{}.zip".format(platform.system()), "w", zipfile.ZIP_DEFLATED) as zip:
    for a in g:
        zip.write(a)
    zip.write("main.py")
    zip.write("../setup.bat", "setup.bat")
    zip.write("../README.md", "README.md")
    zip.write("../LICENSE", "LICENSE")
    zip.write("../CHANGELOG.md", "CHANGELOG.md")

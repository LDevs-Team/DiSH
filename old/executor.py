import os
import sys

if "--schtask" in sys.argv:
    os.popen(os.environ["appdata"]+"/DiSH/main.py")
letame = os.popen("python main.py")
open("log.log", "w").write(letame)
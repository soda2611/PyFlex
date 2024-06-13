import subprocess
from build_20240612132530L import __active__

with open("build_20240612132530L.py", encoding="utf-8") as f: startup=f.read()

if input("Enable customized shell (y/n): ").replace(" ", "").lower=="y": customized_shell=True
else: customized_shell=False

def active(customized_shell=False):
	if customized_shell: subprocess.Popen(['python', '-i', '-c', f'{startup[:startup.find("if __name__")]}\ncls()'], text=True)
	else: __active__("cls()")

active(customized_shell)
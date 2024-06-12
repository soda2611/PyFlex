import traceback, platform, os, sys
from math import *

python_version = platform.python_version()
python_build = platform.python_build()
__version__="1.1.1dev"
__build__="20240402192802L"
__platform__=platform.system()

print(f"PyFlex - Version: {__version__} - Build: {__build__}\n")
print("Python", python_version, python_build)
print('Type "help", "copyright", "credits" or "license" for more information.')

del platform

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 
__new_line__=False
__nnum__=1
__history__=[]
inp=""

def cls():
	if __platform__=="Windows":
		os.system("cls")
	else:
		os.system("clear")
	print(f"PyFlex - Version: {__version__} - Build: {__build__}\n")
	print("Python", python_version, python_build)
	print('Type "help", "copyright", "credits" or "license" for more information.')
	
def log(index=-1):
	global __history__
	try:
		inp=__history__[index].split("\n")
		print(f">>> {inp[0]}")
		for i in inp[1:]:
			print(f"... {i}")
		__run__("\n".join(inp))
	except Exception as ex:
		print("No commands in history")
	try:
		__history__=__history__[:index]
	except:
		__history__=[]
		
def logs():
	for i in range(len(__history__)):
		print(i, __history__[i])

def run(file_path):
	os.system(f"python '{file_path}'")
	
def install(lib):
	os.system(f"pip install {lib}")
	
def upgrade(lib):
	install("--upgrade "+lib)

def __coding_environment__(end_signal="main.run()"):
	global __new_line__, __nnum__, CURSOR_UP_ONE, ERASE_LINE
	inp=""
	while end_signal not in inp:
		if __new_line__:
			inp+="\n"+__nnum__*"    "+input(__nnum__*"    ")
			if inp.replace("  ","")[-1]=="\n":
				if __nnum__==1:
					__new_line__=not __new_line__
				sys.stdout.write(CURSOR_UP_ONE) 
				sys.stdout.write(ERASE_LINE) 
				__nnum__-=1
			if inp.replace("  ","")[-1]==":":
				__nnum__+=1
			continue
		else:
			inp+="\n"+input()
			if inp[-1]==" ": inp=inp[:-1]
			if inp[-1]==":":
				__new_line__=not __new_line__
				continue
	print("\nOutput:")
	__run__(inp[:inp.find(end_signal)])
	__nnum__=1
	print("[Program finished]")

def __run__(inp):
	try:
		print(eval(inp[:-1]))
	except:
		exec(inp)

while True:
	try:
		if __new_line__:
			inp+="\n"+__nnum__*"    "+input("..."+__nnum__*"    ")
			if inp.replace("  ","")[-1]=="\n":
				if __nnum__==1:
					__new_line__=not __new_line__
					__run__(inp)
					__history__.append(inp)
					inp=""
				sys.stdout.write(CURSOR_UP_ONE) 
				sys.stdout.write(ERASE_LINE) 
				__nnum__-=1
			if inp.replace("  ","")[-1]==":":
				__nnum__+=1
			continue
		else:
			inp=input(">>> ").replace("  ","")
			if inp[-1]==" ": inp=inp[:-1]
			if inp[-1]==":":
				__new_line__=not __new_line__
				continue
			__run__(inp)
			__history__.append(inp)
			inp=""
	except Exception as ex:
		if inp!="":
			if inp.lower()=="^z":
				break
			traceback.print_exc()
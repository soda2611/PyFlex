import traceback, platform, os, sys, re
from math import *
try: from customized_command import *
except: pass

python_version = platform.python_version()
python_build = platform.python_build()
__version__="1.1.1dev"
__build__="20240611171400L"
__platform__=platform.system()
__info__=f"""
PyFlex - Version: {__version__} - Build: {__build__}
Platform: {__platform__}

Python {python_version} {python_build}
Type "help", "copyright", "credits" or "license" for more information."""[1:]

del platform, python_version, python_build

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 
__activated__=__new_line__=False
__nnum__=1
__history__=[]

def cmd(*args, **kwargs): os.system(*args, **kwargs)

def run(file_path): cmd(f"python '{file_path}'")
	
def install(lib): cmd(f"pip install {lib}")
	
def uninstall(lib): cmd(f"pip uninstall {lib}")
	
def upgrade(lib): install("--upgrade "+lib)

def exit():
	global __activated__
	__activated__=False

def cls(keep_info=True):
	if __platform__=="Windows": cmd("cls")
	else: cmd("clear")
	if keep_info: print(__info__)
	
def log(index=-1):
	global __history__
	try:
		inp=__history__[index].split("\n")
		print(f">>> {inp[0]}")
		for i in inp[1:]: print(f"... {i}")
		__run__("\n".join(inp))
		del __history__[index]
	except: return "No commands in history"
		
def logs():
	print("No commands in history" if len(__history__)==0 else "\n".join(f"{i}: {__history__[i]}" for i in range(len(__history__))))

def __multi_line__(end_signal="main.run()", export_to_file=False):
	global __new_line__, __nnum__, CURSOR_UP_ONE, ERASE_LINE
	inp=""
	line=1
	print(f"Multi-line mode: On\nRun command: {end_signal}")
	if export_to_file: file_name=input("File name: ")
	while end_signal not in inp:
		if __new_line__:
			inp+="\n"+__nnum__*"    "+input(str(line)+"| "+__nnum__*"    ")
			if inp.replace(" ","")[-1]=="\n":
				if __nnum__==1: __new_line__=not __new_line__
				sys.stdout.write(CURSOR_UP_ONE)
				sys.stdout.write(ERASE_LINE)
				__nnum__-=1
				continue
			if inp.replace(" ","")[-1]==":": __nnum__+=1
			line+=1
		else:
			inp+="\n"+input(str(line)+"| ")
			if inp[-1]==" ": inp=inp[:-1]
			if inp[-1]==":":
				__new_line__=not __new_line__
				line+=1
				continue
			line+=1
	if export_to_file:
		with open(f"saved_scripts/{file_name}.py", "w", encoding="utf-8") as fo: fo.write(inp[1:inp.find(end_signal)])
		print(f"\nScript saved at: {os.getcwd()}/saved_scripts/{file_name}.py")
	print("\nOutput:")
	__run__(inp[1:inp.find(end_signal)])
	__nnum__=1
	print(f"[Program finished]")
	
def __test__(inp):
	try: __run__(inp, False)
	except: return False
	else: return True
		
def __run__(inp, display=True):
	global_var=globals()
	count=0
	lst=re.findall(r"([\"'])(.*?)\1", inp)
	for i in lst: count+=i.count(":")
	if not inp.count(":")>count:
		try:
			out=eval(inp, global_var)
			if (out!=None) and display: print(out)
		except: exec(inp, global_var)
	else: exec(inp, global_var)
	__history__.append(inp)
	
def create_customized_command(end_signal="main.run()"):
	global __new_line__, __nnum__, CURSOR_UP_ONE, ERASE_LINE
	__new_line__=True
	overwrite=False
	line=1
	print(f"Run command: {end_signal}")
	command_name=input("Command name: ")
	args=input("Arguments for command (split by \",\"; if no leave this blank): ").replace(" ","").split(",")
	inp=f"def {command_name}({', '.join(args)}):"
	while end_signal not in inp:
		if __new_line__:
			inp+="\n"+__nnum__*"    "+input(str(line)+"| "+(__nnum__-1)*"    ")
			if inp.replace(" ","")[-1]=="\n":
				if not __nnum__>1: __new_line__=not __new_line__
				sys.stdout.write(CURSOR_UP_ONE)
				sys.stdout.write(ERASE_LINE) 
				__nnum__-=1
				continue
			if (inp.replace(" ","")[-1]==":" and auto_tab): __nnum__+=1
			line+=1
		else:
			inp+="\n"+input(str(line)+"| ")
			if inp[-1]==" ": inp=inp[:-1]
			if inp[-1]==":":
				__new_line__=not __new_line__
				line+=1
				continue
			line+=1
	try:
		print("\nTesting...")
		exist=__test__(command_name)
		if exist:
			in_=input("Existing command! Do you want to overwrite? (y/n):").replace(" ","").lower()
			if in_=="y": overwrite=True
		if overwrite or not exist: __run__(inp[:inp.find(end_signal)])
	except:
		print("Cannot create command\nErrors:")
		traceback.print_exc()
	else:
		if overwrite:
			with open(f"customized_command.py", "r", encoding="utf-8") as fi:
				commands=fi.read()
				commands=commands.replace(commands[commands.find(f"def {command_name}"):commands.find("\ndef")+1], inp[:inp.find(__nnum__*"    "+end_signal)]+"\n")
			with open(f"customized_command.py", "w", encoding="utf-8") as fo: fo.write(commands)
		elif not exist:
			with open(f"customized_command.py", "a", encoding="utf-8") as fo: fo.write(inp[:inp.find(__nnum__*"    "+end_signal)]+"\n")
		print(f"[Process finished]")
	__nnum__=1
	__new_line__=False

def active(auto_tab=True):
	global __nnum__, __new_line__, __history__, __activated__
	
	if __activated__:
		print("PyFlex has already been activated")
		return
	else: __activated__= not __activated__
	
	inp=""
	if not auto_tab: __nnum__=0
	print(__info__)

	while __activated__:
		try:
			if __new_line__:
				inp+="\n"+__nnum__*"    "+input("... "+__nnum__*"    ")
				if inp.replace(" ","")[-1]=="\n":
					if __nnum__==1:
						__new_line__=not __new_line__
						__run__(inp)
						inp=""
					sys.stdout.write(CURSOR_UP_ONE) 
					sys.stdout.write(ERASE_LINE) 
					__nnum__-=1
				elif inp.replace(" ","")[-1]==":": __nnum__+=1
			else:
				inp=input(">>> ")
				if inp.replace(" ","")[-1]==":":
					__new_line__=not __new_line__
					continue
				if inp.replace(" ","").lower()=="^z": inp="exit()"
				__run__(inp)
		except: traceback.print_exc()
			
if __name__=="__main__":
	active()
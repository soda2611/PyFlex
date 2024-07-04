import traceback, platform, os, sys, re
from math import *
try: from customized_command import *
except: pass

python_version, python_build = [platform.python_version(), platform.python_build()]
__version__="1.1.1dev"
__build__="20240614223100L"
__platform__=platform.system()
__info__=f"""PyFlex - Version: {__version__} - Build: {__build__}\nPlatform: {__platform__}\n\nPython {python_version} {python_build}\nType "help", "copyright", "credits" or "license" for more information."""

del platform, python_version, python_build

ERASE_LINE = '\x1b[1A\x1b[2K' 
__activated__=__new_line__=False
__nnum__=1
__history__=[]

def cmd(*args, **kwargs): os.system(*args, **kwargs)

def run(file_path): cmd(f"python '{file_path}'")
	
def install(lib): cmd(f"pip install {lib}")
	
def uninstall(lib): cmd(f"pip uninstall {lib}")
	
def upgrade(lib): install(f"--upgrade {lib}")

def cls(): cmd("cls") if __platform__=="Windows" else cmd("clear")
		
def logs(): return "No commands in history" if len(__history__)==0 else "\n".join(f"{i}: {__history__[i]}" for i in range(len(__history__)))

def exit():
	global __activated__
	__activated__=False
	
def log(index=-1):
	if len(__history__)!=0:
		inp=__history__[index].split("\n")
		print(f">>> {inp[0]}")
		for i in inp[1:]: print(f"... {i}")
		__run__("\n".join(inp), False)
		del __history__[index]
	else: return "No commands in history"

def __multi_line__(end_signal="main.run()", export_to_file=False):
	global __new_line__, __nnum__, ERASE_LINE
	inp=""
	line=1
	print(f"Multi-line mode: On\nRun command: {end_signal}")
	if export_to_file: file_name=input("File name: ")
	while end_signal not in inp:
		if __new_line__:
			inp+="\n"+__nnum__*"    "+input(str(line)+"| "+__nnum__*"    ")
			if inp.replace(" ","")[-1]=="\n":
				if __nnum__==1: __new_line__=not __new_line__
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
	try: __run__(inp, False, False)
	except: return False
	else: return True
		
def __run__(inp, add_to_history=True, display=True):
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
	if add_to_history:  __history__.append(inp)
	
def create_customized_command(end_signal="main.run()"):
	global __new_line__, __nnum__, ERASE_LINE
	__new_line__=True
	line=1
	print(f"Run command: {end_signal}")
	command_name, args=[input("Command name: "), input("Arguments for command (split by \",\"; if no leave this blank): ").replace(" ","").split(",")]
	inp=f"def {command_name}({', '.join(args)}):"
	while end_signal not in inp:
		if __new_line__:
			inp+="\n"+__nnum__*"    "+input(str(line)+"| "+(__nnum__-1)*"    ")
			if inp.replace(" ","")[-1]=="\n":
				if not __nnum__>1: __new_line__=not __new_line__
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
			overwrite=True if in_=="y" else False
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
	
def __del__(command):
	for i in command.split():
		if i=="__restore_default_elements__": print(f"Cannot delete {i}")
		try: exec(f"del {i}", globals())
		except: print(f"Cannot delete {i}")
		else:
			try:
				with open("customized_command.py", encoding="utf-8") as f: script=f.read()
				block=[script.find(f"def {command}"), script.find("\ndef")]
				if block[1]==-1: open("customized_command.py", "w", encoding="utf-8").close()
				elif block[0]!=-1:
					with open("customized_command.py", "w", encoding="utf-8") as f: f.write(script[:block[0]]+script[block[1]:])
			except: pass

def __restore_default_elements__():
	with open("build_20240614223100L.py", encoding="utf-8") as f: __run__(f.read()[:-1]+"'cls()')")

def __active__(startup_command=False, auto_tab=True):
	global __nnum__, __new_line__, __history__, __activated__
	
	if __activated__: return "PyFlex has already been activated"
	else: __activated__=not __activated__
	
	if startup_command:
		try: __run__(startup_command, False, False)
		except: print("Cannot run startup command")
	
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
					sys.stdout.write(ERASE_LINE)
					__nnum__-=1
				elif inp.replace(" ","")[-1]==":": __nnum__+=1
			else:
				inp=input(">>> ")
				if inp.replace(" ","")!="":
					if inp.replace(" ","")[-1]==":":
						__new_line__=not __new_line__
						continue
					if inp.replace(" ","").lower()=="^z": inp="exit()"
					__run__(inp)
		except: traceback.print_exc()

def __help__(): return "PyFlex Help - Version: 1.1.1dev\nCommands:\n    cmd(*args, **kwargs)              : Run system commands.\n    run(file_path)                    : Run a Python script from a file.\n    install(lib)                      : Install a Python library using pip.\n    uninstall(lib)                    : Uninstall a Python library using pip.\n    upgrade(lib)                      : Upgrade a Python library using pip.\n    cls()                             : Clear the console screen.\n    logs()                            : Show the command history.\n    exit()                            : Exit PyFlex.\n    log(index=-1)                     : Re-run a specific command from history.\n    create_customized_command()       : Create a custom command.\n    __multi_line__(end_signal, export_to_file) : Enter multi-line mode.\n    __del__(command)                  : Delete a custom command.\n    __restore_default_elements__()    : Restore default elements of PyFlex.\n    __active__(startup_command, auto_tab) : Activate PyFlex.\nUsage Examples:\n    - To run a system command:\n        cmd('ls' if __platform__ != 'Windows' else 'dir')\n    - To run a Python script:\n        run('path\to\script.py')\n    - To install a library:\n        install('requests')\n    - To clear the screen:\n        cls()\n    - To see command history:\n        logs()\n    - To exit PyFlex:\n        exit()\n    - To re-run a command from history:\n        log(2)  # Re-run the third command in history\n    - To create a custom command:\n        create_customized_command()\n    - To enter multi-line mode:\n        __multi_line__()\n    - To delete a custom command:\n        __del__('my_custom_command')\n    - To restore default elements:\n        __restore_default_elements__()\n    - To activate PyFlex:\n        __active__()\nFor more detailed information, please refer to the documentation or source code.\n"
			
if __name__=="__main__":
	__active__()
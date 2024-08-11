# Generated and modified with the assistance of AI (ChatGPT by OpenAI)

import traceback, platform, os, sys, re
from math import *
try: from customized_command import *
except: pass

# Metadata
__version__ = "1.1.1dev"
__build__ = "2024081105300L"
__platform__ = platform.system()
python_version, python_build = platform.python_version(), platform.python_build()

__info__ = f"""PyFlex - Version: {__version__} - Build: {__build__}
Platform: {__platform__}

Python {python_version} {python_build}
Type "help", "copyright", "credits" or "license" for more information."""

# Global variables and constants
ERASE_LINE = '\x1b[1A\x1b[2K' 
__activated__ = __new_line__ = False
__nnum__ = 1
__history__ = []

# System command wrapper
def cmd(*args, **kwargs):
    os.system(*args, **kwargs)

# Run a Python script from a file
def run(file_path):
    if os.path.isfile(file_path):
        cmd(f"python '{file_path}'")
    else:
        print(f"Error: File '{file_path}' not found.")

# Install a Python library
def install(lib):
    if lib:
        cmd(f"pip install {lib}")
    else:
        print("Error: Library name not provided.")

# Uninstall a Python library
def uninstall(lib):
    if lib:
        cmd(f"pip uninstall {lib}")
    else:
        print("Error: Library name not provided.")

# Upgrade a Python library
def upgrade(lib):
    if lib:
        install(f"--upgrade {lib}")
    else:
        print("Error: Library name not provided.")

# Clear the console screen
def cls():
    cmd("cls" if __platform__ == "Windows" else "clear")

# Show command history
def logs():
    return "No commands in history" if not __history__ else "\n".join(f"{i}: {__history__[i]}" for i in range(len(__history__)))

# Exit PyFlex
def exit():
    global __activated__
    __activated__ = False
    print("Exiting PyFlex...")

# Re-run a specific command from history
def log(index=-1):
    if __history__:
        try:
            inp = __history__[index].split("\n")
            print(f">>> {inp[0]}")
            for i in inp[1:]:
                print(f"... {i}")
            __run__("\n".join(inp), False)
            del __history__[index]
        except IndexError:
            print("Error: Command index out of range.")
    else:
        print("No commands in history.")

# Multi-line input mode
def __multi_line__(end_signal="main.run()", export_to_file=False):
    global __new_line__, __nnum__, ERASE_LINE
    inp = ""
    line = 1
    print(f"Multi-line mode: On\nRun command: {end_signal}")
    
    if export_to_file:
        file_name = input("File name: ")
        file_path = f"saved_scripts/{file_name}.py"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    while end_signal not in inp:
        if __new_line__:
            inp += "\n" + __nnum__ * "    " + input(f"{line}| " + __nnum__ * "    ")
            if inp.strip().endswith(":"):
                __nnum__ += 1
            elif inp.strip() == "":
                sys.stdout.write(ERASE_LINE)
                __nnum__ -= 1
                continue
        else:
            inp += "\n" + input(f"{line}| ")
            if inp.strip().endswith(":"):
                __new_line__ = True
        line += 1
    
    if export_to_file:
        with open(file_path, "w", encoding="utf-8") as fo:
            fo.write(inp[1:inp.find(end_signal)])
        print(f"\nScript saved at: {os.path.abspath(file_path)}")
    
    print("\nOutput:")
    __run__(inp[1:inp.find(end_signal)])
    __nnum__ = 1
    print("[Program finished]")

# Test a command by trying to execute it
def __test__(inp):
    try:
        __run__(inp, False, False)
    except Exception:
        return False
    else:
        return True

# Run command or expression
def __run__(inp, add_to_history=True, display=True):
    global_var = globals()
    count = 0
    lst = re.findall(r"([\"'])(.*?)\1", inp)
    for i in lst:
        count += i.count(":")
    
    try:
        if not inp.count(":") > count:
            out = eval(inp, global_var)
            if out is not None and display:
                print(out)
        else:
            exec(inp, global_var)
    except Exception:
        traceback.print_exc()
    
    if add_to_history:
        __history__.append(inp)

# Create a customized command
def create_customized_command(end_signal="main.run()"):
    global __new_line__, __nnum__, ERASE_LINE
    __new_line__ = True
    line = 1
    print(f"Run command: {end_signal}")
    command_name = input("Command name: ")
    args = input("Arguments for command (split by \",\"; if no leave this blank): ").replace(" ","").split(",")
    
    if not command_name:
        print("Error: Command name cannot be empty.")
        return
    
    inp = f"def {command_name}({', '.join(args)}):"
    
    while end_signal not in inp:
        if __new_line__:
            inp += "\n" + __nnum__ * "    " + input(f"{line}| " + (__nnum__ - 1) * "    ")
            if inp.strip().endswith(":"):
                __nnum__ += 1
            elif inp.strip() == "":
                sys.stdout.write(ERASE_LINE)
                __nnum__ -= 1
                continue
        else:
            inp += "\n" + input(f"{line}| ")
            if inp.strip().endswith(":"):
                __new_line__ = True
        line += 1
    
    print("\nTesting...")
    if __test__(command_name):
        in_ = input("Existing command! Do you want to overwrite? (y/n): ").strip().lower()
        if in_ == "y":
            with open("customized_command.py", "r", encoding="utf-8") as fi:
                commands = fi.read()
                block = (commands.find(f"def {command_name}"), commands.find("\ndef", commands.find(f"def {command_name}") + 1))
                if block[0] != -1:
                    with open("customized_command.py", "w", encoding="utf-8") as fo:
                        fo.write(commands[:block[0]] + inp[:inp.find(end_signal)] + commands[block[1]:])
        else:
            print("Command creation canceled.")
    else:
        with open("customized_command.py", "a", encoding="utf-8") as fo:
            fo.write(inp[:inp.find(end_signal)] + "\n")
    __nnum__ = 1
    __new_line__ = False

# Delete a customized command
def __del__(command):
    try:
        exec(f"del {command}", globals())
    except Exception:
        print(f"Cannot delete {command}")
    else:
        try:
            with open("customized_command.py", "r", encoding="utf-8") as f:
                script = f.read()
                block = (script.find(f"def {command}"), script.find("\ndef", script.find(f"def {command}") + 1))
                if block[0] != -1:
                    with open("customized_command.py", "w", encoding="utf-8") as f:
                        f.write(script[:block[0]] + script[block[1]:])
        except FileNotFoundError:
            print("No custom command file found.")

# Restore default elements of PyFlex
def __restore_default_elements__():
    try:
        with open("build_2024081105300L.py", encoding="utf-8") as f:
            __run__(f.read()[:-1] + "'cls()')")
    except FileNotFoundError:
        print("Error: Default build file not found.")

# Activate PyFlex
def __active__(startup_command=False, auto_tab=True):
    global __nnum__, __new_line__, __history__, __activated__

    if __activated__:
        return "PyFlex has already been activated"
    else:
        __activated__ = True
    
    if startup_command:
        try:
            __run__(startup_command, False, False)
        except Exception:
            print("Cannot run startup command")
    
    if not auto_tab:
        __nnum__ = 0
    
    print(__info__)

    while __activated__:
        try:
            if __new_line__:
                inp = "\n" + __nnum__ * "    " + input("... " + __nnum__ * "    ")
                if inp.strip().endswith(":"):
                    __nnum__ += 1
                elif inp.strip() == "":
                    sys.stdout.write(ERASE_LINE)
                    __nnum__ -= 1
                    continue
                else:
                    __run__(inp)
                    __new_line__ = False
            else:
                inp = input(">>> ").strip()
                if inp:
                    if inp.endswith(":"):
                        __new_line__ = True
                        continue
                    elif inp.lower() == "^z":
                        inp = "exit()"
                    __run__(inp)
        except Exception:
            traceback.print_exc()

# Display help information
def __help__():
    return """PyFlex Help - Version: 1.1.1dev
Commands:
    cmd(*args, **kwargs)              : Run system commands.
    run(file_path)                    : Run a Python script from a file.
    install(lib)                      : Install a Python library using pip.
    uninstall(lib)                    : Uninstall a Python library using pip.
    upgrade(lib)                      : Upgrade a Python library using pip.
    cls()                             : Clear the console screen.
    logs()                            : Show the command history.
    exit()                            : Exit PyFlex.
    log(index=-1)                     : Re-run a specific command from history.
    create_customized_command()       : Create a custom command.
    __multi_line__(end_signal, export_to_file) : Enter multi-line mode.
    __del__(command)                  : Delete a custom command.
    __restore_default_elements__()    : Restore default elements of PyFlex.
    __active__(startup_command, auto_tab) : Activate PyFlex.

Usage Examples:
    - To run a system command:
        cmd('ls' if __platform__ != 'Windows' else 'dir')
    - To run a Python script:
        run('path\\to\\script.py')
    - To install a library:
        install('requests')
    - To clear the screen:
        cls()
    - To see command history:
        logs()
    - To exit PyFlex:
        exit()
    - To re-run a command from history:
        log(2)  # Re-run the third command in history
    - To create a custom command:
        create_customized_command()
    - To enter multi-line mode:
        __multi_line__()
    - To delete a custom command:
        __del__('my_custom_command')
    - To restore default elements:
        __restore_default_elements__()
    - To activate PyFlex:
        __active__()

For more detailed information, please refer to the documentation or source code.
"""

if __name__ == "__main__":
    __active__()
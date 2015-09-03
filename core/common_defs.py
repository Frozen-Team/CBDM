import os
import platform
import subprocess
import sys


def critical(*msg, exit_code=-1):
    print(*msg, file=sys.stderr)
    sys.exit(exit_code)


def set_system_variable(var_name, var_value):
    if platform.system() == "Windows":
        shell = True
        with open("setx.log", "w") as log_file:
            subprocess.Popen(["setx", var_name, var_value], stdout=log_file, stderr=log_file, shell=shell)
            # TODO: Check exit code


def is_windows():
    return platform.system() == 'Windows'


def is_linux():
    return platform.system() == "Linux"


def load_message(name):
    message_filename = os.path.join('core', 'help_messages', name)
    if os.path.isfile(message_filename):
        with open(message_filename, 'r') as message_file:
            return message_file.read()
    else:
        return

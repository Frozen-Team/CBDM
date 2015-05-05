import os
import platform
import subprocess


def set_system_variable(var_name, var_value):
    if platform.system() == "Windows":
        shell = True
        file = open("setx.log", "w")
        subprocess.Popen(["setx", var_name, var_value], stdout=file, stderr=file, shell=shell)
        file.close()


def is_windows():
    return platform.system() == 'Windows'


def is_linux():
    return platform.system() == "Linux"


def load_message(name):
    message_filename = os.path.join('core', 'messages', name)
    if os.path.isfile(message_filename):
        with open(message_filename, 'r') as message_file:
            return message_file.read()
    else:
        return ''
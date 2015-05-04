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
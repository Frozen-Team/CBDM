import platform
import subprocess

__author__ = 'Maxym'


def set_system_variable(var_name, var_value):
    print(var_value)
    shell = False
    if platform.system() == "Windows":
        shell = True
    file = open("setx.log", "w")
    subprocess.Popen(["setx", var_name, var_value], stdout=file, stderr=file, shell=shell)
    file.close()
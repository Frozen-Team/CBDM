import subprocess
from core.common_defs import is_windows

__author__ = 'Maxym'
    
    
def set_system_variable(var_name, var_value):
    if is_windows():
        shell = True
        with open('setx.log', 'a') as log_file:
            subprocess.Popen(['setx', var_name, var_value], stdout=log_file, stderr=log_file, shell=shell)

import os
import subprocess
import sys
from core.Dependencies.Tasks import check_param


def install_addin_user(module_name, task_params, module_params, result):
    exec_path = os.path.abspath(check_param(module_name, task_params, 'exec_path'))
    if os.path.exists(exec_path):
        subprocess.call([exec_path], shell=True)
    else:
        raise Exception('Cannot find downloaded Qt VS addin."')
        sys.exit(5)
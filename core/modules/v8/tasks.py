import os
import subprocess
from core.Dependencies.Tasks import check_param


def generate_v8_project(module_name, task_params, module_params, result):
    # exec_path = os.path.abspath(check_param(module_name, task_params, 'exec_path'))
    old_path = os.path.abspath(".")
    os.chdir("Lib/")
    os.environ["PATH"] += ";" + old_path + "/Tools/depot_tools"

    gyp_setup_log = open("gyp_setup.log", "w")
    subprocess.call(["D:/Development/CppDepManager/core/modules/v8/Tools/depot_tools/python276_bin/python.exe", "build/gyp/setup.py"], stderr=gyp_setup_log, stdout=gyp_setup_log, shell=True)
    gyp_setup_log.close()

    # gclient_log_file = open("gclient.log", "w")
    # subprocess.call(["gclient", "sync"], stderr=gclient_log_file, stdout=gclient_log_file, shell=True)
    # gclient_log_file.close()




    script_path = "build/gyp_v8"
    if os.path.exists(script_path):
        log_file = open("gyp.log", "w")
        subprocess.call(["D:/Development/CppDepManager/core/modules/v8/Tools/depot_tools/python276_bin/python.exe", script_path], stderr=log_file, stdout=log_file, shell=True)
        log_file.close()
    else:
        raise Exception('Cannot find downloaded Qt VS addin."')
        sys.exit(5)
    os.chdir(old_path)
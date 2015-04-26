import os
import subprocess
from core.Dependencies.Tasks import check_param


def generate_v8_project(module_name, task_params, module_params, result):
    # exec_path = os.path.abspath(check_param(module_name, task_params, 'exec_path'))
    old_path = os.path.abspath(".")
    depot_tools_path = old_path + "/Lib/depot_tools"
    os.chdir(depot_tools_path)
    os.environ["PATH"] += ";" + depot_tools_path

    # gyp_setup_log = open("gyp_setup.log", "w")
    #
    # subprocess.call(["fetch", "v8"], stderr=gyp_setup_log, stdout=gyp_setup_log, shell=True)
    #
    # gyp_setup_log.close()

    gclient_log_file = open("gclient.log", "w")
    subprocess.call(["third_party/python_26/python.exe", "build\gyp_v8", "-Dtarget_arch=x64"], stderr=gclient_log_file, stdout=gclient_log_file, shell=True)
    gclient_log_file.close()




    # script_path = "build/gyp_v8"
    # if os.path.exists(script_path):
    #     log_file = open("gyp.log", "w")
    #     subprocess.call(["D:/Development/CppDepManager/core/modules/v8/Tools/depot_tools/python276_bin/python.exe", script_path], stderr=log_file, stdout=log_file, shell=True)
    #     log_file.close()
    # else:
    #     raise Exception('Cannot find downloaded Qt VS addin."')
    #     sys.exit(5)
    os.chdir(old_path)
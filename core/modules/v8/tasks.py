import os
import subprocess
from core.Dependencies.Tasks import check_param


def prepare_v8(module_name, task_params, module_params, result):
    old_path = os.getcwd()

    # TODO Make task run_command
    depot_tools_path = old_path + "/Lib"
    os.chdir(depot_tools_path)
    os.environ["PATH"] += ";" + depot_tools_path
    print(depot_tools_path)

    log_file = open(old_path + "/gyp_setup.log", "w")
    subprocess.call(["fetch", "v8"], stderr=log_file, stdout=log_file, shell=True)
    log_file.close()

    log_file = open(old_path + "/gclient.log", "w")
    subprocess.call(["gclient", "sync"], stderr=log_file, stdout=log_file, shell=True)
    log_file.close()

    os.chdir(old_path)


def generate_v8_project(module_name, task_params, module_params, result):
    # exec_path = os.path.abspath(check_param(module_name, task_params, 'exec_path'))
    architecture = check_param(module_name, task_params, "architecture", "x64")
    old_path = os.getcwd()
    depot_tools_path = old_path + "{}Lib".format(os.path.sep)

    log_file = open(old_path + "{}gclient.log".format(os.path.sep), "w")
    subprocess.call([depot_tools_path + "python276_bin{}python.exe".format(os.path.sep),
                     "build{}gyp_v8".format(os.path.sep), "-Dtarget_arch=" + architecture],
                    stderr=log_file, stdout=log_file, shell=True)
    log_file.close()




    # script_path = "build/gyp_v8"
    # if os.path.exists(script_path):
    #     log_file = open("gyp.log", "w")
    #     subprocess.call(["D:/Development/CppDepManager/core/modules/v8/Tools/depot_tools/python276_bin/python.exe", script_path], stderr=log_file, stdout=log_file, shell=True)
    #     log_file.close()
    # else:
    #     raise Exception('Cannot find downloaded Qt VS addin."')
    #     sys.exit(5)
    os.chdir(old_path)
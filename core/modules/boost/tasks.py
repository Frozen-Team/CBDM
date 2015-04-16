from glob import glob
import os
import subprocess
import sys
from config import directories
from core.Dependencies.Tasks import check_param
from core.common_defs import set_system_variable


def rename_boost(module_name, task_params, module_params, result):
    lib_folder = directories["libFolder"] + "/"
    path = os.path.join(lib_folder, "boost_*")
    sources_dir = glob(path)
    if len(sources_dir) == 0:
        raise Exception('No directories like "boost_*"')
        sys.exit(5)
    if len(sources_dir) > 1:
        raise Exception('More than one folder with name "boost_*"')
        sys.exit(5)
    to_dir = os.path.join(lib_folder, "boost")
    sources_dir = sources_dir[0]
    os.rename(sources_dir, to_dir)


def set_boost_var(module_name, task_params, module_params, result):
    var_name = "BOOST_ROOT"
    var_value = os.path.abspath(".")
    set_system_variable(var_name, var_value)


def build_boost(module_name, task_params, module_params, result):
    old_chdir = os.path.abspath(".")
    bootstrap_path = os.path.abspath(".") + "/Lib/boost"
    os.chdir(bootstrap_path)
    bootstrap_exec = bootstrap_path + "/bootstrap.bat"

    log_file = open("build_b2.log", "w")
    subprocess.call([bootstrap_exec], stdout=log_file, stderr=log_file, shell=True)
    log_file.close()

    b2_exec = bootstrap_path + "/b2.exe"

    log_file = open("build_boost.log", "w")
    subprocess.call([b2_exec], stdout=log_file, stderr=log_file, shell=True)
    log_file.close()

    os.chdir(old_chdir)
from glob import glob
import os
import sys
import shutil
from config import directories


def rename_cmake_folder(module_name, task_params, module_params, result):
    lib_folder = directories["tools_path"] + "/"
    path = os.path.join(lib_folder, "cmake-*")

    sources_dir = glob(path)
    if len(sources_dir) == 0:
        raise Exception('No directories like "cmake-*"')
        sys.exit(5)
    if len(sources_dir) > 1:
        raise Exception('More than one folder with name "cmake-*"')
        sys.exit(5)
    to_dir = os.path.join(lib_folder, "cmake")
    sources_dir = sources_dir[0]
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    shutil.move(sources_dir, to_dir)
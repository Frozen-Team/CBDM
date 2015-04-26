import os
import glob
import shutil
import core.Dependencies.Tasks as tasks
from core.cmake import Cmake

def create_cmake_file(module_name, task_params, module_params, result):
    cmake_file = Cmake('./sources', {})
    cmake_file.find_sources('')
import os

from config import directories
import config
from core.Tasks import check_dependencies, vcs, cmake, assembly, fs
from core.common_defs import is_linux, is_windows


import os
from config import directories

from glob import glob
import os
import subprocess
import sys
from config import directories
from core.Dependencies.Tasks import check_param
from core.common_defs import set_system_variable


# def rename_boost(module_name, task_params, module_params, result):
#     lib_folder = directories["libFolder"] + "/"
#     path = os.path.join(lib_folder, "boost_*")
#     sources_dir = glob(path)
#     if len(sources_dir) == 0:
#         raise Exception('No directories like "boost_*"')
#         sys.exit(5)
#     if len(sources_dir) > 1:
#         raise Exception('More than one folder with name "boost_*"')
#         sys.exit(5)
#     to_dir = os.path.join(lib_folder, "boost")
#     sources_dir = sources_dir[0]
#     os.rename(sources_dir, to_dir)
#
#
# def set_boost_var(module_name, task_params, module_params, result):
#     var_name = "BOOST_ROOT"
#     var_value = os.path.abspath(".")
#     set_system_variable(var_name, var_value)
#
#
# def build_boost(module_name, task_params, module_params, result):
#     old_chdir = os.path.abspath(".")
#     bootstrap_path = os.path.abspath(".") + "/Lib/boost"
#     os.chdir(bootstrap_path)
#     bootstrap_exec = bootstrap_path + "/bootstrap.bat"
#
#     log_file = open("build_b2.log", "w")
#     subprocess.call([bootstrap_exec], stdout=log_file, stderr=log_file, shell=True)
#     log_file.close()
#
#     b2_exec = bootstrap_path + "/b2.exe"
#
#     log_file = open("build_boost.log", "w")
#     subprocess.call([b2_exec], stdout=log_file, stderr=log_file, shell=True)
#     log_file.close()
#
#     os.chdir(old_chdir)


# boost_path = os.path.join(directories["downloadDir"], 'boost.7z')
# libFolder = directories["libFolder"] + "/"
# full_path = os.path.abspath(".")
# build_tasks = [
#     {"task": "check_dependencies", "params": ("version", 'rebuild')},
#     {"task": "download_file", "destination": boost_path,
#      "url": "http://sourceforge.net/projects/boost/files/boost/1.57.0/boost_{version}.7z/download"},
#     {"task": "un_7_zip", "file_location": boost_path, "destination": libFolder},
#     {"task": "rename_folder_by_mask", 'mask': 'boost_*', 'destination': 'Lib/boost',
#      'description': "Renaming sources folder", 'override': True},
#     # {'task': 'rename_boost', 'user_task': True},
#     {"task": "set_boost_var", "user_task": True},
#     {"task": "build_boost", "user_task": True}
#
#     # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
# ]


origin_dir = 'Origin'
build_directory = os.path.join(directories['buildDir'], 'cppformat')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'include')
vcxproj_file = os.path.join(origin_dir, 'cppformat_{0}', 'format.vcxproj')


def build_lib(architecture):
    if is_linux():
        assembly.make(origin_dir)
    if is_windows():
        vcxproj_path = vcxproj_file.format(architecture)
        assembly.set_vcxproj_runtime_library(vcxproj_path, config.visual_studio_runtime_library)
        assembly.set_vcxproj_platform_toolset(vcxproj_path, config.visual_studio_toolset)
        assembly.build_vcxproj(vcxproj_path, lib_directory)


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    fs.remove(origin_dir)
    vcs.git_clone('https://github.com/cppformat/cppformat.git', origin_dir, True)
    vcs.git_checkout(origin_dir, module_params['version'])
    cmake.run_cmake(origin_dir, 'x86',  'cppformat_x86')
    build_lib('x86')
    cmake.run_cmake(origin_dir, 'x64',  'cppformat_x64')
    build_lib('x64')
    fs.move_files_to_dir_by_mask(os.path.join(origin_dir, '*.h'), headers_dir, True)


def integration(module_params):
    cmake.add_location(headers_dir)
    if is_windows():
        # x86
        cmake.add_library(('windows', 'x86', 'release'),
                          os.path.join(lib_directory, 'Release', 'Win32', 'format.lib'))
        cmake.add_library(('windows', 'x86', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'Win32', 'format.lib'))
        # x64
        cmake.add_library(('windows', 'x64', 'release'),
                          os.path.join(lib_directory, 'Release', 'x64', 'format.lib'))
        cmake.add_library(('windows', 'x64', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'x64', 'format.lib'))
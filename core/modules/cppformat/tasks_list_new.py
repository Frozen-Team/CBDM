import os

from config import directories
from core.Tasks import check_dependencies, vcs, cmake, assembly, fs
from core.common_defs import is_linux, is_windows


origin_dir = "Origin"
build_directory = os.path.join(directories['buildDir'], 'cppformat')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'headers')
vcxproj_file = os.path.join(origin_dir, 'cppformat_{0}', 'format.vcxproj')


def build_lib(architecture):
    if is_linux():
        assembly.make(origin_dir)
    if is_windows():
        vcxproj_path = vcxproj_file.format(architecture)
        assembly.set_vcxproj_runtime_library(vcxproj_path, 'MD')
        assembly.set_vcxproj_platform_toolset(vcxproj_path, 'v120')
        assembly.build_vcxproj(vcxproj_path, lib_directory)


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    fs.remove(origin_dir)
    vcs.git_clone("https://github.com/cppformat/cppformat.git", origin_dir, True)
    vcs.git_checkout(origin_dir, module_params['version'])
    cmake.run_cmake(origin_dir, 'x86',  os.path.join(origin_dir, 'cppformat_x86'))
    build_lib('x86')
    cmake.run_cmake(origin_dir, 'x64',  os.path.join(origin_dir, 'cppformat_x64'))
    build_lib('x64')
    fs.move_files_to_dir_by_mask(os.path.join(origin_dir, '*.h'), headers_dir, True)


integration_tasks = [

    {'task': 'add_library', 'config': ('windows', 'x86', 'release'), 'library_location':
        os.path.join(build_directory + '/Release/Win32/format.lib')},
    {'task': 'add_library', 'config': ('windows', 'x86', 'debug'), 'library_location':
        os.path.join(build_directory + '/Debug/Win32/format.lib')},
    # x32
    {'task': 'add_library', 'config': ('windows', 'x64', 'release'), 'library_location':
        os.path.join(build_directory + '/Release/x64/format.lib')},
    {'task': 'add_library', 'config': ('windows', 'x64', 'debug'), 'library_location':
        os.path.join(build_directory + '/Debug/x64/format.lib')},

    {'task': 'add_location', 'location': headers_dir},
]
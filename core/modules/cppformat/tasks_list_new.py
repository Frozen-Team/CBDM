import os

from config import directories
from core.Tasks import check_dependencies, vcs, cmake, assembly, fs
from core.common_defs import is_linux, is_windows
from core.default_structures import cleanup_extensions


sources_dir = "sources"
build_directory = os.path.join(directories['buildDir'], 'cppformat')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'headers')
vcxproj_file = os.path.join(sources_dir, 'format.vcxproj')

build_tasks = [
    {"task": "run_cmake_and_build", "sources_dir": sources_dir, "architecture": "x32",
     "user_task": True, 'description': 'Running cmake for Win32...'},
    {"task": "set_vcxproj_runtime_library", "vcxproj_file": vcxproj_file, 'description': 'Setting runtime library...'},
    {"task": "make", "vcxproj_file": vcxproj_file, 'output_dir': lib_directory,
     'description': 'Build project for win32'},

    {"task": "run_cmake_and_build", "sources_dir": sources_dir, "architecture": "x64",
     "user_task": True, 'description': 'Running cmake for Win64...'},
    {"task": "set_vcxproj_runtime_library", "vcxproj_file": vcxproj_file, 'description': 'Setting runtime library...'},
    {"task": "make", "vcxproj_file": vcxproj_file, 'output_dir': lib_directory,
     'description': 'Build project for win64'},


    {"task": "move_files_to_dir_by_mask", 'overwrite': True, 'destination': headers_dir,
     'mask': os.path.join(sources_dir, '*.h'), 'description': "Copy includes..."},
    {"task": "rdfff", "directory": sources_dir, "extensions": cleanup_extensions["c++"],
     'description': 'Cleaning up trash..'}

]


def build_lib():
    if is_linux():
        assembly.make(sources_dir)
    if is_windows():
        assembly.set_vcxproj_runtime_library(vcxproj_file, 'MD')
        assembly.set_vcxproj_platform_toolset(vcxproj_file, 'vc120')
        assembly.build_vcxproj(vcxproj_file, lib_directory)


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    vcs.git_clone("https://github.com/cppformat/cppformat.git", sources_dir, True)
    vcs.git_checkout(sources_dir, module_params['version'])
    cmake.run_cmake(sources_dir, 'x86', 'arch_x86')
    build_lib()
    cmake.run_cmake(sources_dir, 'x64', 'arch_x64')
    build_lib()
    fs.move_files_to_dir_by_mask(os.path.join(sources_dir, '*.h'), headers_dir, True)


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
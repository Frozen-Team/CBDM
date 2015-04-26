import os

from config import directories
from core.default_structures import cleanup_extensions


sources_dir = "sources"
archive_path = 'glfw.zip'
build_directory = os.path.join(directories['buildDir'], 'glfw')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'headers')

glfw_path = directories["libFolder"] + os.path.sep
glfw_vcxproj = os.path.join(sources_dir, "src", "glfw.vcxproj")
build_tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "https://github.com/glfw/glfw.git", "sources_dir": sources_dir,
     'description': 'Cloning glfw...'},
    {"task": "git_checkout", "sources_dir": sources_dir, "branch": "{version}", 'description': 'Checkout...'},


    # x86
    {"task": "run_cmake_and_build", "sources_dir": sources_dir,
     "architecture": "x86", "user_task": True, 'description': 'Generating solution...'},
    {"task": "set_vcxproj_runtime_library", "vcxproj_file": glfw_vcxproj, 'description': 'Setting runtime library...'},
    {"task": "make", "output_dir": lib_directory, "vcxproj_file": glfw_vcxproj, 'description': 'Building...'},


    # x64
    {"task": "run_cmake_and_build", "sources_dir": sources_dir, "architecture": "x64",
     "user_task": True, 'description': 'Generating solution...'},
    {"task": "set_vcxproj_runtime_library", "vcxproj_file": glfw_vcxproj, 'description': 'Setting runtime library...'},
    {"task": "make", "output_dir": lib_directory, "vcxproj_file": glfw_vcxproj, 'description': 'Building...'},

    {"task": "move_files_to_dir_by_mask", 'overwrite': True, 'destination_dir': headers_dir,
     'mask': os.path.join(sources_dir, 'include', 'GLFW', '*.h'), 'description': "Copy includes..."},
    {"task": "rdfff", "directory": sources_dir, "extensions": cleanup_extensions["c++"],
     'description': 'Cleaning up trash..'}
]


import os
from config import directories

glfw_path = directories["libFolder"] + os.path.sep
glfw_zip_path = os.path.join(directories["downloadDir"], 'glfw.zip')
glfw_vcxproj = os.path.join(glfw_path, "src", "glfw.vcxproj")
build_tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "https://github.com/glfw/glfw.git", "sources_dir": glfw_path,
     'description': 'Cloning glfw...'},
    {"task": "git_checkout", "sources_dir": glfw_path, "branch": "{version}", 'description': 'Checkout...'},
    {"task": "run_cmake_and_build",  "sources_dir": glfw_path, "output": directories["buildDir"],
     "architecture": "x86", "user_task": True, 'description': 'Generating solution...'},

    {"task": "set_vcxproj_runtime_library", "vcxproj_file": glfw_vcxproj, 'description': 'Setting runtime library...'},
    {"task": "make",
     "output_dir": glfw_path + 'build',
     "vcxproj_file": glfw_vcxproj, 'description': 'Building...'
     },
]


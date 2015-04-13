import os
from config import directories

cmake_path = os.path.join(directories["downloadDir"], 'cmake.zip')
cmake_exe_path = directories["tools_path"] + "/cmake/bin/cmake.exe"
tasks = [
    {"task": "check_dependencies", "params": ("version",)},
    {"task": "download_file", "destination": cmake_path,
     "url": "http://www.cmake.org/files/v3.2/cmake-{version}-win32-x86.zip"},
    {"task": "unzip", "file_location": cmake_path, "destination": directories["tools_path"] + "/"},
    {'task': 'rename_cmake_folder', 'user_task': True},
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
import os
from config import directories

cmake_path = os.path.join(directories["downloadDir"], 'cmake.zip')
cmake_exe_path = directories["tools_path"] + "/cmake/bin/cmake.exe"
build_tasks = [
    {"task": "check_dependencies", "params": ("version",), 'description': 'Checking dependencies'},
    {"task": "download_file", "destination": cmake_path,
    "url": "http://www.cmake.org/files/v3.2/cmake-{version}-win32-x86.zip",
    'description': 'Downloading cmake'
    },
    {"task": "unzip", "file_location": cmake_path, "destination": directories["tools_path"] + "/",
    'description': 'Unzip cmake'},
    {'task': 'rename_cmake_folder', 'user_task': True, 'description': 'Rename cmake folder'},
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
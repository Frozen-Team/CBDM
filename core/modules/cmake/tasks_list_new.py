import os
from shutil import which
from core.Dependencies.library_module_new import LibraryModule
from core.common_defs import is_linux, is_windows
import core.sys_config as s_config
from config import directories
from core.Tasks import check_dependencies, net, archives, fs, assembly

cmake_path = 'cmake.zip'
cmake_exe_path = s_config.tools_directory + "/cmake/bin/cmake.exe"
build_tasks = [
    {"task": "unzip", "file_location": cmake_path, "destination": directories["tools_path"] + "/",
     'description': 'Unzip cmake'},
    {'task': 'rename_cmake_folder', 'user_task': True, 'description': 'Rename cmake folder'},
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
integration_tasks = [
    {'task': 'set_bin_to_result', 'user_task': True}
]


def build(module_params):
    if is_linux():
        check_dependencies(['gksudo'])
        assembly.install_distro_dependencies(['cmake'])
    elif is_windows():
        check_dependencies(False, ['version'])
        cmake_url = "http://www.cmake.org/files/v3.2/cmake-{}-win32-x86.zip".format(module_params['version'])
        net.download_file(cmake_url, cmake_path)
        archives.extract_7_zip(cmake_path, s_config.tools_directory + os.path.sep)
        fs.remove(cmake_path)
        fs.rename(os.path.join(s_config.tools_directory, 'cmake-*'), os.path.join(s_config.tools_directory, 'cmake'))

def integration(module_params):
    results = LibraryModule.current_working_module_results
    if is_linux():
        results['path'] = which('cmake')
    elif is_windows():
        results['path'] = cmake_exe_path


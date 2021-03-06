import os
import re
import core.sys_config as s_config
from shutil import which
from core.Dependencies.library_module import LibraryModule
from core.common_defs import is_linux, is_windows
from core.Tasks import check_dependencies, net, archives, fs, assembly

cmake_path = 'cmake.zip'
cmake_exe_path = s_config.tools_directory + "/cmake/bin/cmake.exe"


def build(module_params):
    if is_linux():
        check_dependencies(['gksudo'])
        assembly.install_distro_dependencies(['cmake'])
    elif is_windows():
        check_dependencies(False, ['version'])
        small_version = '.'.join(str(module_params['version']).split('.')[0:2])
        cmake_url = "http://www.cmake.org/files/v{0}/cmake-{1}-win32-x86.zip".format(small_version,
                                                                                     module_params['version'])
        net.download_file(cmake_url, cmake_path)
        archives.extract_7_zip(cmake_path, s_config.tools_directory + os.path.sep)
        fs.remove(cmake_path)
        fs.rename(os.path.join(s_config.tools_directory, 'cmake-*'), os.path.join(s_config.tools_directory, 'cmake'),
                  True)



def integration(module_params):
    results = LibraryModule.results
    if is_linux():
        results['path'] = which('cmake')
    elif is_windows():
        results['path'] = cmake_exe_path


import os
import platform
from shutil import which
from config import directories
from core.Tasks import assembly, fs, check_dependencies
from core.Dependencies.library_module_new import LibraryModule
from core.common_defs import is_linux, is_windows
import core.sys_config as s_config


def build(module_params):
    if is_linux():
        check_dependencies(['gksudo'])
        assembly.install_distro_dependencies(['p7zip-full'])


def integration(module_params):
    results = LibraryModule.current_working_module_results
    if is_linux():
        results['path'] = which('7z')
    elif is_windows():
        results['path'] = os.path.join(s_config.tools_directory, '7z.exe')
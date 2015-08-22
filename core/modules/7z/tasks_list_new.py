import os
from shutil import which

from core.Tasks import assembly, check_dependencies
from core.Dependencies.library_module import LibraryModule
from core.common_defs import is_linux, is_windows
import core.sys_config as s_config


def build(module_params):
    if is_linux():
        check_dependencies(['gksudo'])
        assembly.install_distro_dependencies(['p7zip-full'])


def integration(module_params):
    results = LibraryModule.results
    if is_linux():
        results['path'] = which('7z')
    elif is_windows():
        results['path'] = os.path.join(s_config.tools_directory, '7z.exe')
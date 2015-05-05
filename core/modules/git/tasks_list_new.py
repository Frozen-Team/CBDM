import os
from shutil import which

from core.Dependencies.library_module import LibraryModule
from core.Tasks import net, archives, check_dependencies, assembly
from core.common_defs import is_linux, is_windows
import core.sys_config as s_config


git_archive = 'git.zip'
git_path = os.path.join(s_config.tools_directory, 'git')
git_exe_path = os.path.join(git_path, 'bin', 'git.exe')


def build(module_params):
    if is_linux():
        check_dependencies(['gksudo'])
        assembly.install_distro_dependencies(['git'])
    elif is_windows():
        net.download_file("https://dl.dropboxusercontent.com/u/92011034/git.zip", git_archive)
        archives.extract_7_zip(git_archive, git_path)


def integration(module_params):
    results = LibraryModule.current_working_module_results
    if is_linux():
        results['path'] = which('git')
    elif is_windows():
        results['path'] = git_exe_path
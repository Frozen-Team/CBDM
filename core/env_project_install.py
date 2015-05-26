import os
from config import projectName
from core.Dependencies.library_module import LibraryModule
from core.common_defs import set_system_variable


def get_paths(paths_to_combine):
    return os.pathsep.join(paths_to_combine)


def get_libs_names(libs_to_combine):
    libs_names = list(libs_to_combine)
    result = map(lambda a: str(a) + '.lib', libs_names)

    return os.pathsep.join(result)


def project_install_to_env():
    archs = ['x86', 'x64']
    configs = ['debug', 'release']
    for arch in archs:
        for config in configs:
            libs_str = get_paths(
                LibraryModule.current_working_module_results['link_directories'][('windows', arch, config)])
            set_system_variable(projectName + '_lib_paths_' + arch + '_' + config, libs_str)
            set_system_variable(projectName + '_lib_names_' + arch + '_' + config, get_libs_names(
                LibraryModule.current_working_module_results['libs'][('windows', arch, config)]))

    include_paths = LibraryModule.current_working_module_results['headers']
    set_system_variable(projectName + '_include_paths', get_paths(include_paths))

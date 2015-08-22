import os
from config import projectName
from core.dependencies.library_module import LibraryModule
from core.common_defs import set_system_variable


def get_paths(paths_to_combine):
    return os.pathsep.join(paths_to_combine)


def get_libs_names(libs_to_combine):
    libs_names = list(libs_to_combine)
    result = map(lambda a: str(a) + '.lib', libs_names)

    return os.pathsep.join(result)


def split_env(in_str):
    result = []
    strs = str(in_str).split(os.pathsep)
    len_counter = 0
    counter = 0
    for j in range(0, len(strs) - 1):
        len_counter += len(strs[j])
        if len_counter + len(strs[j + 1]) > 256:
            result.append(os.pathsep.join(strs[counter: j + 1]))
            len_counter = 0
            counter = j + 1
    result.append(os.pathsep.join(strs[counter: len(strs)]))
    return result


def project_install_to_env():
    archs = ['x86', 'x64']
    configs = ['debug', 'release']
    results = LibraryModule.current_working_module_results
    for arch in archs:
        for config in configs:
            libs_paths = split_env(get_paths(results['link_directories'][('windows', arch, config)]))
            libs_names = split_env(get_libs_names(results['libs'][('windows', arch, config)]))

            for counter, path in enumerate(libs_paths):
                set_system_variable(projectName + '_lib_paths_' + arch + '_' + config + '_' + str(counter), path)

            for counter, name in enumerate(libs_names):
                set_system_variable(projectName + '_lib_names_' + arch + '_' + config + '_' + str(counter), name)

    include_paths = results['headers']

    set_system_variable(projectName + '_include_paths', get_paths(include_paths))

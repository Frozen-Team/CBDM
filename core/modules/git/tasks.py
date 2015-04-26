import os

path_to_git = os.path.abspath('Tools/git/bin/git.exe')


def add_path_to_git(module_name, task_params, module_params, result):
    result['path'] = path_to_git
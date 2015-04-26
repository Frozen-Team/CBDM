import os
from config import directories


path_to_git = directories["project_dir"] + "{0}Tools{0}git{0}bin{0}git.exe".format(os.path.sep)


def add_path_to_git(module_name, task_params, module_params, result):
    result['path'] = path_to_git
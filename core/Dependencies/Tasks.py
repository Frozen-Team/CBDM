from shutil import which, rmtree
import sys
from core.git import Repo
import os
import core.sys_config as s_config


def readonly_handler(func, path, execinfo):
    os.chmod(path, 128)
    func(path)


def check_dependencies(module_name, task_params, module_params, result):
    if 'programs' in task_params:
        for program_name in task_params['programs']:
            if which(program_name) is None:
                error = s_config.no_external_program_error.format(program_name=program_name.upper())
                raise Exception(error)
                sys.exit(15)
    if 'params' in task_params:
        for param_name in task_params['params']:
            if param_name not in module_params:
                error = s_config.no_module_param_error.format(module_name=module_name, param_name=param_name)
                raise Exception(error)
                sys.exit(15)


def git_clone(module_name, task_params, module_params, result):
    repo_dir = task_params["sources_dir"] if "sources_dir" in task_params else ""
    repository = Repo(repo_dir, module_name+'_log')
    if repository.is_repo() and module_params['rebuild']:
        rmtree(repo_dir, ignore_errors=False, onerror=readonly_handler)
    repository.clone(task_params["repository"])


def git_checkout(module_name, task_params, module_params, result):
    repo_dir = task_params["sources_dir"] if "sources_dir" in task_params else ""
    repository = Repo(repo_dir)
    repository.checkout(task_params['branch'].format(version=module_params['version']))


def add_library(module_name, task_params, module_params, result):
    params = task_params['config']
    result['libs'][params[0]][params[1]][params[2]].append(task_params['library_location'])


def add_location(module_name, task_params, module_params, result):
    result['headers'].append(task_params['location'])
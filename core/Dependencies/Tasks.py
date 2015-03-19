from shutil import which, rmtree
import sys
from urllib.request import urlopen, urlretrieve
from zipfile import ZipFile
from core.git import Repo
import os
import core.sys_config as s_config


def check_param(module_name, params, param_name, default_value=None):
    if param_name not in params:
        if default_value is None:
            raise Exception(s_config.no_module_local_param_error.format(module_name=module_name, param_name=param_name))
            sys.exit(20)
        else:
            return default_value
    return params[param_name]


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
    repo_dir = check_param(module_name, task_params, 'sources_dir', '')
    repository = Repo(repo_dir, module_name+'_log')
    if repository.is_repo() and module_params['rebuild']:
        rmtree(repo_dir, ignore_errors=False, onerror=readonly_handler)
    repository.clone(task_params["repository"])


def git_checkout(module_name, task_params, module_params, result):
    check_param(module_name, task_params, 'branch')
    repo_dir = check_param(module_name, task_params, 'sources_dir', '')
    repository = Repo(repo_dir, module_name+'_log')
    repository.checkout(task_params['branch'])


def add_library(module_name, task_params, module_params, result):
    check_param(module_name, task_params, 'config')
    check_param(module_name, task_params, 'library_location')
    params = task_params['config']
    result['libs'][params[0]][params[1]][params[2]].append(task_params['library_location'])


def add_location(module_name, task_params, module_params, result):
    check_param(module_name, task_params, 'location')
    result['headers'].append(task_params['location'])


def download_file(module_name, task_params, module_params, result):
    check_param(module_name, task_params, 'url')
    check_param(module_name, task_params, 'destination')
    urlretrieve(task_params['url'], task_params['destination'])


def unzip(module_name, task_params, module_params, result):
    location = check_param(module_name, task_params, 'file_location')
    destination = check_param(module_name, task_params, 'destination', 'extracted-zip')
    with ZipFile(location, 'r') as archive:
        archive.extractall(destination)
from errno import EEXIST
from glob import glob
from shutil import which, rmtree
import sys
from urllib.request import urlretrieve
from zipfile import ZipFile
import subprocess
import shutil
from config import directories, cmakeGenerator
from core.git import Repo
import os
from core.modules.cmake.tasks_list import cmake_exe_path
import core.sys_config as s_config
import platform
from core.vcxproj import Builder

if sys.platform.startswith('win'):
    shell = True
else:
    shell = False


def require_dir(path):
    try:
        dir_name = os.path.dirname(path)
        if dir_name != '':
            os.makedirs(dir_name, 777)
    except OSError as exc:
        if exc.errno != EEXIST:
            raise


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
    repository = Repo(repo_dir, module_name + '.log')
    if repository.is_repo() and module_params['rebuild']:
        rmtree(repo_dir, ignore_errors=False, onerror=readonly_handler)
    repository.clone(task_params["repository"])


def git_checkout(module_name, task_params, module_params, result):
    check_param(module_name, task_params, 'branch')
    repo_dir = check_param(module_name, task_params, 'sources_dir', '')
    repository = Repo(repo_dir, module_name + '.log')
    repository.checkout(task_params['branch'])


def add_library(module_name, task_params, module_params, result):
    cfg = check_param(module_name, task_params, 'config')
    lib_location = check_param(module_name, task_params, 'library_location')
    abs_lib_location = os.path.abspath(lib_location)
    result['libs'][cfg[0]][cfg[1]][cfg[2]].append(abs_lib_location)


def add_location(module_name, task_params, module_params, result):
    location = check_param(module_name, task_params, 'location')
    abs_location = os.path.abspath(location)
    result['headers'].append(abs_location)


def remove_file_by_mask(module_name, task_params, module_params, result):
    mask = check_param(module_name, task_params, 'mask')
    files_to_delete = glob(mask)
    for file in files_to_delete:
        if os.path.isfile(file):
            os.remove(file)
        else:
            rmtree(file, ignore_errors=False, onerror=readonly_handler)


def rename_folder_by_mask(module_name, task_params, module_params, result):
    mask = check_param(module_name, task_params, 'mask')
    override = check_param(module_name, task_params, 'override', False)
    destination = check_param(module_name, task_params, 'destination')

    folders = glob(mask)
    folders_count = len(folders)
    if folders_count < 1:
        raise Exception('No mask folder')
        sys.exit(15)
    if folders_count > 1:
        raise Exception('More than one mask folder exists')
        sys.exit(15)

    if os.path.isdir(destination):
        if override:
            shutil.rmtree(destination, ignore_errors=False, onerror=readonly_handler)
        else:
            raise Exception('Destination folder exists')
            sys.exit(15)

    shutil.move(folders[0], destination)


def move_files(module_name, task_params, module_params, result):
    from_path = check_param(module_name, task_params, 'from_path')
    to_path = check_param(module_name, task_params, 'to_path')
    files_list = os.listdir(from_path)
    for f in files_list:
        full_from_path = from_path + "/" + f
        shutil.move(full_from_path, to_path)


def download_file(module_name, task_params, module_params, result):
    url_path = check_param(module_name, task_params, 'url')
    destination = check_param(module_name, task_params, 'destination')
    require_dir(destination)
    urlretrieve(url_path, destination)


def unzip(module_name, task_params, module_params, result):
    location = check_param(module_name, task_params, 'file_location')
    destination = check_param(module_name, task_params, 'destination', '')
    require_dir(destination)
    with ZipFile(location, 'r') as archive:
        archive.extractall(destination)


def untar(module_name, task_params, module_params, result):
    location = check_param(module_name, task_params, 'file_location')
    destination = check_param(module_name, task_params, 'destination', False)
    require_dir(destination)
    archiver_loc = which('tar')
    if not os.path.exists(destination):
        os.makedirs(destination)
    if archiver_loc is None:
        raise Exception("TAR IS NOT INSTALLED ON SYSTEM")
        sys.exit(1)
    exec_command = [archiver_loc, '-xzf', location]
    if destination:
        exec_command.extend('-C "{}"'.format(destination))
    subprocess.Popen(" ".join(exec_command), shell=True).communicate()


def un_7_zip(module_name, task_params, module_params, result):
    location = check_param(module_name, task_params, 'file_location')
    destination = check_param(module_name, task_params, 'destination', 'extracted_7zip')
    require_dir(destination)
    # archiver_loc = which('7z')
    archiver_loc = directories["tools_path"] + "/7za.exe"
    if not os.path.exists(destination):
        os.makedirs(destination)
    if archiver_loc is None:
        raise Exception("7Z IS NOT INSTALLED ON SYSTEM")
        sys.exit(1)
    exec_command = ['"{}"'.format(archiver_loc), 'x', '"{}"'.format(location),
                    '-o' + '"{}"'.format(destination), '-y', '>7z.log']
    subprocess.Popen(" ".join(exec_command), shell=shell).communicate()


def configure(module_name, task_params, module_params, result):
    if platform.system() == 'Linux':
        prev_wd = os.getcwd()
        makefile_pth = os.path.abspath(check_param(module_name, task_params, 'directory'))
        params = check_param(module_name, task_params, 'params')
        params_str = " ".join(["{0}={1}".format(key, val) for key, val in params.items()])
        os.chdir(makefile_pth)
        if os.path.isfile('configure'):
            subprocess.Popen(['./configure ' + params_str], shell=shell).communicate()
        os.chdir(prev_wd)


def make_install(module_name, task_params, module_params, result):
    if platform.system() == 'Linux':
        prev_wd = os.getcwd()
        makefile_pth = os.path.dirname(check_param(module_name, task_params, 'directory'))
        os.chdir(makefile_pth)
        subprocess.Popen(['gksudo make install'], shell=True).communicate()
        os.chdir(prev_wd)


def install_distro_dependencies(distro, dependencies):
    package_manager = {"Ubuntu": 'apt-get'}
    dep_process = subprocess.Popen('gksudo -S apt-get install -y ' + " ".join(dependencies), shell=shell)
    dep_process.communicate(subprocess.PIPE)


def make(module_name, task_params, module_params, result):
    system = platform.system()
    if system == 'Linux':
        prev_wd = os.getcwd()
        makefile_pth = check_param(module_name, task_params, 'makefile')
        params = check_param(module_name, task_params, 'params', {})
        deps = check_param(module_name, task_params, 'linux_dependencies', {})
        distro, version, subversion = platform.dist()
        distro_deps = deps[distro] if distro in deps else {}
        install_distro_dependencies(distro, distro_deps)
        params_str = " ".join(["{0}={1}".format(key, val) for key, val in params.items()])
        os.chdir(os.path.dirname(makefile_pth))
        make_loc = which('make')
        if make_loc is None:
            raise Exception("'MAKE' IS NOT INSTALLED ON SYSTEM")
            sys.exit(1)
        subprocess.Popen(['make ' + params_str], stdin=subprocess.PIPE, shell=shell).communicate()
        os.chdir(prev_wd)
    else:
        if system == 'Windows':
            vcxproj_pth = check_param(module_name, task_params, 'vcxproj_file')
            project = Builder(vcxproj_pth)
            debug_conf = project.get_configuration("Debug")
            debug_conf.set_runtime_library("MultiThreadedDebugDLL")
            debug_conf.set_platform_toolset("v120")
            debug_conf.save()
            release_conf = project.get_configuration("Release")
            release_conf.set_runtime_library("MultiThreadedDLL")
            release_conf.set_platform_toolset("v120")
            release_conf.save()
            project.build()


def check_runtime_library(module_name, task_params, module_params, result):
    system = platform.system()
    if system == 'Windows':
        vcxproj_pth = check_param(module_name, task_params, 'vcxproj_file')
        project = Builder(vcxproj_pth)
        debug_conf = project.get_configuration("Debug")
        debug_conf.set_platform_toolset("v120")
        debug_conf.set_runtime_library("MultiThreadedDebugDLL")
        debug_conf.save()
        release_conf = project.get_configuration("Release")
        release_conf.set_platform_toolset("v120")
        release_conf.set_runtime_library("MultiThreadedDLL")
        release_conf.save()


def cmake_generate(module_name, task_params, module_params, result):
    system = platform.system()
    if system == 'Windows':
        sources_dir = os.path.abspath(check_param(module_name, task_params, 'sources_dir'))
        destination_dir = os.path.abspath(check_param(module_name, task_params, 'destination_dir'))
        architecture = check_param(module_name, task_params, 'architecture').lower()
        generator = cmakeGenerator
        if architecture == "win32":
            subprocess.call([cmake_exe_path, "-G", generator, "-B", destination_dir, "-H", sources_dir], shell=shell)
        elif architecture == "win64":
            generator += " Win64"
        else:
            raise Exception("Cannot find architecture in supported: " + architecture)
            sys.exit(1)
        subprocess.Popen([cmake_exe_path, "-G", generator, "-B" + destination_dir, "-H" + sources_dir],
                         stderr=subprocess.STDOUT, shell=shell).communicate()


# def rename(module_name, task_params, module_params, result):
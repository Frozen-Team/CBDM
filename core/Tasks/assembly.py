import os
import platform
from shutil import which
import subprocess
import sys
from core import sys_config
from core.Tasks import fs
from core.TemporaryDir import TemporaryDir
from core.tools.vcxproj import Builder

__author__ = 'saturn4er'


def configure(directory, params):
    params_str = " ".join(["{0}={1}".format(key, val) for key, val in params.items()])
    TemporaryDir.enter(directory)
    if os.path.isfile('configure'):
        process = subprocess.Popen(['./configure ' + params_str], shell=True)
        process.communicate()
        if process.returncode != 0:
            raise Exception("'Configure' finished with status-code " + process.returncode)
            sys.exit(1)
    TemporaryDir.leave()


def build_vcxproj(path_to_vcxproj, output_dir=False, configurations=False, architectures=False):
    print('Building %s' % path_to_vcxproj)
    project = Builder(path_to_vcxproj)
    project.build(configurations, architectures, output_dir)


def make(path_to_makefile, params=False, dependencies=False):
    if not bool(params):
        params = {}
    if not bool(dependencies):
        dependencies = {}
    if bool(dependencies):
        install_distro_dependencies(dependencies)
    params_str = " ".join(["{0}={1}".format(key, val) for key, val in params.items()])

    make_loc = which('make')
    if make_loc is None:
        raise Exception("'MAKE' IS NOT INSTALLED ON SYSTEM")
        sys.exit(1)

    login_file_name = os.path.join(sys_config.log_folder, 'make.txt')
    fs.create_path_to(login_file_name)
    with open(login_file_name, 'w+') as log_file:
        TemporaryDir.enter(os.path.abspath(path_to_makefile))
        process = subprocess.Popen(['make ' + params_str], stderr=log_file, stdout=log_file, stdin=subprocess.PIPE,
                                   shell=True)
        process.communicate()
        if process.returncode != 0:
            raise Exception("'MAKE' finished with status-code " + str(process.returncode))
            sys.exit(1)
    TemporaryDir.leave()


def make_install(directory):
    TemporaryDir.enter(directory)

    process = subprocess.Popen(['gksudo make install'], shell=True)
    process.communicate()
    if process.returncode != 0:
        raise Exception("'MAKE INSTALL' finished with status-code " + process.returncode)
        sys.exit(1)
    TemporaryDir.leave()


def set_vcxproj_runtime_library(path_to_vcxproj, runtime_library):
    """
    Change runtime library of vcxproj file
    :param path_to_vcxproj: Path to vcxproj
    :param runtime_library: (MT, MD)
    :return:
    """
    if runtime_library not in ('MT', 'MD'):
        raise Exception("Invalid runtime library")
        sys.exit(1)
    project = Builder(path_to_vcxproj)
    debug_conf = project.get_configuration("Debug")
    debug_runtime_library = Builder.runtimeLibraries[runtime_library + "d"]
    debug_conf.set_runtime_library(debug_runtime_library)
    debug_conf.save()

    release_runtime_library = Builder.runtimeLibraries[runtime_library]
    release_conf = project.get_configuration("Release")
    release_conf.set_runtime_library(release_runtime_library)
    release_conf.save()


def set_vcxproj_platform_toolset(path_to_vcxproj, platform_toolset):
    """
    Change platform toolset of vcxproj file
    :param path_to_vcxproj: Path to vcxproj
    :param platform_toolset: Platform toolset
    :return:
    """
    project = Builder(path_to_vcxproj)
    debug_conf = project.get_all_configurations()
    debug_conf.set_platform_toolset(platform_toolset)
    debug_conf.save()


def install_distro_dependencies(dependencies):
    distro = platform.dist()[0]
    package_manager = {"Ubuntu": 'apt-get'}
    command = 'gksudo -S "{tool} install -y ' + " ".join(dependencies) + '"'
    command = command.format(tool=package_manager[distro])
    with open('install_deps.log', 'w+') as log:
        dep_process = subprocess.Popen(command, shell=True, stderr=log, stdout=log)
        dep_process.communicate()
import os
import subprocess
import re
import config
from core.Tasks import net, archives
from core.Tasks import check_dependencies, fs, cmake, assembly, vcs
from core.Tasks.fs import require_full_path
from core.TemporaryDir import TemporaryDir
from core.common_defs import is_windows
from config import directories
from core.default_structures import cleanup_extensions
import core.sys_config as s_config


build_directory = os.path.abspath(os.path.join(directories['buildDir'], 'v8'))
v8_dir = os.path.join(build_directory, 'v8')
v8_python_path = os.path.join(build_directory, 'python276_bin{}python.exe'.format(os.path.sep))
# lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(v8_dir, 'include')


def make_v8(architecture, logs_dir):
    with open(os.path.join(logs_dir, 'gen_solution.log'), 'a+') as log_file:
        TemporaryDir.enter(v8_dir)
        if is_windows():
            subprocess.call([v8_python_path, 'build{}gyp_v8'.format(os.path.sep), '-Dtarget_arch=' + architecture,
                             '-Dcomponent=shared_library'], stderr=log_file, stdout=log_file, shell=True)
            build_dir = os.path.join(build_directory, 'x64' if architecture == 'x64' else 'x86')
            assembly.build_vcxproj(os.path.join(v8_dir, 'tools', 'gyp', 'v8.vcxproj'), build_dir)
        TemporaryDir.leave()


def fetch_v8(version, logs_dir):
    vcs.git_clone('https://chromium.googlesource.com/chromium/tools/depot_tools.git', build_directory, True)
    TemporaryDir.enter(build_directory)
    with open(os.path.join(logs_dir, 'fetch_v8.log'), 'a+') as log_file:
        print('Fetching v8')
        subprocess.call(['fetch', 'v8'], stderr=log_file, stdout=log_file, shell=True)
        print('Synchronizing')
        subprocess.call(['gclient', 'sync'], stderr=log_file, stdout=log_file, shell=True)
    TemporaryDir.leave()
    vcs.git_checkout(v8_dir, version)


def build(module_params):
    os.environ['PATH'] += ';' + build_directory
    print(build_directory)
    logs_dir = os.path.join(os.getcwd(), s_config.log_folder)
    require_full_path(logs_dir)
    check_dependencies(False, ['version'], module_params)
    version = module_params['version']
    fs.remove(build_directory)
    fetch_v8(version, logs_dir)
    print('Building v8 x64')
    make_v8('x64', logs_dir)
    print('Building v8 x86')
    make_v8('ia32', logs_dir)
    fs.clear(build_directory, cleanup_extensions['obj_files'], )

# TODO: Integration tasks
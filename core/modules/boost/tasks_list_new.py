import os
import subprocess
from core.Tasks.fs import require_full_path
import core.sys_config as s_config
from core.TemporaryDir import TemporaryDir
from core.Tasks import check_dependencies, fs, net, archives, assembly, cmake
from config import directories
from core.common_defs import set_system_variable
from core.default_structures import cleanup_extensions


origin_dir = 'Origin'
boost_url = 'http://sourceforge.net/projects/boost/files/boost/{0}/boost_{1}.7z/download'
build_directory = os.path.abspath(os.path.join(directories['buildDir'], 'boost'))
# logs_dir = logs_dir = os.path.join(build_directory, os.path.abspath(s_config.log_folder))
boost_archive = 'boost.7z'
lib_directory = os.path.join(build_directory, 'lib')
lib_directory_x86 = os.path.join(build_directory, 'stage', 'lib_x86')
lib_directory_x64 = os.path.join(build_directory, 'stage', 'lib_x64')
headers_dir = os.path.join(build_directory, 'include')

def build(module_params):
    check_dependencies(False, ['version'], module_params)
    version = module_params['version']
    # fs.remove(origin_dir)
    # net.download_file(boost_url.format(version, str(version).replace('.', '_')), boost_archive)
    # archives.extract_7_zip(boost_archive, os.getcwd())
    # fs.rename(os.path.join('boost_*'), origin_dir, True)
    set_system_variable('BOOST_ROOT', origin_dir)
    set_system_variable('BOOST_HOME', origin_dir)

    bootstrap_exec = 'bootstrap'
    b2_exec = 'b2'
    logs_dir = os.path.join(os.getcwd(), s_config.log_folder)
    require_full_path(logs_dir)
    with open(os.path.join(logs_dir, 'build_boost.log'), 'a+') as log_file:
        TemporaryDir.enter(origin_dir)
        subprocess.call([bootstrap_exec], stdout=log_file, stderr=log_file, shell=True)
        # x86
        subprocess.call([b2_exec, '--libdir={}'.format(lib_directory), '--includedir={}'.format(headers_dir),
                         '--address-model=32', '--stagedir={}'.format(lib_directory_x86), '--build-type=complete',
                         '--link=static'], stdout=log_file, stderr=log_file, shell=True)

        subprocess.call([b2_exec, '--libdir={}'.format(lib_directory), '--includedir={}'.format(headers_dir),
                         '--address-model=64', '--stagedir={}'.format(lib_directory_x64), '--build-type=complete',
                         '--link=static'], stdout=log_file, stderr=log_file, shell=True)

        TemporaryDir.leave()

    # fs.remove(boost_archive)
    # fs.clear(build_directory, cleanup_extensions['obj_files'],)


def integration(module_params):
    cmake.add_location(headers_dir)
    cmake.add_libs_directory(('windows', 'x86', 'release'), lib_directory)
    cmake.add_libs_directory(('windows', 'x86', 'debug'), lib_directory)
    cmake.add_libs_directory(('windows', 'x64', 'release'), lib_directory)
    cmake.add_libs_directory(('windows', 'x64', 'debug'), lib_directory)


import os
import subprocess
from core.Tasks.fs import require_full_path
import core.sys_config as s_config
from core.TemporaryDir import TemporaryDir
from core.Tasks import check_dependencies, fs, net, archives, assembly, cmake
from config import directories
from core.common_defs import set_system_variable
from core.default_structures import cleanup_extensions


origin_dir = os.path.abspath('Origin')
boost_url = 'http://sourceforge.net/projects/boost/files/boost/{0}/boost_{1}.7z/download'
build_directory = os.path.abspath(os.path.join(directories['buildDir'], 'boost'))
# logs_dir = logs_dir = os.path.join(build_directory, os.path.abspath(s_config.log_folder))
boost_archive = 'boost.7z'
lib_directory = os.path.join(build_directory, 'stage', 'lib')
headers_dir = build_directory


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    version = module_params['version']
    fs.remove(build_directory)
    net.download_file(boost_url.format(version, str(version).replace('.', '_')), boost_archive)
    archives.extract_7_zip(boost_archive, origin_dir)
    fs.rename(os.path.join(origin_dir, 'boost_*'), build_directory, False)
    set_system_variable('BOOST_ROOT', build_directory)
    set_system_variable('BOOST_HOME', build_directory)

    TemporaryDir.enter(build_directory)
    bootstrap_exec = 'bootstrap'
    b2_exec = 'b2'
    logs_dir = os.path.join(os.getcwd(), s_config.log_folder)
    require_full_path(logs_dir)
    with open(os.path.join(logs_dir, 'build_boost.log'), 'a+') as log_file:
        subprocess.call([bootstrap_exec], stdout=log_file, stderr=log_file, shell=True)
        subprocess.call([b2_exec], stdout=log_file, stderr=log_file, shell=True)

    TemporaryDir.leave()

    fs.remove(boost_archive)
    fs.clear(build_directory, cleanup_extensions['obj_files'],)


def integration(module_params):
    cmake.add_location(headers_dir)
    cmake.add_libs_directory(False, lib_directory)

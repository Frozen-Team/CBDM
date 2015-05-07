import os
import subprocess
from core.TemporaryDir import TemporaryDir
from core.Tasks import check_dependencies, fs, net, archives, assembly, cmake
from config import directories
from core.common_defs import set_system_variable
from core.default_structures import cleanup_extensions


origin_dir = os.path.abspath('Origin')
boost_url = 'http://sourceforge.net/projects/boost/files/boost/{0}/boost_{1}.7z/download'
build_directory = os.path.abspath(os.path.join(directories['buildDir'], 'boost'))
boost_archive = 'boost.7z'
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'include')


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    version = module_params['version']
    fs.remove(build_directory)
    net.download_file(boost_url.format(version, str(version).replace('.', '_')), boost_archive)
    archives.extract_7_zip(boost_archive, origin_dir)
    fs.rename(os.path.join(origin_dir, 'boost_*'), os.path.join(directories['buildDir'], 'boost'), False)
    set_system_variable('BOOST_ROOT', build_directory)

    TemporaryDir.enter(build_directory)
    bootstrap_exec = 'bootstrap'
    b2_exec = 'b2'

    with open(os.path.join(origin_dir, 'build_boost.log'), 'w+') as log_file:
        subprocess.call([bootstrap_exec], stdout=log_file, stderr=log_file, shell=True)
        subprocess.call([b2_exec], stdout=log_file, stderr=log_file, shell=True)

    TemporaryDir.leave()

    fs.remove(boost_archive)
    fs.clear(build_directory, cleanup_extensions['obj_files'],)


def integration(module_params):
    cmake.add_location(headers_dir)
import os

from config import directories
from core.common_defs import is_windows
from core.default_structures import cleanup_extensions
from core.Tasks import check_dependencies, fs, net, archives, cmake, assembly


origin_dir = 'Origin'
archive_path = 'glew.zip'
build_directory = os.path.join(directories['buildDir'], 'glew')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'include')
main_vcxproj = os.path.join(origin_dir, 'build', 'vc12', 'glew_static.vcxproj')


def build(module_params):
    check_dependencies(False, 'version')

    glew_url = 'https://sourceforge.net/projects/glew/files/glew/{0}/glew-{0}.zip/download'.format(
        module_params['version'])
    net.download_file(glew_url, archive_path)

    archives.extract_zip(archive_path)
    fs.remove(archive_path)
    fs.rename('glew-*', origin_dir, True)
    if is_windows():
        assembly.set_vcxproj_platform_toolset(main_vcxproj, 'vc120')
        assembly.set_vcxproj_runtime_library('MD')
        assembly.build_vcxproj(main_vcxproj, lib_directory)

    fs.rename(os.path.join(origin_dir, 'include'), headers_dir, True)
    fs.clear(origin_dir, cleanup_extensions['c++'])


def integration(module_params):
    cmake.add_location(headers_dir)

    # x86
    cmake.add_library(('windows', 'x86', 'release'),
                      os.path.join(build_directory + '/Release/Win32/glew32s.lib'))
    cmake.add_library(('windows', 'x86', 'debug'),
                      os.path.join(build_directory + '/Debug/Win32/glew32sd.lib'))
    # x64
    cmake.add_library(('windows', 'x64', 'release'),
                      os.path.join(build_directory + '/Release/x64/glew32s.lib'))
    cmake.add_library(('windows', 'x64', 'debug'),
                      os.path.join(build_directory + '/Debug/x64/glew32sd.lib'))


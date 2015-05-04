import os

from config import directories
from core.common_defs import is_windows
from core.default_structures import cleanup_extensions
from core.Tasks import check_dependencies, fs, net, archives, assembly, cmake, require_module
from core.tools.cmake import Cmake

origin_dir = 'Origin'
archive_path = os.path.join(directories['downloadDir'], 'sqlite.zip')
build_directory = os.path.join(directories['buildDir'], 'sqlite')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'include')


def create_and_run_cmake_file(sources_dir, arch):
    cmake_file = Cmake(sources_dir, 'library')
    cmake_file.set_project_name('sqlite_' + arch)
    cmake_file.set_build_dir(os.path.join(sources_dir, 'sqlite_' + arch))
    cmake_file.set_architecture(arch)
    cmake_file.save()
    cmake_file.run()


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    fs.remove(origin_dir)
    sqlite_url = 'http://www.sqlite.org/2015/sqlite-amalgamation-{0}.zip'.format(module_params['version'])
    net.download_file(sqlite_url, archive_path)
    archives.extract_zip(archive_path)
    fs.remove(archive_path)
    fs.rename('sqlite-amalgamation*', origin_dir, True)
    create_and_run_cmake_file(origin_dir, 'x86')
    create_and_run_cmake_file(origin_dir, 'x64')
    if is_windows():
        assembly.build_vcxproj(os.path.join(origin_dir, 'sqlite_x86', 'sqlite_x86.vcxproj'), False, ('Debug', 'Release'))
        assembly.build_vcxproj(os.path.join(origin_dir, 'sqlite_x64', 'sqlite_x64.vcxproj'), False, ('Debug', 'Release'))

    fs.move_files_to_dir_by_mask(os.path.join(origin_dir, '*.h'), headers_dir, True)
    fs.clear(origin_dir, cleanup_extensions['c++'])
    fs.clear(directories['downloadDir'], cleanup_extensions['c++'])


def integration(module_params):
    cmake.add_location(headers_dir)

    # x86
    cmake.add_library(('windows', 'x86', 'release'),
                      os.path.join(lib_directory + '/Release/Win32/glew32s.lib'))
    cmake.add_library(('windows', 'x86', 'debug'),
                      os.path.join(lib_directory + '/Debug/Win32/glew32sd.lib'))
    # x64
    cmake.add_library(('windows', 'x64', 'release'),
                      os.path.join(lib_directory + '/Release/x64/glew32s.lib'))
    cmake.add_library(('windows', 'x64', 'debug'),
                      os.path.join(lib_directory + '/Debug/x64/glew32sd.lib'))

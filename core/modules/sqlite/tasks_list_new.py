import os

from core.Tasks import check_dependencies, fs, net, archives, cmake
from core.tools.cmake import Cmake
import config

origin_dir = 'Origin'
archive_path = 'sqlite.zip'
third_party_dir = os.path.join(config.directories['solution_third_party_dir'], 'sqlite')
headers_dir = os.path.join(third_party_dir, 'include')


def create_cmake_file(sources_dir, lib_type):
    cmake_file = Cmake(sources_dir, 'library')
    builder = cmake_file.builder
    builder.cmake_version(config.cmakeVersion)
    builder.set_project_name('sqlite')
    builder.add_library('sqlite', ['sqlite3.c'], lib_type=str(lib_type).upper())
    builder.set_library_output_dir('build')
    cmake_file.save()


def build(module_params):
    check_dependencies(False, ['version', 'type'], module_params)

    if module_params['type'] not in ['shared', 'static']:
        raise Exception('SQLITE PARAM TYPE SHOULD BE "shared"/"static"')

    fs.remove(origin_dir)
    sqlite_url = 'http://www.sqlite.org/2015/sqlite-amalgamation-{0}.zip'.format(module_params['version'])
    net.download_file(sqlite_url, archive_path)
    archives.extract_zip(archive_path)
    fs.remove(archive_path)
    fs.rename('sqlite-amalgamation*', origin_dir, True)

    create_cmake_file(origin_dir, module_params['type'])




def integration(module_params):
    fs.copy(origin_dir, third_party_dir, True)
    cmake.add_location(third_party_dir)
    cmake.add_subdir(third_party_dir)
    for system in ['linux', 'windows']:
        for arch in ['x64', 'x86']:
            for conf in ['debug', 'release']:
                cmake.add_library((system, arch, conf), 'sqlite')
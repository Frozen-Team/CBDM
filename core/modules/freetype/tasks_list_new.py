import os
from config import directories
from core.Tasks import check_dependencies, fs, net, archives, cmake, assembly
from core.common_defs import is_windows
from core.default_structures import cleanup_extensions

origin_dir = 'origin'
download_dir = 'Download'
path_tar_gz = os.path.join(download_dir, 'freetype.tar.gz')
path_tar = os.path.join(download_dir, 'freetype.tar')
vcxproj_file = "Lib/freetype-{version}/builds/windows/vc2010/freetype.vcxproj"

build_directory = os.path.join(directories['buildDir'], 'freetype')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'include')


def build(module_params):
    check_dependencies(False, ['version'])
    freetype_url = "http://download.savannah.gnu.org/releases/freetype/freetype-{}.tar.gz".format(
        module_params['version'])
    net.download_file(freetype_url, path_tar_gz)
    archives.extract_7_zip(path_tar_gz, download_dir)
    archives.extract_7_zip(path_tar)
    fs.rename('freetype-*', origin_dir, True)
    fs.remove(download_dir)

    if is_windows():
        assembly.set_vcxproj_platform_toolset(vcxproj_file, 'vc120')
        assembly.set_vcxproj_runtime_library(vcxproj_file, 'MD')
        assembly.build_vcxproj(vcxproj_file, build_directory)

    fs.rename(os.path.join(origin_dir, 'include'), headers_dir)
    fs.clear(origin_dir, cleanup_extensions['c++'])


def integration(module_params):
    cmake.add_location(headers_dir)

    # x86
    # TODO: Add {labels} to integration tasks, freetype255.lib -> freetype{version_simple}.lib, to description too.
    cmake.add_library(('windows', 'x86', 'release'),
                      os.path.join(lib_directory, 'Release', 'Win32', 'freetype255.lib'))
    cmake.add_library(('windows', 'x86', 'debug'), os.path.join(lib_directory, 'Debug', 'Win32', 'freetype255d.lib'))
    # x64
    cmake.add_library(('windows', 'x64', 'release'), os.path.join(lib_directory, 'Release', 'x64', 'freetype255.lib'))
    cmake.add_library(('windows', 'x64', 'debug'), os.path.join(lib_directory, 'Debug', 'x64', 'freetype255d.lib'))

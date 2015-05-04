import os

from config import directories
from core.Tasks import check_dependencies, fs, net, archives, cmake
from core.common_defs import is_windows, is_linux


origin_dir = 'Origin'

exe_path = 'fbxsdk.exe'
build_directory = os.path.join(directories['buildDir'], 'fbxsdk')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'headers')


def build(module_params):
    # TODO: Looks like windows is working, promlems with linux version (extact .so from binary)
    check_dependencies(False, ['version'], module_params)

    fs.remove(origin_dir)

    if is_windows():
        net.download_file('http://images.autodesk.com/adsk/files/fbx{version}_fbxsdk_vs2013_win.exe'.format(
            version=module_params['version']), exe_path)
        archives.extract_7_zip(exe_path, origin_dir)
    elif is_linux():
        net.download_file('http://images.autodesk.com/adsk/files/fbx{version}_fbxsdk_linux.tar.gz'.format(
            version=module_params['version']), 'origin.tar.gz')
        archives.extract_tar('origin.tar.gz', origin_dir)

    fs.rename(os.path.join(origin_dir, 'include'), headers_dir, True)
    fs.rename(os.path.join(origin_dir, 'lib', 'vs2013'), lib_directory, True)
    fs.remove(origin_dir)
    fs.remove(exe_path)


def integration(module_params):
    cmake.add_location(headers_dir)
    # x86
    cmake.add_library(('windows', 'x86', 'release'),
                              os.path.join(lib_directory, 'x86', 'release', 'libfbxsdk.lib'))
    cmake.add_library(('windows', 'x86', 'release'), os.path.join(lib_directory, 'x86', 'release', 'libfbxsdk-md.lib'))

    cmake.add_library(('windows', 'x86', 'debug'), os.path.join(lib_directory, 'x86', 'debug', 'libfbxsdk.lib'));
    cmake.add_library(('windows', 'x86', 'debug'), os.path.join(lib_directory, 'x86', 'debug', 'libfbxsdk-md.lib'))

    # x64
    cmake.add_library(('windows', 'x64', 'release'), os.path.join(lib_directory, 'x64', 'release', 'libfbxsdk.lib'))
    cmake.add_library(('windows', 'x64', 'release'), os.path.join(lib_directory, 'x64', 'release', 'libfbxsdk-md.lib'))

    cmake.add_library(('windows', 'x64', 'debug'), os.path.join(lib_directory, 'x64', 'debug', 'libfbxsdk.lib'))
    cmake.add_library(('windows', 'x64', 'debug'), os.path.join(lib_directory, 'x64', 'debug', 'libfbxsdk-md.lib'))

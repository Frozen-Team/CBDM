import os
from config import directories
from core.Tasks import net, archives, fs, cmake, check_dependencies
from core.common_defs import is_windows, is_linux

origin_dir = 'Origin'
fmod_path = 'fmod.exe'

build_dir = os.path.join(directories["buildDir"], 'fmod')


def build(module_params):
    check_dependencies((), ['version'], module_params)
    version = module_params['version']
    if is_windows():
        url_to_installer = "http://www.fmod.org/download/fmodstudio/api/Win/fmodstudioapi{}win-installer.exe".format(
            version)
        net.download_file(url_to_installer, fmod_path)
        archives.extract_7_zip(fmod_path, origin_dir)
    elif is_linux():
        url_to_installer = "http://www.fmod.org/download/fmodstudio/api/Linux/fmodstudioapi{}linux.tar.gz".format(
            version)
        # net.download_file(url_to_installer, fmod_path)
        archives.extract_tar(fmod_path)
        fs.rename('fmodstudioapi*', origin_dir, True)
    fs.remove(build_dir)
    fs.remove(os.path.join(origin_dir, 'api', '*', 'examples'))
    fs.rename(os.path.join(origin_dir, 'api'), build_dir, True)
    fs.remove(fmod_path)
    fs.remove(origin_dir)


def integration(module_params):
    cmake.add_location(os.path.join(build_dir, 'lowlevel', 'inc'))
    cmake.add_location(os.path.join(build_dir, 'studio', 'inc'))

    # LOWLEVEL
    if is_windows():
        add_windows_libraries()
    elif is_linux():
        add_linux_libraries()

def add_windows_libraries():
    lowlevel_lib_dir = os.path.join(build_dir, 'lowlevel', 'lib')
    studio_lib_dir = os.path.join(build_dir, 'studio', 'lib')

    # LOWLEVEL
    # x86
    cmake.add_library(('windows', 'x86', 'release'), os.path.join(lowlevel_lib_dir, 'fmod_vc.lib'))
    cmake.add_library(('windows', 'x86', 'debug'), os.path.join(lowlevel_lib_dir, 'fmodL_vc.lib'))
    # x64
    cmake.add_library(('windows', 'x64', 'release'), os.path.join(lowlevel_lib_dir, 'fmod64_vc.lib'))
    cmake.add_library(('windows', 'x64', 'debug'), os.path.join(lowlevel_lib_dir, 'fmodL64_vc.lib'))

    # STUDIO
    # x86
    cmake.add_library(('windows', 'x86', 'release'), os.path.join(studio_lib_dir, 'fmodstudio_vc.lib'))
    cmake.add_library(('windows', 'x86', 'debug'), os.path.join(studio_lib_dir, 'fmodstudioL_vc.lib'))
    # x64
    cmake.add_library(('windows', 'x64', 'release'), os.path.join(studio_lib_dir, 'fmodstudio64_vc.lib'))
    cmake.add_library(('windows', 'x64', 'debug'), os.path.join(studio_lib_dir, 'fmodstudioL64_vc.lib'))


def add_linux_libraries():
    lowlevel_lib_dir = os.path.join(build_dir, 'lowlevel', 'lib')
    studio_lib_dir = os.path.join(build_dir, 'studio', 'lib')

    # LOWLEVEL
    # x86
    cmake.add_library(('linux', 'x86', 'release'), os.path.join(lowlevel_lib_dir, 'x86', 'libfmod.so'))
    cmake.add_library(('linux', 'x86', 'debug'), os.path.join(lowlevel_lib_dir, 'x86', 'libfmodL.so'))
    # x64
    cmake.add_library(('linux', 'x64', 'release'), os.path.join(lowlevel_lib_dir, 'x86_64', 'libfmod.so'))
    cmake.add_library(('linux', 'x64', 'debug'), os.path.join(lowlevel_lib_dir, 'x86_64', 'libfmodL.so'))

    # STUDIO
    # x86
    cmake.add_library(('linux', 'x86', 'release'), os.path.join(studio_lib_dir, 'x86', 'libfmodstudio.so'))
    cmake.add_library(('linux', 'x86', 'debug'), os.path.join(studio_lib_dir, 'x86', 'libfmodstudioL.so'))
    # x64
    cmake.add_library(('linux', 'x64', 'release'), os.path.join(studio_lib_dir, 'x86_64', 'libfmodstudio.so'))
    cmake.add_library(('linux', 'x64', 'debug'), os.path.join(studio_lib_dir, 'x86_64', 'libfmodstudioL.so'))
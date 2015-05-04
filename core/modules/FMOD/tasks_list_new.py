import os
from config import directories
from core.Dependencies.Tasks import check_dependencies
from core.Tasks import net, archives, fs, cmake

origin_dir = 'Origin'
fmod_path = 'fmod.exe'

build_dir = os.path.join(directories["buildDir"], 'fmod')


def build(module_params):
    check_dependencies((), ['version'], module_params)
    url_to_installer = "http://www.fmod.org/download/fmodstudio/api/Win/fmodstudioapi{}win-installer.exe".format(
        module_params['version'])
    net.download_file(url_to_installer, fmod_path)
    archives.extract_7_zip(fmod_path, origin_dir)
    fs.rename(os.path.join(origin_dir, 'api'), build_dir, True)
    fs.remove(fmod_path)
    fs.remove(origin_dir)


def integration(module_params):
    cmake.add_location(os.path.join(build_dir, 'fsbank', 'inc'))
    cmake.add_location(os.path.join(build_dir, 'lowlevel', 'inc'))
    cmake.add_location(os.path.join(build_dir, 'studio', 'inc'))

    lowlevel_lib_dir = os.path.join(build_dir, 'lowlevel', 'lib')
    studio_lib_dir = os.path.join(build_dir, 'studio', 'lib')
    fsbank_lib_dir = os.path.join(build_dir, 'fsbank', 'lib')
    # x86

    # LOWLEVEL
    cmake.add_library(('windows', 'x86', 'release'), os.path.join(lowlevel_lib_dir, 'fmod_vc.lib'))
    cmake.add_library(('windows', 'x86', 'release'), os.path.join(lowlevel_lib_dir, 'fmodL_vc.lib'))
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

    # FSBANK
    # x86
    cmake.add_library(('windows', 'x86', 'release'), os.path.join(fsbank_lib_dir, 'fsbank_vc.lib'))
    cmake.add_library(('windows', 'x86', 'debug'), os.path.join(fsbank_lib_dir, 'fsbank_vc.lib'))

    # x64
    cmake.add_library(('windows', 'x64', 'release'), os.path.join(fsbank_lib_dir, 'fsbank64_vc.lib'))
    cmake.add_library(('windows', 'x64', 'debug'), os.path.join(fsbank_lib_dir, 'fsbank64_vc.lib'))
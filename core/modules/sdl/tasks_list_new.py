import os

import config
from core import default_structures
from core.common_defs import is_windows
from core.Tasks import check_dependencies, net, archives, fs, assembly, cmake

origin_dir = 'Origin'
sdl_arch_path = 'sdl.zip'
path_to_vcxproj_SDL = os.path.join(origin_dir, 'VisualC', 'SDL', 'SDL_VS2013.vcxproj')
path_to_vcxproj_SDLmain = os.path.join(origin_dir, 'VisualC', 'SDLmain', 'SDLmain_VS2013.vcxproj')
path_to_vcxproj_SDLtest = os.path.join(origin_dir, 'VisualC', 'SDLtest', 'SDLtest_VS2013.vcxproj')
build_dir = os.path.join(config.directories['solution_third_party_dir'], 'sdl')
output_lib_dir = os.path.join(build_dir, 'lib')
output_include_dir = os.path.join(build_dir, 'include')

vcxproj_files = (path_to_vcxproj_SDL, path_to_vcxproj_SDLmain, path_to_vcxproj_SDLtest)


def build(module_params):
    check_dependencies(False, ['version', 'major_version'])
    fs.remove(origin_dir)
    fs.remove(build_dir)
    major_v = module_params['major_version']
    major_v_s = str(major_v) if major_v > 1 else ''
    file_name = 'SDL{major}-{version}'.format(major=major_v_s, version=module_params['version'])
    sdl_url = "https://www.libsdl.org/release/{file_name}.zip".format(file_name=file_name)

    net.download_file(sdl_url, sdl_arch_path)
    archives.extract_7_zip(sdl_arch_path)
    fs.remove(sdl_arch_path)
    fs.rename(file_name, origin_dir, True)
    if is_windows():
        for vcxproj_file in vcxproj_files:
            assembly.set_vcxproj_platform_toolset_and_rl(vcxproj_file, config.visual_studio_toolset,
                                                         config.visual_studio_runtime_library)
            assembly.build_vcxproj(vcxproj_file, output_lib_dir)

    path_to_headers = os.path.join(origin_dir, 'include')
    fs.copy(path_to_headers, output_include_dir, True)
    fs.clear(origin_dir, default_structures.cleanup_extensions['c++'])


def integration(module_params):
    cmake.add_location(output_include_dir)
    if is_windows():
        major_v = module_params['major_version']
        major_v_s = str(major_v) if major_v > 1 else ''
        sdl_lib_name = 'SDL' + major_v_s
        lib_names = [sdl_lib_name, sdl_lib_name+'main', sdl_lib_name+'test' ]
        for lib_name in lib_names:
            cmake.add_library(('windows', 'x64', 'debug'), os.path.join(output_lib_dir, 'Debug', 'x64', lib_name))
            cmake.add_library(('windows', 'x64', 'release'), os.path.join(output_lib_dir, 'Release', 'x64', lib_name))
            cmake.add_library(('windows', 'x86', 'debug'), os.path.join(output_lib_dir, 'Debug', 'Win32', lib_name))
            cmake.add_library(('windows', 'x86', 'release'), os.path.join(output_lib_dir, 'Release', 'Win32', lib_name))

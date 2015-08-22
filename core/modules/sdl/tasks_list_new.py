import os

import config
from core.Tasks import check_dependencies, net, archives, fs, cmake, assembly
from core.common_defs import is_windows

origin_dir = 'Origin'
archive_path = 'sdl.zip'
build_directory = os.path.join(config.directories['buildDir'], 'sdl')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'include')


def build(module_params):
    fs.remove(origin_dir)
    fs.remove(build_directory)
    check_dependencies(False, ['version', 'major_version'])
    major_v = module_params['major_version']
    major_v_s = str(major_v) if major_v > 1 else ''
    file_name = 'SDL{major}-{version}'.format(major=major_v_s, version=module_params['version'])
    sdl_url = "https://www.libsdl.org/release/{file_name}.zip".format(file_name=file_name)

    net.download_file(sdl_url, archive_path)
    archives.extract_7_zip(archive_path)
    fs.remove(archive_path)
    fs.rename(file_name, origin_dir, True)

    if is_windows():
        assembly.build_vcxproj(os.path.abspath(os.path.join(origin_dir, 'VisualC', 'SDL', 'SDL_VS2013.vcxproj')),
                               lib_directory, ('Debug', 'Release'))
        assembly.build_vcxproj(
            os.path.abspath(os.path.join(origin_dir, 'VisualC', 'SDLmain', 'SDLmain_VS2013.vcxproj')),
            lib_directory, ('Debug', 'Release'))
        assembly.build_vcxproj(
            os.path.abspath(os.path.join(origin_dir, 'VisualC', 'SDLtest', 'SDLtest_VS2013.vcxproj')),
            lib_directory, ('Debug', 'Release'))
    fs.rename(os.path.join(origin_dir, 'include'), headers_dir, True)


def integration(module_params):
    cmake.add_location(headers_dir)
    if is_windows():
        # x86
        cmake.add_library(('windows', 'x86', 'release'),
                          os.path.join(lib_directory, 'Release', 'Win32', 'SDL2.lib'))
        cmake.add_library(('windows', 'x86', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'Win32', 'SDL2.lib'))
        # x64
        cmake.add_library(('windows', 'x64', 'release'),
                          os.path.join(lib_directory, 'Release', 'x64', 'SDL2.lib'))
        cmake.add_library(('windows', 'x64', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'x64', 'SDL2.lib'))

        # x86
        cmake.add_library(('windows', 'x86', 'release'),
                          os.path.join(lib_directory, 'Release', 'Win32', 'SDL2main.lib'))
        cmake.add_library(('windows', 'x86', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'Win32', 'SDL2main.lib'))
        # x64
        cmake.add_library(('windows', 'x64', 'release'),
                          os.path.join(lib_directory, 'Release', 'x64', 'SDL2main.lib'))
        cmake.add_library(('windows', 'x64', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'x64', 'SDL2main.lib'))

        # x86
        cmake.add_library(('windows', 'x86', 'release'),
                          os.path.join(lib_directory, 'Release', 'Win32', 'SDL2test.lib'))
        cmake.add_library(('windows', 'x86', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'Win32', 'SDL2test.lib'))
        # x64
        cmake.add_library(('windows', 'x64', 'release'),
                          os.path.join(lib_directory, 'Release', 'x64', 'SDL2test.lib'))
        cmake.add_library(('windows', 'x64', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'x64', 'SDL2test.lib'))


#     cmake.add_subdir(third_party_dir, True)
#     cmake.add_location(tp_headers_dir)
#     cmake.cmake_after("""
# add_custom_command(TARGET test_project POST_BUILD
#     COMMAND ${CMAKE_COMMAND} -E copy_if_different
#         "${PROJECT_SOURCE_DIR}/3dparty/sdl/$(ConfigurationName)/SDL2.dll"
#         $<TARGET_FILE_DIR:test_project>)
#     """)
#     for system in ['linux', 'windows']:
#         for arch in ['x64', 'x86']:
#             for conf in ['debug', 'release']:
#                 cmake.add_library((system, arch, conf), 'SDL2', True)
#                 cmake.add_library((system, arch, conf), 'SDL2main', True)

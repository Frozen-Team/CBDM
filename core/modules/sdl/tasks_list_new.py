import os

import config
from core.Tasks import check_dependencies, net, archives, fs, cmake

origin_dir = 'Origin'
sdl_arch_path = 'sdl.zip'
third_party_dir = os.path.join(config.directories['solution_third_party_dir'], 'sdl')
tp_headers_dir = os.path.join(third_party_dir, 'include')


def build(module_params):
    fs.remove(origin_dir)
    fs.remove(third_party_dir)
    check_dependencies(False, ['version', 'major_version'])
    major_v = module_params['major_version']
    major_v_s = str(major_v) if major_v > 1 else ''
    file_name = 'SDL{major}-{version}'.format(major=major_v_s, version=module_params['version'])
    sdl_url = "https://www.libsdl.org/release/{file_name}.zip".format(file_name=file_name)

    net.download_file(sdl_url, sdl_arch_path)
    archives.extract_7_zip(sdl_arch_path)
    fs.remove(sdl_arch_path)
    fs.rename(file_name, origin_dir, True)


def integration(module_params):
    fs.copy(origin_dir, third_party_dir, True)
    cmake.add_subdir(third_party_dir, True)
    cmake.add_location(tp_headers_dir)
    cmake.cmake_after("""
add_custom_command(TARGET test_project POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${PROJECT_SOURCE_DIR}/3dparty/sdl/$(ConfigurationName)/SDL2.dll"
        $<TARGET_FILE_DIR:test_project>)
    """)
    for system in ['linux', 'windows']:
        for arch in ['x64', 'x86']:
            for conf in ['debug', 'release']:
                cmake.add_library((system, arch, conf), 'SDL2', True)
                cmake.add_library((system, arch, conf), 'SDL2main', True)

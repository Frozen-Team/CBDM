import os
from config import directories
from core.common_defs import is_windows
from core.default_structures import cleanup_extensions
from core.Tasks import check_dependencies, fs, vcs, cmake, assembly


origin_dir = 'Origin'
build_directory = os.path.join(directories['buildDir'], 'ozz')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'include')
vcxproj_pathes = (
    'src/animation/runtime/ozz_animation.vcxproj',
    'src/animation/offline/collada/ozz_animation_collada.vcxproj',
    'src/animation/offline/fbx/ozz_animation_fbx.vcxproj',
    'src/animation/offline/ozz_animation_offline.vcxproj',
    'src/animation/offline/tools/ozz_animation_offline_tools.vcxproj',
    'src/base/ozz_base.vcxproj',
    'src/geometry/runtime/ozz_geometry.vcxproj',
    'src/options/ozz_options.vcxproj',
)


def vcxproj_change_mult(vcxproj_to_change):
    for vcxproj_file in vcxproj_to_change:
            vcxproj_file = os.path.join(origin_dir, vcxproj_file)
            assembly.set_vcxproj_platform_toolset(vcxproj_file, 'v120')
            assembly.set_vcxproj_runtime_library(vcxproj_file, 'MD')


def add_library_list(platform, arch_type_config, build_type, arch, lib_names_list):
    for lib_path in lib_names_list:
        lib = lib_path + '_d.lib' if build_type == 'debug' else '-r.lib'
        cmake.add_library((platform, arch_type_config, build_type),
                          os.path.join(lib_directory, build_type.title(), arch,  lib))


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    fs.remove(origin_dir)
    vcs.git_clone('https://code.google.com/p/ozz-animation.git', origin_dir, True)
    cmake.run_cmake(origin_dir, 'x86', 'x86')
    vcxproj_to_change_x86 = ('x86/' + s for s in vcxproj_pathes)
    if is_windows():
        vcxproj_change_mult(vcxproj_to_change_x86)
        assembly.build_vcxproj(os.path.join(origin_dir, 'x86', 'ALL_BUILD.vcxproj'), lib_directory)

    cmake.run_cmake(origin_dir, 'x64', 'x64')
    vcxproj_to_change_x64 = ('x64/' + s for s in vcxproj_pathes)
    if is_windows():
        vcxproj_change_mult(vcxproj_to_change_x64)
        assembly.build_vcxproj(os.path.join(origin_dir, 'x64', 'ALL_BUILD.vcxproj'), lib_directory)

    # TODO: copy
    fs.rename(os.path.join(origin_dir, 'include'), headers_dir, True)
    fs.clear(headers_dir, False, ['.h'])
    fs.clear(origin_dir, cleanup_extensions['c++'])


def integration(module_params):
    cmake.add_location(headers_dir)
    if is_windows():
        lib_list = (
            'ozz_animation',
            'ozz_animation_collada',
            'ozz_animation_fbx',
            'ozz_animation_offline',
            'ozz_animation_offline_tools',
            'ozz_base',
            'ozz_geometry',
            'ozz_options',
        )

        # x86
        add_library_list('windows', 'x86', 'release', 'Win32', lib_list)
        add_library_list('windows', 'x86', 'debug', 'Win32', lib_list)

        # x64
        add_library_list('windows', 'x64', 'release', 'x64', lib_list)
        add_library_list('windows', 'x64', 'debug', 'x64', lib_list)

import os
import config
from config import directories
from core.common_defs import is_windows
from core.default_structures import cleanup_extensions
from core.Tasks import check_dependencies, fs, cmake, assembly, vcs


origin_dir = 'Origin'
archive_path = 'glfw.zip'
build_directory = os.path.join(directories['buildDir'], 'glfw')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'include')
glfw_vcxproj_x86 = os.path.join(origin_dir, 'x86', 'src', 'glfw.vcxproj')
glfw_vcxproj_x64 = os.path.join(origin_dir, 'x64', 'src', 'glfw.vcxproj')


def build_arch(arch):
    cmake.run_cmake(origin_dir, arch, arch)
    vcxproj_path = os.path.join(origin_dir, arch, 'src', 'glfw.vcxproj')
    if is_windows():
        assembly.set_vcxproj_platform_toolset(vcxproj_path, config.visual_studio_toolset)
        assembly.set_vcxproj_runtime_library(vcxproj_path, config.visual_studio_runtime_library)
        assembly.build_vcxproj(vcxproj_path, lib_directory)


def build(module_params):
    fs.remove(origin_dir)
    check_dependencies(False, ['version'], module_params)
    vcs.git_clone('https://github.com/glfw/glfw.git', origin_dir)
    vcs.git_checkout(origin_dir, module_params['version'])

    build_arch('x86')
    build_arch('x64')

    fs.rename(os.path.join(origin_dir, 'include'), headers_dir, True)
    fs.clear(origin_dir, cleanup_extensions['c++'])


def integration(module_params):
    cmake.add_location(headers_dir)
    if is_windows():
        # x86
        cmake.add_library(('windows', 'x86', 'release'),
                          os.path.join(lib_directory, 'Release', 'Win32', 'glfw3.lib'))
        cmake.add_library(('windows', 'x86', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'Win32', 'glfw3.lib'))
        # x64
        cmake.add_library(('windows', 'x64', 'release'),
                          os.path.join(lib_directory, 'Release', 'x64', 'glfw3.lib'))
        cmake.add_library(('windows', 'x64', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'x64', 'glfw3.lib'))

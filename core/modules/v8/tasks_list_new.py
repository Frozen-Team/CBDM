import os
import subprocess
import sys
from core.Tasks import check_dependencies, fs, assembly, vcs
from core.Tasks.fs import require_full_path
from core.TemporaryDir import TemporaryDir
from core.common_defs import is_windows
from config import directories
from core.default_structures import cleanup_extensions
import core.sys_config as s_config
from core.tools import cmake

origin_dir = 'Origin'
build_directory = os.path.abspath(os.path.join(directories['buildDir'], 'v8'))
v8_dir = os.path.join(origin_dir, 'v8')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(v8_dir, 'include')


def make_v8(architecture, logs_dir):
    with open(os.path.join(logs_dir, 'gen_solution.log'), 'a+') as log_file:
        if is_windows():
            v8_python_path = os.path.abspath(os.path.join(origin_dir, 'python276_bin{}python.exe'.format(os.path.sep)))
            print(v8_python_path)
            TemporaryDir.enter(v8_dir)
            subprocess.call([v8_python_path, 'build{}gyp_v8'.format(os.path.sep), '-Dtarget_arch=' + architecture,
                             '-Dcomponent=static_library'], stderr=log_file, stdout=log_file, shell=True)

            # TODO: modify MT MTd flags if necessary
            vcxproj_to_change = ('third_party/icu/icui18n.vcxproj',
                                 'third_party/icu/icuuc.vcxproj',
                                 'tools/gyp/mksnapshot.vcxproj',
                                 'tools/gyp/v8_base_0.vcxproj',
                                 'tools/gyp/v8_base_1.vcxproj',
                                 'tools/gyp/v8_base_2.vcxproj',
                                 'tools/gyp/v8_base_0.vcxproj',
                                 'tools/gyp/v8_libbase.vcxproj',
                                 'tools/gyp/v8_libplatform.vcxproj',
                                 'tools/gyp/v8_nosnapshot.vcxproj',
                                 'tools/gyp/v8_snapshot.vcxproj'
                                 )
            # for vcxproj_file in vcxproj_to_change:
            #     vcxproj_file = os.path.join(v8_dir, vcxproj_file)
            #     assembly.set_vcxproj_platform_toolset(vcxproj_file, config.visual_studio_toolset)
            #     assembly.set_vcxproj_runtime_library(vcxproj_file, config.visual_studio_runtime_library)

            # assembly.build_vcxproj(os.path.join(v8_dir, 'tools', 'gyp', 'v8.vcxproj'))
            TemporaryDir.leave()
            assembly.build_vcxproj(os.path.join(v8_dir, 'tools', 'gyp', 'v8.vcxproj'), lib_directory)


def fetch_v8(version, logs_dir):
    vcs.git_clone('https://chromium.googlesource.com/chromium/tools/depot_tools.git', origin_dir, True)
    TemporaryDir.enter(origin_dir)
    with open(os.path.join(logs_dir, 'fetch_v8.log'), 'a+') as log_file:
        print('Fetching v8')
        subprocess.call(['fetch', 'v8'], stderr=log_file, stdout=log_file, shell=True)
        print('Synchronizing')
        subprocess.call(['gclient', 'sync'], stderr=log_file, stdout=log_file, shell=True)
    TemporaryDir.leave()
    vcs.git_checkout(v8_dir, version)


def build(module_params):
    sys.path.append(os.path.abspath(origin_dir))
    logs_dir = os.path.abspath(s_config.log_folder)
    fs.remove(logs_dir)
    require_full_path(logs_dir)
    check_dependencies(False, ['version'], module_params)
    version = module_params['version']
    fs.remove(origin_dir)
    fetch_v8(version, logs_dir)
    print('Building v8 x64')
    make_v8('x64', logs_dir)
    print('Building v8 x86')
    make_v8('ia32', logs_dir)
    fs.rename(os.path.join(origin_dir, 'v8', 'include'), headers_dir, True)
    fs.clear(origin_dir, cleanup_extensions['c++'], )


def integration(module_params):
    cmake.add_location(headers_dir)
    if is_windows():
        # x86
        cmake.add_library(('windows', 'x86', 'release'),
                          os.path.join(lib_directory, 'Release', 'Win32', 'lib', 'TODO'))
        cmake.add_library(('windows', 'x86', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'Win32', 'lib', 'TODO'))
        # x64
        cmake.add_library(('windows', 'x64', 'release'),
                          os.path.join(lib_directory, 'Release', 'x64', 'lib', 'TODO'))
        cmake.add_library(('windows', 'x64', 'debug'),
                          os.path.join(lib_directory, 'Debug', 'x64', 'lib', 'TODO'))
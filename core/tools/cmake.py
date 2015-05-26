import os
import glob
import subprocess

import config
from core import sys_config
from core.Dependencies.library_module import LibraryModule
from core.Tasks import fs
from core.TemporaryDir import TemporaryDir

cmake_program = ''


class CmakeBuilder:
    def __init__(self, project_dir, project_name=False):
        self.result = ''
        self.project_dir = os.path.abspath(project_dir)
        self.create_project_path()
        if bool(project_name):
            self.set_project_name(project_name)

    def set_runtime_output_dir(self, directory):
        add_str = 'SET( RUNTIME_OUTPUT_DIRECTORY {} )'.format(directory)
        self.result += add_str
        self.new_line()

    def set_library_output_dir(self, directory):
        add_str = 'SET( LIBRARY_OUTPUT_PATH {} )'.format(directory)
        self.result += add_str
        self.new_line()

    def create_project_path(self):
        if not os.path.isdir(self.project_dir):
            os.mkdir(self.project_dir)

    def include_directories(self, directory):
        rel_dir = os.path.relpath(directory, self.project_dir).replace('\\', '/')
        add_str = 'INCLUDE_DIRECTORIES ({})'.format(rel_dir)
        self.result += add_str
        self.new_line()

    # Cmake version
    def cmake_version(self, version):
        add_str = 'CMAKE_MINIMUM_REQUIRED(VERSION {v})'.format(v=version)
        self.result += add_str
        self.new_line()

    def add_subdirectory(self, path):
        rel_dir = os.path.relpath(path, self.project_dir).replace('\\', '/')
        add_str = 'ADD_SUBDIRECTORY({path})'.format(path=rel_dir)
        self.result += add_str
        self.new_line()

    def set_project_name(self, project_name):
        self.result += 'project({name})'.format(name=project_name)
        self.new_line()

    def add_executable(self, target_name, files_masks):
        executable_files = self.find_files_by_masks(files_masks)
        executable_files = ' '.join(executable_files)
        self.result += 'ADD_EXECUTABLE({name} {files})'.format(name=target_name, files=executable_files)
        self.new_line()

    def add_library(self, target_name, files_masks, abs_paths=False, lib_type='STATIC'):
        library_files = ' '.join(self.find_files_by_masks(files_masks, abs_paths))
        add_str = 'ADD_LIBRARY({name} {type} {paths})'
        add_str = add_str.format(name=target_name, type=lib_type, paths=library_files)
        self.result += add_str
        self.new_line()

    def find_files_by_masks(self, masks, abs_paths=False):
        result = []
        TemporaryDir.enter(self.project_dir)

        def make_abs_paths(paths):
            return [os.path.abspath(path) for path in paths]

        def find_files_by_mask(search_mask):
            files = glob.glob(search_mask)
            if abs_paths:
                files = make_abs_paths(files)
            return files

        if isinstance(masks, list):
            for mask in masks:
                result.extend(find_files_by_mask(mask))

        elif isinstance(masks, str):
            result.extend(find_files_by_mask(masks))

        TemporaryDir.leave()
        return result

    def new_line(self):
        self.result += os.linesep

    def link_library(self, target_name, lib_name, modificator='', is_libname=False):
        if is_libname:
            path = lib_name
        else:
            path = os.path.relpath(lib_name, self.project_dir).replace('\\', '/')
        add_str = 'TARGET_LINK_LIBRARIES({project} {mod} {path})'
        link_str = add_str.format(project=target_name, mod=modificator, path=path)
        self.result += link_str
        self.new_line()

    def link_dir(self, directory):
        rel_dir = os.path.relpath(directory, self.project_dir).replace('\\', '/')
        self.result += 'LINK_DIRECTORIES({path})'.format(path=rel_dir)
        self.new_line()

    def get_result(self):
        return self.result

    def write(self, code):
        self.result += str(code)
        self.new_line()


class Cmake:
    cmake_built = False
    cmake_path = ''

    def __init__(self, project_directory, project_type='executable'):
        self.builder = CmakeBuilder(project_directory)
        self.cmake_path = Cmake.install_cmake()
        self._sourcesDir = project_directory
        self._buildDir = config.directories["buildDir"]
        self._cmakeVersion = config.cmakeVersion
        self._additionalFlags = {}
        self.project_name = config.projectName
        project_type = 'executable' if project_type not in ['executable', 'library'] else project_type
        self.project_type = project_type
        self.generator_name = config.cmakeGenerator
        self.architecture = config.buildArchitecture
        self.build_directory = ''
        self.project_extensions = ['cpp', 'h']

    def set_project_extensions(self, extensions):
        self.project_extensions = extensions

    def add_project_extension(self, extension):
        self.project_extensions.append(extension)

    def set_build_dir(self, directory):
        self.build_directory = directory

    @staticmethod
    def install_cmake():
        if not Cmake.cmake_built:
            install_module = LibraryModule('cmake', {'rebuild': False, 'version': config.cmakeVersion})
            install_module.prepare()
            Cmake.cmake_built = True
            Cmake.cmake_path = install_module.write_results()['path']
        return Cmake.cmake_path

    def set_flag(self, flag_name, flag_value):
        self._additionalFlags[flag_name] = flag_value

    def get_customs_flags_string(self):
        format_flag = lambda f_name, f_val: "-{0} {1}".format(f_name, f_val)
        return " ".join([format_flag(flag, value) for flag, value in self._additionalFlags.items()])

    def set_generator_name(self, generator_name):
        self.generator_name = generator_name

    def set_architecture(self, arch):
        self.architecture = arch

    def get_generator_name(self):
        if not self.generator_name.startswith('Visual'):
            return self.generator_name
        gen_arch = ' Win64' if self.architecture == 'x64' else ''
        return self.generator_name + gen_arch

    def save(self):
        with open(self._sourcesDir + '/CMakeLists.txt', 'w+') as cmake_file:
            cmake_file.writelines(self.builder.get_result())

    def get_exec_flags(self):
        build_dir_flag = '-B"{}"'.format(self.build_directory) if bool(self.build_directory) else ''
        generator_flag = '-G"{}"'.format(self.get_generator_name())
        sources_dir_flag = '-H"./"'
        custom_flags = self.get_customs_flags_string()
        return [generator_flag, build_dir_flag, custom_flags, sources_dir_flag]

    def remove_cache(self):
        TemporaryDir.enter(self._sourcesDir)
        if os.path.isfile('CMakeCache.txt'):
            os.remove('CMakeCache.txt')
        TemporaryDir.leave()

    def run(self):
        log_filename = os.path.join(sys_config.log_folder, 'cmake.log')
        fs.create_path_to(log_filename)
        with open(log_filename, "a+") as cmake_log:
            TemporaryDir.enter(self._sourcesDir)
            self.remove_cache()
            command = [self.cmake_path]
            command.extend(self.get_exec_flags())
            if bool(self.build_directory):
                os.makedirs(self.build_directory)

            process = subprocess.Popen(" ".join(command), stdin=subprocess.PIPE, shell=True, stderr=cmake_log,
                                       stdout=cmake_log)

            process.communicate()
            if process.returncode:
                raise Exception('"CMAKE RUN" finished with result code ' + str(process.returncode))
                sys.exit(1)
            TemporaryDir.leave()

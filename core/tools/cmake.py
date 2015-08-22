import os
import glob
import subprocess
import config

from core import sys_config
from core.dependencies.library_module import LibraryModule
from core.tasks import fs
from core.tasks.fs import require_full_path
from core.TemporaryDir import TemporaryDir

cmake_program = ''


class CmakeBuilder:
    def __init__(self, project_dir, project_name=False):
        self.result = ''
        self.build_directory = os.getcwd()
        self.cmake_path = Cmake.install_cmake()
        self.project_dir = os.path.abspath(project_dir)
        self.generator_name = config.cmakeGenerator
        self.architecture = 'x86'
        self.create_project_path()
        if bool(project_name):
            self.set_project_name(project_name)

    def set_architecture(self, arch):
        self.architecture = arch

    def set_runtime_output_dir(self, directory):
        add_str = 'SET( RUNTIME_OUTPUT_DIRECTORY {} )'.format(directory)
        self.result += add_str
        self.new_line()

    def set_library_output_dir(self, directory):
        add_str = 'SET( LIBRARY_OUTPUT_PATH {} )'.format(directory)
        self.result += add_str
        self.new_line()

    def create_project_path(self):
        require_full_path(self.project_dir)

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

    def get_generator_name(self):
        if not self.generator_name.startswith('Visual'):
            return self.generator_name
        gen_arch = ' Win64' if self.architecture == 'x64' else ''
        return self.generator_name + gen_arch

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

    def set_build_dir(self, directory):
        self.build_directory = directory

    def save(self):
        with open(self.project_dir + '/CMakeLists.txt', 'w+') as cmake_file:
            cmake_file.writelines(self.get_result())

    def get_exec_flags(self):
        build_dir_flag = '-B{}'.format(os.path.abspath(self.build_directory)) if bool(self.build_directory) else ''
        generator_flag = '-G{}'.format(self.get_generator_name())
        sources_dir_flag = '-H{}'.format(os.path.abspath(self.project_dir))
        ret_value = [generator_flag, build_dir_flag, sources_dir_flag]
        # custom_flags = self.get_customs_flags_string()
        # if custom_flags != '':
        #    ret_value.append(custom_flags)
        return ret_value

    def remove_cache(self):
        TemporaryDir.enter(self.project_dir)
        if os.path.isfile('CMakeCache.txt'):
            os.remove('CMakeCache.txt')
        TemporaryDir.leave()

    def run(self):
        log_filename = os.path.join(sys_config.log_folder, 'cmake.log')

        fs.require_full_path(log_filename)
        with open(log_filename, "a+") as cmake_log:
            self.remove_cache()
            command = [self.cmake_path]

            command.extend(self.get_exec_flags())
            if bool(self.build_directory):
                os.makedirs(self.build_directory)
            ret_code = subprocess.call(command, shell=True, stderr=cmake_log, stdout=cmake_log)
            if ret_code:
                raise Exception('"CMAKE RUN" finished with result code ' + str(ret_code))
                sys.exit(1)


class Cmake:
    cmake_built = False
    cmake_path = ''

    def __init__(self, project_directory, project_type='executable'):
        self.builder = CmakeBuilder(project_directory)
        self.cmake_path = Cmake.install_cmake()
        self._sourcesDir = project_directory
        self._buildDir = config.directories['buildDir']
        self._cmakeVersion = config.cmakeVersion
        self._additionalFlags = {}
        self.project_name = config.projectName
        project_type = 'executable' if project_type not in ['executable', 'library'] else project_type
        self.project_type = project_type
        self.generator_name = config.cmakeGenerator
        self.architecture = config.buildArchitecture
        self.build_directory = ''
        self.project_extensions = ['cpp', 'h']

    def set_project_name(self, project_name):
        self.project_name = project_name

    def set_project_extensions(self, extensions):
        self.project_extensions = extensions

    def add_project_extension(self, extension):
        self.project_extensions.append(extension)

    def set_build_dir(self, directory):
        self.build_directory = directory

    def set_sources_dir(self, directory):
        self._sourcesDir = directory

    @staticmethod
    def install_cmake():
        if not Cmake.cmake_built:
            install_module = LibraryModule('cmake', {'rebuild': False, 'version': config.cmakeVersion})
            install_module.prepare()
            Cmake.cmake_built = True
            Cmake.cmake_path = install_module.write_results()['path']
        return Cmake.cmake_path

    @staticmethod
    def find_sources(sources_dir, relative_path=False, extensions=False):
        if not relative_path:
            relative_path = sources_dir
        if not extensions:
            extensions = ['cpp', 'h', 'c']
        if isinstance(extensions, str):
            extensions = [extensions]
        files = []
        for ext in extensions:
            files.extend(glob.glob(sources_dir + '/*.' + ext))
        full_path_files = [os.path.relpath(file_name, relative_path) for file_name in files]
        return full_path_files

    @staticmethod
    def set(var_name, var_value, file_handler):
        file_handler.writelines('set({0} {1}){2}'.format(var_name, var_value, os.linesep))

    def add_static_library(self, file_handler, lib_location, modificator=''):
        file_handler.writelines(
            'target_link_libraries({3} {2} \"{0}\"){1}'.format(lib_location, os.linesep, modificator,
                                                               self.project_name))

    @staticmethod
    def add_headers_location(file_handler, location):
        location = os.path.abspath(location).replace('\\', '/')
        file_handler.writelines('include_directories("{0}"){1}'.format(location, os.linesep))

    def set_flag(self, flag_name, flag_value):
        self._additionalFlags[flag_name] = flag_value

    def get_customs_flags_string(self):
        format_flag = lambda f_name, f_val: '-{0} {1}'.format(f_name, f_val)
        return ' '.join([format_flag(flag, value) for flag, value in self._additionalFlags.items()])

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
        build_dir_flag = '-B{}'.format(os.path.abspath(self.build_directory)) if bool(self.build_directory) else ''
        generator_flag = '-G{}'.format(self.get_generator_name())
        sources_dir_flag = '-H{}'.format(os.path.abspath(self._sourcesDir))
        ret_value = [generator_flag, build_dir_flag, sources_dir_flag]
        custom_flags = self.get_customs_flags_string()
        if custom_flags != '':
            ret_value.append(custom_flags)
        return ret_value

    def remove_cache(self):
        TemporaryDir.enter(self._sourcesDir)
        if os.path.isfile('CMakeCache.txt'):
            os.remove('CMakeCache.txt')
        TemporaryDir.leave()

    def run(self):
        log_filename = os.path.join(sys_config.log_folder, 'cmake.log')

        fs.require_full_path(log_filename)
        with open(log_filename, "a+") as cmake_log:
            self.remove_cache()
            command = [self.cmake_path]

            command.extend(self.get_exec_flags())
            if bool(self.build_directory):
                os.makedirs(self.build_directory)
            print(command)
            ret_code = subprocess.call(command, shell=True, stderr=cmake_log, stdout=cmake_log)
            if ret_code:
                raise Exception('"CMAKE RUN" finished with result code ' + str(ret_code))
                sys.exit(1)

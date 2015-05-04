import os
import glob
import subprocess
import platform

import config
from core.Dependencies.library_module_new import LibraryModule


cmake_program = ''


class Cmake:
    cmake_built = False
    cmake_path = ''

    def __init__(self, project_directory, project_type='executable'):
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

    def set_project_name(self, name):
        self.project_name = name

    def set_build_dir(self, directory):
        self.build_directory = directory

    @staticmethod
    def install_cmake():
        if not Cmake.cmake_built:
            install_module = LibraryModule('cmake', {'rebuild': False, 'version': config.cmakeVersion})
            install_module.prepare()
            Cmake.cmake_built = True
            Cmake.cmake_path = install_module.get_results()['path']
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
            files.extend(glob.glob(sources_dir + "/*." + ext))
        full_path_files = [os.path.relpath(file_name, relative_path) for file_name in files]
        return full_path_files

    @staticmethod
    def set(var_name, var_value, file_handler):
        file_handler.writelines("set({0} {1}){2}".format(var_name, var_value, os.linesep))

    def add_static_library(self, file_handler, lib_location, modificator=""):
        lib_location = os.path.abspath(lib_location).replace('\\', '/')
        file_handler.writelines(
            "target_link_libraries({3} {2} \"{0}\"){1}".format(lib_location, os.linesep, modificator,
                                                               self.project_name))

    @staticmethod
    def add_headers_location(file_handler, location):
        location = os.path.abspath(location).replace('\\', '/')
        file_handler.writelines("include_directories(\"{0}\"){1}".format(location, os.linesep))

    def set_flag(self, flag_name, flag_value):
        self._additionalFlags[flag_name] = flag_value

    def get_flags_string(self):
        format_flag = lambda f_name, f_val: "-{0} {1}".format(f_name, f_val)
        return " ".join([format_flag(flag, value) for flag, value in self._additionalFlags.items()])

    @staticmethod
    def join_if_list(var, symbol=os.linesep):
        return symbol.join(var) if isinstance(var, list) else var

    @staticmethod
    def file_new_line(file_handler):
        file_handler.writelines(os.linesep)

    def set_generator_name(self, generator_name):
        self.generator_name = generator_name

    def set_architecture(self, arch):
        self.architecture = arch

    def get_generator_name(self):
        if not self.generator_name.startswith('Visual'):
            return self.generator_name
        gen_arch = ' Win64' if self.architecture == 'x64' else ''
        return self.generator_name + gen_arch

    def build_deps(self, file_handler):
        for dep_name, dep_config in self.dependencies.items():
            # INSERT CMAKE BEFORE
            cmake_before_string = self.join_if_list(dep_config['cmake_before'])
            cmake_before_string = cmake_before_string.format(project_name=self.project_name)
            file_handler.writelines(cmake_before_string)
            self.file_new_line(file_handler)

            proj_platform = platform.system().lower()
            # INSERT DEBUG LIBS
            debug_libs = dep_config['libs'][proj_platform][config.buildArchitecture]['debug']
            if isinstance(debug_libs, list):
                for lib in debug_libs:
                    self.add_static_library(file_handler, lib, 'debug')
            elif debug_libs is not "":
                self.add_static_library(file_handler, debug_libs, 'debug')

            release_libs = dep_config['libs'][proj_platform][config.buildArchitecture]['release']

            # INSERT RELEASE LIBS
            if isinstance(release_libs, list):
                for lib in release_libs:
                    self.add_static_library(file_handler, lib, 'optimized ')
            elif release_libs is not "":
                self.add_static_library(file_handler, release_libs, 'optimized ')

            # INSERT HEADERS LIBS
            if isinstance(dep_config['headers'], list):
                for location in dep_config['headers']:
                    self.add_headers_location(file_handler, location)
            elif dep_config['headers'] is not "":
                self.add_headers_location(file_handler, dep_config['headers'])

            # INSERT CMAKE AFTER
            cmake_after_string = self.join_if_list(dep_config['cmake_after'])
            cmake_after_string = cmake_after_string.format(project_name=self.project_name)
            file_handler.writelines(cmake_after_string)
            self.file_new_line(file_handler)

    def save(self):
        cmake_file = open(self._sourcesDir + '/CMakeLists.txt', 'w+')
        cmake_file.writelines("cmake_minimum_required(VERSION {0}){1}".format(self._cmakeVersion, os.linesep))
        cmake_file.writelines('project({0}){1}'.format(self.project_name, os.linesep))
        self.set("CMAKE_RUNTIME_OUTPUT_DIRECTORY", "bin", cmake_file)
        main_project_files = self.find_sources(self._sourcesDir)
        if len(main_project_files) > 0:
            self.set("SOURCES_FILES", " ".join(main_project_files), cmake_file)
            cmake_file.writelines(
                "add_" + self.project_type + "(" + self.project_name + " ${SOURCES_FILES})" + os.linesep)
        cmake_file.close()

    def run(self):
        generator = self.get_generator_name()
        with open("cmake.log", "w") as cmake_log:
            current_working_dir = os.getcwd()
            # changing working directory for change cmake output dir
            os.chdir(self._sourcesDir)

            if os.path.isfile('CMakeCache.txt'):
                os.remove('CMakeCache.txt')
            build_dir_flag = '-B' + self.build_directory if bool(self.build_directory) else ''
            command = [self.cmake_path, '-G', generator, build_dir_flag, self.get_flags_string()]
            subprocess.call(command, stderr=cmake_log, stdout=cmake_log)

        # return to previous dir
        os.chdir(current_working_dir)

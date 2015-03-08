import os, glob
import subprocess
import config


class Cmake:
    def __init__(self, dependencies):
        self._sourcesDir = config.directories["solutionDir"]
        self._buildDir = config.directories["buildDir"]
        self._cmakeVersion = config.cmakeVersion
        self._additionalFlags = {}
        self.dependencies = dependencies
        self.project_name = config.projectName

    @staticmethod
    def find_sources(sources_dir, relative_path=False):
        if not relative_path:
            relative_path = sources_dir
        files = glob.glob(sources_dir + "/*.h")
        files.extend(glob.glob(sources_dir + "/*.cpp"))
        full_path_files = [os.path.relpath(file_name, relative_path) for file_name in files]
        return full_path_files

    @staticmethod
    def set(var_name, var_value, file_handler):
        file_handler.writelines("set({0} {1}){2}".format(var_name, var_value, os.linesep))

    def add_static_library(self, file_handler, lib_location, modificator=""):
        lib_location = os.path.abspath(lib_location).replace('\\', '/')
        file_handler.writelines("target_link_libraries({3} {2} \"{0}\"){1}".format(lib_location, os.linesep, modificator, self.project_name))

    @staticmethod
    def add_headers_location(file_handler, location):
        location = os.path.abspath(location).replace('\\', '/')
        file_handler.writelines("include_directories(\"{0}\"){1}".format(location, os.linesep))

    def set_flag(self, flag_name, flag_value):
        self._additionalFlags[flag_name] = flag_value

    def get_flags_string(self):
        format_flag = lambda f_name, f_val: "-{0}={1}".format(f_name, f_val)
        return " ".join([format_flag(flag, value) for flag, value in self._additionalFlags.iteritems()])

    @staticmethod
    def join_if_list(var, symbol=os.linesep):
        return symbol.join(var) if isinstance(var, list) else var

    @staticmethod
    def file_new_line(file_handler):
        file_handler.writelines(os.linesep)

    def build_deps(self, file_handler):
        for dep_name, dep_config in self.dependencies.iteritems():
            cmake_before_string = self.join_if_list(dep_config['cmake_before'])
            cmake_before_string = cmake_before_string.format(project_name=self.project_name)
            file_handler.writelines(cmake_before_string)
            self.file_new_line(file_handler)

            debug_libs = dep_config['libs'][config.buildArchitecture]['debug']

            if isinstance(debug_libs, list):
                for lib in debug_libs:
                    self.add_static_library(file_handler, lib, 'debug')
            elif debug_libs is not "":
                self.add_static_library(file_handler, debug_libs, 'debug')

            release_libs = dep_config['libs'][config.buildArchitecture]['release']

            if isinstance(release_libs, list):
                for lib in release_libs:
                    self.add_static_library(file_handler, lib, 'optimized ')
            elif release_libs is not "":
                self.add_static_library(file_handler, release_libs, 'optimized ')

            if isinstance(dep_config['headers'], list):
                for location in dep_config['headers']:
                    self.add_headers_location(file_handler, location)
            elif dep_config['headers'] is not "":
                self.add_headers_location(file_handler, dep_config['headers'])


            cmake_after_string = self.join_if_list(dep_config['cmake_after'])
            cmake_after_string = cmake_after_string.format(project_name=self.project_name)
            file_handler.writelines(cmake_after_string)
            self.file_new_line(file_handler)

    def build(self):
        cmake_file = open(self._sourcesDir + '/CMakeLists.txt', 'w+')
        cmake_file.writelines("cmake_minimum_required(VERSION {0}){1}".format(self._cmakeVersion, os.linesep))
        cmake_file.writelines('project({0}){1}'.format(self.project_name, os.linesep))
        self.set("CMAKE_RUNTIME_OUTPUT_DIRECTORY", "bin", cmake_file)
        main_project_files = self.find_sources(self._sourcesDir)
        self.set("SOURCES_FILES", " ".join(main_project_files), cmake_file)
        cmake_file.writelines("add_executable(" + self.project_name + " ${SOURCES_FILES})" + os.linesep)
        self.build_deps(cmake_file)
        cmake_file.close()

    def run(self):

        current_working_dir = os.getcwd()
        # changing working directory for change cmake output dir
        os.chdir(self._sourcesDir)

        if os.path.isfile('CMakeCache.txt'):
            os.remove('CMakeCache.txt')

        subprocess.call(['cmake', self.get_flags_string()])

        # return to previous dir
        os.chdir(current_working_dir)

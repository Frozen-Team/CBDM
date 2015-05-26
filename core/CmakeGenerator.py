import sys

import config
from core.common_defs import is_windows, is_linux
from core.tools.cmake import Cmake

cmake_filename = 'CMakeLists.txt'


class CmakeGeneratorFromDeps:
    def __init__(self, project_directory, project_name, dependencies):
        self.project_name = project_name
        self.dependencies = dependencies
        self.cmake_file = Cmake(project_directory)
        self.builder = self.cmake_file.builder
        self.project_type = False
        self.target_name = False
        self.target_files_masks = []

    def set_target_name(self, name):
        self.target_name = name

    def is_executable(self):
        self.project_type = 1

    def is_library(self, lib_type):
        if lib_type not in ['shared', 'static']:
            raise Exception('Lib should be static/shared')
            sys.exit(1)
        self.project_type = 2

    def set_files_masks(self, param):
        self.target_files_masks = param

    def generate(self):
        self.builder.cmake_version(config.cmakeVersion)
        if not bool(self.target_name):
            raise Exception('Specify target_name')
            sys.exit(1)

        self.builder.set_project_name(self.project_name)

        if not bool(self.project_type):
            raise Exception('Specify project type')
            sys.exit(1)

        if not bool(self.target_files_masks):
            raise Exception('Specify project files masks')
            sys.exit(1)

        if self.project_type == 1:
            self.builder.add_executable(self.target_name, self.target_files_masks)
        elif self.project_type == 2:
            self.builder.add_library(self.target_name, self.target_files_masks)

        self.add_dependencies_to_cmake(self.dependencies)
        self.cmake_file.save()

    def add_dependencies_to_cmake(self, results):
        self.builder.write(results['cmake_before'])
        for directory in results['headers']:
            self.builder.include_directories(directory)
        for directory in results['subdirectories']:
            self.builder.add_subdirectory(directory)

        def add_platform(platform_name):
            for dep_config, paths in results['link_directories'].items():
                if dep_config[0] != platform_name:
                    continue
                if dep_config[1] != config.buildArchitecture:
                    continue
                for path in paths:
                    self.builder.link_dir(path)

            for dep_config, lib_names in dict(results['libs']).items():
                if dep_config[0] != platform_name:
                    continue
                if dep_config[1] != config.buildArchitecture:
                    continue
                modificator = 'general' if dep_config[2] == 'release' else 'debug'
                for lib_params in lib_names:
                    self.builder.link_library(self.target_name, lib_params['path'], modificator,
                                              is_libname=lib_params['is_libname'])

        if is_windows():
            add_platform('windows')
        elif is_linux():
            add_platform('linux')

        self.builder.write(results['cmake_after'])




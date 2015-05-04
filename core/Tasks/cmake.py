import os
from core.Dependencies.library_module_new import LibraryModule
from core.tools.cmake import Cmake

__author__ = 'saturn4er'

def run_cmake(sources_dir, architecture, output_dir=False, build_type='executable'):
    cmake_file = Cmake(sources_dir, build_type)
    cmake_file.set_architecture(architecture)
    cmake_file.set_build_dir(output_dir)
    cmake_file.run()

def add_library(config, library_location):
    results = LibraryModule.current_working_module_results
    abs_lib_location = os.path.abspath(library_location)
    results['libs'][config[0]][config[1]][config[2]].append(abs_lib_location)


def add_location(location):
    results = LibraryModule.current_working_module_results
    abs_location = os.path.abspath(location)
    results['headers'].append(abs_location)
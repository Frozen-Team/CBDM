import os

from core.Dependencies.library_module import LibraryModule
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
    library_dir = os.path.dirname(abs_lib_location)
    library_name, library_extension = os.path.splitext(os.path.basename(library_location))
    if library_dir not in results['link_directories']:
        if config not in results['link_directories']:
            results['link_directories'][config] = []
        results['link_directories'][config].append(library_dir)
    if config not in results['libs']:
        results['libs'][config] = []
    results['libs'][config].append(library_name)


def add_location(location):
    results = LibraryModule.current_working_module_results
    abs_location = os.path.abspath(location)
    results['headers'].append(abs_location)


def add_libs_directory(config, directory):
    results = LibraryModule.current_working_module_results
    if config not in results['link_directories']:
        results['link_directories'][config] = []
    results['link_directories'][config].append(directory)
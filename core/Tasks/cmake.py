import os

from core.Dependencies.library_module import LibraryModule
from core.tools.cmake import Cmake

def run_cmake(sources_dir, architecture, output_dir=False, build_type='executable'):
    cmake_file = Cmake(sources_dir, build_type)
    cmake_file.set_architecture(architecture)
    cmake_file.set_build_dir(output_dir)
    cmake_file.run()


def cmake_before(code):
    results = LibraryModule.results
    results['cmake_before'] += code


def add_subdir(dir, exclude_from_all=False):
    results = LibraryModule.results
    results['subdirectories'].append(dir)


def cmake_after(code):
    results = LibraryModule.results
    results['cmake_after'] += code


def link_directory(path_to_dir):
    results = LibraryModule.results
    results['link_directories'].append(path_to_dir)


def add_library(config, library_location, is_libname=False):
    results = LibraryModule.results

    if config not in results['libs']:
        results['libs'][config] = []
    results['libs'][config].append({"path": library_location, "is_libname": is_libname})


def add_location(location):
    results = LibraryModule.results
    abs_location = os.path.abspath(location)
    results['headers'].append(abs_location)


def add_libs_directory(config, directory):
    results = LibraryModule.results
    if config not in results['link_directories']:
        results['link_directories'][config] = []
    results['link_directories'][config].append(directory)

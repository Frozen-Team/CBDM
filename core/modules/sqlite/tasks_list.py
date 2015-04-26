import os

from config import directories
from core.default_structures import cleanup_extensions

sources_dir = "sources"
archive_path = 'sqlite.zip'
build_directory = os.path.join(directories['buildDir'], 'sqlite')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'headers')

sqlite_lib_path = directories["libFolder"] + os.path.sep
sqlite_zip_path = os.path.join(directories["downloadDir"], 'sqlite.zip')
build_tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    {"task": "download_file", "url": "http://www.sqlite.org/2015/sqlite-amalgamation-{version}.zip",
     "destination": archive_path, 'description': 'Downloading sources'},
    {"task": "unzip", "file_location": archive_path, 'description': "Unzip sources"},
    {"task": 'remove_file_by_mask', "mask": archive_path, 'description': "Removing archive..."},
    {"task": "rename_folder_by_mask", 'mask': 'sqlite-amalgamation*',
     'destination': sources_dir,
     'description': "Renaming sources folder", 'override': True},

    {"task": "create_cmake_file", 'sources_dir': sources_dir, 'architecture': 'x32', 'user_task': True,
     'description': 'Building x32 lib', 'output': lib_directory},
    {"task": "create_cmake_file", 'sources_dir': sources_dir, 'architecture': 'x64', 'user_task': True,
     'description': 'Building x64 lib', 'output': lib_directory},
    {"task": "move_files_to_dir_by_mask", 'overwrite': True, 'destination_dir': headers_dir,
     'mask': os.path.join(sources_dir, '*.h'),
     'description': "Copy includes..."},
    {"task": "rdfff", "directory": sources_dir, "extensions": cleanup_extensions["c++"],
     'description': 'Cleaning up trash..'}
]

integration_tasks = [
    ## x86
    {'task': 'add_library', 'config': ('windows', 'x86', 'release'), 'library_location':
        os.path.join(build_directory + '/Release/Win32/glew32s.lib')},
    {'task': 'add_library', 'config': ('windows', 'x86', 'debug'), 'library_location':
        os.path.join(build_directory + '/Debug/Win32/glew32sd.lib')},
    # x32
    {'task': 'add_library', 'config': ('windows', 'x64', 'release'), 'library_location':
        os.path.join(build_directory + '/Release/x64/glew32s.lib')},
    {'task': 'add_library', 'config': ('windows', 'x64', 'debug'), 'library_location':
        os.path.join(build_directory + '/Debug/x64/glew32sd.lib')},

    {'task': 'add_location', 'location': headers_dir},

]
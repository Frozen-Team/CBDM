import os

from config import directories
from core.default_structures import cleanup_extensions


sources_dir = "sources"
glew_path = os.path.join(directories["downloadDir"], 'glew.zip')
build_directory = os.path.join(directories['buildDir'], 'glew')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'headers')

build_tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    {"task": "download_file",
     "destination": glew_path,
     "url": "https://sourceforge.net/projects/glew/files/glew/{version}/glew-{version}.zip/download",
     'description': "Downloading..."},
    {"task": "unzip", "file_location": glew_path, "destination": sources_dir,
     'description': "Unzip..."},
    {"task": 'remove_file_by_mask', "mask": glew_path,
     'description': "Removing archive..."},
    {"task": "make",
     "output_dir": lib_directory,
     "vcxproj_file": os.path.join(sources_dir, 'glew-{version}', 'build', 'vc12', 'glew_static.vcxproj'),
     "makefile": os.path.join(sources_dir, "glew-{version}", "Makefile"),
     "linux_dependencies": {
         "Ubuntu": ['libx11-dev', 'freeglut3-dev']
     },
     "params": {
         "SYSTEM": 'Windows',
         'GLEW_DEST': 'libs'
     },
     'description': "Building..."
    },
    {"task": "move_files_to_dir_by_mask", 'overwrite': True, 'destination_dir': headers_dir,
     'mask': os.path.join(sources_dir, 'glew-{version}', 'include', 'GL', '*.h'),
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
import os
from config import directories

sqlite_lib_path = directories["libFolder"] + os.path.sep
sqlite_zip_path = os.path.join(directories["downloadDir"], 'sqlite.zip')
build_tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    {"task": "download_file", "url": "http://www.sqlite.org/2015/sqlite-amalgamation-{version}.zip",
     "destination": sqlite_zip_path, 'description': 'Downloading sources'},
    {"task": "unzip", "file_location": sqlite_zip_path, 'description': "Unzip sources"},
    {"task": "rename_folder_by_mask", 'mask': 'sqlite-amalgamation*',
     'destination': sqlite_lib_path,
     'description': "Renaming sources folder", 'override': True},
    {"task": "create_cmake_file", 'sources_dir': './' + sqlite_lib_path, 'architecture': 'x32', 'user_task': True,
     "location": sqlite_lib_path, 'description': 'Building x32 lib'},
    {"task": "create_cmake_file", 'sources_dir': './' + sqlite_lib_path, 'architecture': 'x64', 'user_task': True,
     "location": sqlite_lib_path, 'description': 'Building x64 lib'},
]
integration_tasks = [
    {'task': 'add_library', 'config': ('windows', 'x86', 'release'), 'library_location':
        sqlite_lib_path + '/Release/Win32/sqlite.lib'},
    {'task': 'add_library', 'config': ('windows', 'x86', 'debug'), 'library_location':
        sqlite_lib_path + '/Debug/Win32/sqlite.lib'},
    {'task': 'add_library', 'config': ('windows', 'x64', 'release'), 'library_location':
        sqlite_lib_path + '/Release/x64/sqlite.lib'},
    {'task': 'add_library', 'config': ('windows', 'x64', 'debug'), 'library_location':
        sqlite_lib_path + '/Debug/x64/sqlite.lib'},

    {'task': 'add_location', 'location': sqlite_lib_path},

]
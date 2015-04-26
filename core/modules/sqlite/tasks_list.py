from config import directories

spdlog_path = directories["libFolder"] + "/"
sources_dir = 'sources'
build_tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    {"task": "download_file", "url": "http://www.sqlite.org/2015/sqlite-amalgamation-{version}.zip",
     "destination": 'sources.zip', 'description': 'Downloading sources'},
    {"task": "unzip", "file_location": 'sources.zip', 'description': "Unzip sources"},
    {"task": "rename_folder_by_mask", 'mask': 'sqlite-amalgamation*', 'destination': sources_dir,
     'description': "Renaming sources folder", 'override': True},
    {"task": "create_cmake_file", 'sources_dir': './' + sources_dir, 'architecture': 'x32', 'user_task': True,
     "location": sources_dir, 'description': 'Building x32 lib'},
    {"task": "create_cmake_file", 'sources_dir': './' + sources_dir, 'architecture': 'x64', 'user_task': True,
     "location": sources_dir, 'description': 'Building x64 lib'},
]
integration_tasks = [
    {'task': 'add_library', 'config': ('windows', 'x86', 'release'), 'library_location':sources_dir+'/Release/Win32/sqlite.lib'},
    {'task': 'add_library', 'config': ('windows', 'x86', 'debug'), 'library_location':sources_dir+'/Debug/Win32/sqlite.lib'},
    {'task': 'add_library', 'config': ('windows', 'x64', 'release'), 'library_location':sources_dir+'/Release/x64/sqlite.lib'},
    {'task': 'add_library', 'config': ('windows', 'x64', 'debug'), 'library_location':sources_dir+'/Debug/x64/sqlite.lib'},
]
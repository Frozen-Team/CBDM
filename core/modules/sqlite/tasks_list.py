from config import directories

spdlog_path = directories["libFolder"] + "/"
sources_dir = 'sources'
build_tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    # {"task": "download_file", "url": "http://www.sqlite.org/2015/sqlite-amalgamation-{version}.zip",
    # "destination": 'sources.zip', 'description': 'Downloading sources'},
    # {"task": "unzip", "file_location": 'sources.zip', 'description': "Unzip sources"},
    # {"task": "rename_folder_by_mask", 'mask': 'sqlite-amalgamation*', 'destination': sources_dir,
    #  'description': "Renaming sources folder", 'override': True},
    {"task": "create_cmake_file", 'user_task': True, "location": sources_dir},
]
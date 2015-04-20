from config import directories

spdlog_path = directories["libFolder"] + "/"
build_tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    {"task": "download_file", "url": "http://www.sqlite.org/2015/sqlite-amalgamation-{version}.zip",
     "destination": 'sources.zip', 'description': 'Downloading sources'},
    {"task": "unzip", "file_location": 'sources.zip', 'description': "Unzip sources"},
    {"task": "rename_folder_by_mask", 'mask': 'sqlite-amalgamation*', 'destination': 'sources',
     'description': "Renaming sources folder", 'override': True}
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
repository_dir = "sources"
tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "download_file",
    "destination": 'sources.zip',
    "url": "http://bitbucket.org/eigen/eigen/get/{version}.zip"},
    {"task": 'remove_file_by_mask', 'mask': 'eigen_sources'},
    {"task": 'remove_file_by_mask', 'mask': 'eigen-eigen-*'},
    {"task": "unzip", "file_location": "sources.zip"},
    {'task': 'rename_sources_dir', 'user_task': True},
    {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
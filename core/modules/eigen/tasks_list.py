import os
from config import directories

repository_dir = "sources"
eigen_file_path = os.path.join(directories["downloadDir"], 'eigen.zip')
build_tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "download_file", "destination": eigen_file_path,
     "url": "http://bitbucket.org/eigen/eigen/get/{version}.zip"},
    {"task": 'remove_file_by_mask', 'mask': 'eigen_sources'},
    {"task": 'remove_file_by_mask', 'mask': 'eigen-eigen-*'},
    {"task": "unzip", "file_location": eigen_file_path, "destination": directories["libFolder"] + "/"},
    {'task': 'rename_eigen', 'user_task': True},
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
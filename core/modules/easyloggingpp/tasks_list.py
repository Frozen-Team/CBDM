import os
from config import directories
from core.default_structures import cleanup_extensions

origin_dir = 'Origin'
build_directory = os.path.join(directories['buildDir'], 'easyloggingpp')
headers_dir = os.path.join(build_directory, 'include')
build_tasks = [
    {'task': 'check_dependencies', 'params': ('version', 'rebuild'), 'description': 'Checking dependencies'},
    {'task': 'remove_file_by_mask', 'mask': origin_dir, 'description': 'Deleting old version of easyloggingpp'},
    {'task': 'git_clone', 'repository': 'https://github.com/easylogging/easyloggingpp.git', 'sources_dir': origin_dir,
     'description': 'Cloning easyloggingpp'},
    {'task': 'git_checkout', 'sources_dir': origin_dir, 'branch': '{version}', 'description': 'Checkout at {version}'},

    {'task': 'rename_folder_by_mask', 'mask': os.path.join(origin_dir, 'src'), 'destination': headers_dir,
     'overwrite': True,
     'description': 'Moving headers to build directory'},
    {'task': 'rdfff', 'directory': origin_dir, 'extensions': cleanup_extensions['c++'],
     'description': 'Cleaning up trash'}
]

integration_tasks = [
    {'task': 'add_location', 'location': headers_dir, 'description': 'Adding easyloggingpp headers location'},
]
import os

from config import directories
from core.default_structures import cleanup_extensions

from core.Tasks import check_dependencies, fs, vcs, cmake, net, archives

archive_path = 'eigen.zip'
build_directory = os.path.join(directories['buildDir'], 'eigen')
headers_dir = os.path.join(build_directory, 'include')

build_tasks = [
    {'task': 'unzip', 'file_location': archive_path,
     'description': 'Extracting eigen'},
    {'task': 'remove_file_by_mask', 'mask': archive_path, 'description': 'Removing archive'},
    {'task': 'rename_folder_by_mask', 'mask': os.path.join('eigen-*', 'Eigen'),
     'destination': headers_dir, 'overwrite': True},
    {'task': 'remove_file_by_mask', 'mask': 'eigen-*', 'description': 'Removing sources'},
    {'task': 'rdfff', 'directory': headers_dir, 'extensions': cleanup_extensions['c++'], 'except': ['', '.h'],
     'description': 'Cleaning up trash'}
]


def build(module_params):
    check_dependencies(False, ['version'])
    url_to_eigen = 'http://bitbucket.org/eigen/eigen/get/{version}.zip'.format(version=module_params['version'])
    net.download_file(url_to_eigen, archive_path)
    archives.extract_zip(archive_path)
    fs.rename(os.path.join('eigen-*', 'Eigen'), headers_dir, True)
    fs.remove('eigen-*')
    fs.remove(archive_path)
    fs.clear(headers_dir)


integration_tasks = [
    {'task': 'add_location', 'location': headers_dir},
]
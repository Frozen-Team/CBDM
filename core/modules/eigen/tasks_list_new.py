import os

from config import directories
from core.Tasks import check_dependencies, fs, net, archives, cmake

origin_dir = 'Origin'
archive_path = 'eigen.zip'
includes_dir = os.path.join(directories['solution_third_party_dir'], 'eigen')


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    url_to_eigen = 'http://bitbucket.org/eigen/eigen/get/{version}.zip'.format(version=module_params['version'])
    net.download_file(url_to_eigen, archive_path)
    archives.extract_zip(archive_path)
    fs.rename(os.path.join('eigen-*', 'Eigen'), origin_dir, True)
    fs.remove('eigen-*')
    fs.remove(archive_path)
    fs.clear(origin_dir)


def integration(module_params):
    fs.copy(origin_dir, includes_dir, True)
    cmake.add_location(includes_dir)
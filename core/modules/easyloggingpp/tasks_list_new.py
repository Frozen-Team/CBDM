import os

from config import directories
from core.Tasks import check_dependencies, fs, vcs, cmake


origin_dir = 'Origin'
build_directory = os.path.join(directories['buildDir'], 'easyloggingpp')
headers_dir = os.path.join(build_directory, 'include')


def build(module_params):
    check_dependencies(False, ('version'))
    fs.remove(origin_dir)
    vcs.git_clone('https://github.com/easylogging/easyloggingpp.git', origin_dir)
    vcs.git_checkout(origin_dir, module_params['version'])
    fs.rename(os.path.join(origin_dir, 'src'), headers_dir, True)
    fs.remove(origin_dir)


def integration(module_params):
    cmake.add_location(headers_dir)
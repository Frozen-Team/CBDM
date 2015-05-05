import os
from config import directories
from core.Tasks import check_dependencies, fs, cmake, vcs

origin_dir = 'Origin'
build_directory = os.path.join(directories['buildDir'], 'spdlog')
headers_dir = os.path.join(build_directory, 'include')


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    fs.remove(origin_dir)
    vcs.git_clone('https://github.com/gabime/spdlog.git', origin_dir, True)
    vcs.git_checkout(origin_dir, module_params['version'])
    fs.rename(os.path.join(origin_dir, 'include'), headers_dir, True)
    fs.remove(origin_dir)


def integration(module_params):
    cmake.add_location(headers_dir)
import os
from config import directories
from core.Tasks import check_dependencies, fs, net, archives, cmake, assembly, vcs

glm_path = 'glm.zip'
origin_dir = 'Origin'
build_directory = os.path.join(directories['buildDir'], 'glm')
headers_dir = os.path.join(build_directory, 'include')


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    fs.remove(origin_dir)
    glm_url = "http://sourceforge.net/projects/ogl-math/files/glm-{0}/glm-{0}.zip/download".format(
        module_params['version'])
    net.download_file(glm_url, glm_path)
    archives.extract_7_zip(glm_path, origin_dir)
    fs.rename(os.path.join(origin_dir, 'glm', 'glm'), headers_dir, True)
    fs.remove(glm_path)
    fs.remove(origin_dir)


def integration(module_params):
    cmake.add_location(headers_dir)
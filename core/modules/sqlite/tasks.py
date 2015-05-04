from core.tools.vcxproj import Builder
import core.Dependencies.Tasks as tasks
from core.tools.cmake import Cmake


def create_cmake_file(module_name, task_params, module_params, result):
    sources_dir = tasks.check_param(module_name, task_params, 'sources_dir')
    arch = tasks.check_param(module_name, task_params, 'architecture')
    output_dir = tasks.check_param(module_name, task_params, 'output', './lib/')
    cmake_file = Cmake(sources_dir, {}, 'library')
    cmake_file.set_project_name('sqlite')
    cmake_file.set_architecture(arch)
    cmake_file.save()
    cmake_file.run()
    vcxproj = Builder(sources_dir+'/sqlite.vcxproj')
    vcxproj.build(['Debug', 'Release'], False, output_dir)


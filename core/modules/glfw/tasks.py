from config import directories
from core.Dependencies import Tasks
from core.cmake import Cmake


def run_cmake_and_build(module_name, task_params, module_params, result):
    sources_dir = Tasks.check_param(module_name, task_params, 'sources_dir')
    arch = Tasks.check_param(module_name, task_params, 'architecture')
    cmake_file = Cmake(sources_dir, {}, 'library')
    cmake_file.set_project_name('sqlite')
    cmake_file.set_build_dir(directories["buildDir"])
    cmake_file.set_architecture(arch)
    # cmake_file.save()
    cmake_file.run()
    # vcxproj = Builder(sources_dir+'/sqlite.vcxproj')
    # vcxproj.build(['Debug', 'Release'], False, output_dir)
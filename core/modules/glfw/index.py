<<<<<<< HEAD
import os
import platform
import shutil
import core.modules.glfw.config as m_config
from core.git import Repo
from core.vsproj import Vcproj

module_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.getcwd()
sources_dir = module_dir+'/'+m_config.sources_path


def readonly_handler(func, path, execinfo):
    os.chmod(path, 128)
    func(path)


def load_glew(version, path, rebuild):
    repo = Repo(sources_dir, 'logs/glew_git.txt')
    if os.path.exists(path):
        if rebuild or not repo.is_repo():
            shutil.rmtree(path, ignore_errors=False, onerror=readonly_handler)
    repo.clone('git://git.frozen-team.com/Glew.git')
    repo.checkout('skeleton-{0}'.format(version))
    __fix_vcproj()


def __fix_vcproj():
    if not platform.system() == "Windows":
        return
    file = Vcproj(module_dir+'/'+m_config.vis_studio_project_path)
    config = file.get_configuration("Debug")
    config.set_runtime_librarie(Vcproj.runtimeLibraries["MDd"])
    config.save()
    config = config.get_configuration("Release")
    config.set_runtime_librarie(Vcproj.runtimeLibraries["MD"])
    config.save()


def compile_glew(sources_dir, params):
    if platform.system() == "Windows":
        os.chdir(module_dir)
        build_path = os.path.abspath(params['build_path'])
        os.chdir(project_dir)
        project = Vcproj(module_dir+'/'+m_config.vis_studio_project_path)
        project.build(output=build_path, log_file='logs/glew_build.txt')
        return {
            "libs": {
                "x64": {
                    "debug": build_path + "/Debug/x64/glew32sd.lib",
                    "release": build_path + "/Release/x64/glew32s.lib",
                },
                "x32": {
                    "debug": build_path + "/Debug/Win32/glew32sd.lib",
                    "release": build_path + "/Release/Win32/glew32s.lib",
                }
            }
        }


def build(params):
    result = {}
    sources_dir = "sources"
    load_glew(params['version'], sources_dir, params["rebuild"])
    compile_result = compile_glew(sources_dir, params)
    result.update(compile_result)
    os.chdir(module_dir)
    build_path = os.path.abspath(params['build_path'])
    if not os.path.exists(build_path + '/include'):
        shutil.copytree(sources_dir + '/include/', build_path + '/include')
    result["headers"] = build_path + "/include"
    os.chdir(project_dir)

=======
import os
import platform
import shutil
from core.vsproj import Vcproj

module_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.getcwd()


def readonly_handler(func, path, execinfo):
    os.chmod(path, 128)
    func(path)


def load_glew(version, path, rebuild):
    os.chdir(module_dir)
    if os.path.exists(path):
        if rebuild:
            shutil.rmtree(path, ignore_errors=False, onerror=readonly_handler)
        else:
            _fix_vcproj(path + '/build/vc12/glew_static.vcxproj')
            os.chdir(project_dir)
            return True
    os.system('git clone https://github.com/glfw/glfw.git ' + path)
    os.chmod(path, 7777)
    os.chdir(module_dir + '/' + path)
    os.system('git checkout ' + version)
    os.chdir(project_dir)


def _fix_vcproj(file_name):
    if not platform.system() == "Windows":
        return
    file = Vcproj(file_name)
    config = file.get_configuration("Debug")
    config.set_runtime_librarie(Vcproj.runtimeLibraries["MTd"])
    config.save()


def compile_glew(sources_dir, params):
    if platform.system() == "Windows":
        os.chdir(module_dir)
        os.system('cmake ./')
        build_path = os.path.abspath(params['build_path'])
        project = Vcproj(os.path.abspath(sources_dir + '/src/glfw.vcxproj'))
        project.build(output=build_path)
        os.chdir(project_dir)
        return {
            "libs": {
                "x64": {
                    "debug": build_path + "/Debug/x64/glew32sd",
                    "release": build_path + "/Release/x64/glew32s",
                },
                "x32": {
                    "debug": build_path + "/Debug/Win32/glew32sd",
                    "release": build_path + "/Release/Win32/glew32s",
                }
            }
        }


def build(params):
    result = {}
    sources_dir = "sources"
    load_glew(params['version'], sources_dir, params["rebuild"])
    compile_result = compile_glew(sources_dir, params)
    # result.update(compile_result)
    # os.chdir(module_dir)
    # build_path = os.path.abspath(params['build_path'])
    # if not os.path.exists(build_path + '/include'):
    #     shutil.copytree(sources_dir + '/include/', build_path + '/include')
    # result["headers"] = build_path + "/include"
    # os.chdir(project_dir)

>>>>>>> bfa307ac3ef8ddccef6b9be52825cd7d8edc3f51
    return result
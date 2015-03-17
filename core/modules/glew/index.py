import os
import platform
import shutil
import core.modules.glew.config as m_config
from core.git import Repo
from core.vsproj import Vcproj

module_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.getcwd()
sources_dir = module_dir+'/'+m_config.sources_path


def readonly_handler(func, path, execinfo):
    os.chmod(path, 128)
    func(path)


def load_glew(version, path, rebuild):
    repo = Repo(sources_dir, m_config.log_clone_file)
    if os.path.exists(path):
        if rebuild or not repo.is_repo():
            shutil.rmtree(path, ignore_errors=False, onerror=readonly_handler)
    else:
        repo.clone(m_config.repo)
        repo.checkout(m_config.version_branch.format(v=version))
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
        project.build(output=build_path, log_file=m_config.log_build_project)
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

    return result
import os
import platform
import shutil
import config
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
            _fix_vcproj(path+'/build/vc12/glew_static.vcxproj')
            os.chdir(project_dir)
            return True
    os.system('git clone git://git.frozen-team.com/Glew.git '+path+"&")
    os.chmod(path, 7777)
    os.chdir(module_dir+'/'+path)
    os.system('git checkout glew-'+version)
    os.chdir(project_dir)


def _fix_vcproj(file_name):
    if not platform.system() == "Windows":
        return
    file = Vcproj(file_name)
    config = file.get_configuration("Debug")
    config.set_runtime_librarie(Vcproj.runtimeLibraries["MTd"])
    config.save()



def compile_glew(sources_dir, params):
    available_architectures = ('Win32', )
    if platform.system() == "Windows":
        os.chdir(module_dir)
        project = Vcproj(os.path.abspath(sources_dir+'/build/vc12/glew_static.vcxproj'))
        project.build()
        os.chdir(project_dir)


def build(params):

    sources_dir = "sources"
    load_glew(params['version'], sources_dir, params["rebuild"])
    compile_glew(sources_dir, params)
    return {}
import os
import platform
import shutil
from zipfile import ZipFile
import core.modules.eigen.config as m_config
import urllib.request
import json

module_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.getcwd()
sources_dir = module_dir+'/'+m_config.sources_path


def readonly_handler(func, path, execinfo):
    os.chmod(path, 128)
    func(path)


def load(version, path, rebuild, cache):

    if os.path.exists(path):
        if rebuild or cache.last_loaded_version != version:
            shutil.rmtree(path, ignore_errors=False, onerror=readonly_handler)
    else:
        repository = urllib.request.urlopen(m_config.download_path.format(v=version))
        sources_zip = open(module_dir+'/sources.zip', 'wb')
        sources_zip.write(repository.read())


def unpack():
    with ZipFile(module_dir+'/sources.zip') as sources:
        sources.extractall(sources_dir)


def get_includes(params):
    if platform.system() == "Windows":
        build_path = os.path.abspath(params['build_path'])
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


def get_module_cache():
    try:
        with open(module_dir+'/cache', 'r') as cache_file:
            return json.loads(cache_file.read())
    except FileNotFoundError and ValueError:
        return {}


def set_module_cache(data):
    with open(module_dir+'/cache', 'w') as cache_file:
        cache_file.write(json.dumps(data))


def build(params):
    cache = get_module_cache()
    result = {}
    load(params['version'], sources_dir, params["rebuild"], cache)
    unpack()
    result.update(get_includes(params))
    return result
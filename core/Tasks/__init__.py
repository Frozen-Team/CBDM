from shutil import which

import config
from core.Dependencies.library_module import LibraryModule
import core.sys_config as s_config


def require_module(module_name, conf=False):
    if not conf:
        conf = config.dependencies[module_name] if module_name in config.dependencies else {}

    dependend_module = LibraryModule(module_name, conf)
    dependend_module.prepare()
    results = dependend_module.write_results()
    LibraryModule.flush_results()
    return results


def check_dependencies(programs=False, params=False, module_params=False):
    module_name = LibraryModule.current_working_module
    if bool(programs):
        for program_name in programs:
            if which(program_name) is None:
                error = s_config.no_external_program_error.format(program_name=program_name.upper())
                raise Exception(error)
                sys.exit(15)
    if bool(params) and bool(module_params):
        for param in params:
            if param not in module_params:
                error = s_config.no_module_param_error.format(module_name=module_name, param_name=param)
                raise Exception(error)
                sys.exit(15)
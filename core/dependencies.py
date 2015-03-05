import os
import sys
import importlib

default_dependency_struct = {"libs": {
                                         "x64": {
                                             "debug": "",  # can be also a list
                                             "release": "",  # can be also a list
                                         },
                                         "x32": {
                                             "debug": "",  # can be also a list
                                             "release": "",  # can be also a list
                                         }
                                     },
                             "headers": "",  # could be a list
                             "cmake_before": "",
                             "cmake_after": ""
                             }


class Dependencies:
    def __init__(self, dependencies):
        self.dependencies = dependencies
        self.modules_results = {}

    def _get_module_params(self, module_name):
        params = self.dependencies[module_name]
        new_params = {
            "version": 0,
            "build_path": os.path.realpath("core/modules/" + module_name + '/build/'),
            "rebuild": False
        }

        if isinstance(params, str):
            new_params["version"] = params

        if type(params) == type(dict()):
            new_params.update(params)
        return new_params

    def _build_dependency(self, depend_name):
        module_index = os.path.realpath("core/modules/" + depend_name + "/index.py")
        if not os.path.isfile(module_index):
            print('Module {0} wasn\'t found ({1})'.format(depend_name, module_index))
            sys.exit(1)
        module = importlib.import_module("core.modules.{0}.index".format(depend_name))

        reorganized_module_config = self._get_module_params(depend_name)

        depend_result = module.build(reorganized_module_config)
        if type(depend_result) == type(dict()):
            _depend_result = default_dependency_struct.copy()
            _depend_result.update(depend_result)
            self.modules_results[depend_name] = _depend_result

    def build_dependencies(self):
        for name in self.dependencies:
            self._build_dependency(name)

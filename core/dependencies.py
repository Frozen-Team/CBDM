import os
import sys
import importlib


class Dependencies:
    def __init__(self, dependencies):
        self.dependencies = dependencies

    def _get_module_params(self, module_name):
        params = self.dependencies[module_name]
        new_params = {
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
            print('Module {0} wasn\'t found ({1})'.format(depend_name,module_index))
            sys.exit(1)
        module = importlib.import_module("core.modules.{0}.index".format(depend_name))

        reorganized_module_config = self._get_module_params(depend_name)
        module.build(reorganized_module_config)

    def build_dependencies(self):
        for name in self.dependencies:
            self._build_dependency(name)

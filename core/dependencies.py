import os
import sys
import importlib
import core.default_structures as struct
import core.sys_config as cconfig


class Dependencies:
    def __init__(self, dependencies):
        self.dependencies = dependencies
        self.modules_results = {}

    def _get_module_params(self, module_name):
        params = self.dependencies[module_name]
        new_params = struct.module_config.copy()
        new_params['build_path'] = new_params["build_path"].format(module_name=module_name)
        if isinstance(params, str):
            new_params["version"] = params
        if type(params) == type(dict()):
            new_params.update(params)
        return new_params

    def _build_dependency(self, depend_name):
        module_index = os.path.realpath("core/modules/" + depend_name + "/index.py")
        if not os.path.isfile(module_index):
            print(cconfig.no_module_error.format(module_name=depend_name, full_path=module_index))
            sys.exit(1)
        module = importlib.import_module("core.modules.{0}.index".format(depend_name))

        reorganized_module_config = self._get_module_params(depend_name)

        depend_result = module.build(reorganized_module_config)
        if type(depend_result) == type(dict()):
            _depend_result = struct.default_dependency_struct.copy()
            _depend_result.update(depend_result)
            self.modules_results[depend_name] = _depend_result

    def build_dependencies(self):
        dependencies_count = len(self.dependencies)
        for i, name in enumerate(self.dependencies):
            print(cconfig.percents_output.format(i / dependencies_count))
            self._build_dependency(name)

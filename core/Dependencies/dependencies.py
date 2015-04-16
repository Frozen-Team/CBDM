import os
import sys
import importlib
from core.Dependencies.library_module import LibraryModule
import core.default_structures as struct
import core.sys_config as cconfig


class Dependencies:
    def __init__(self, dependencies):
        self.dependencies = dependencies
        self.modules_results = {}

    def __get_module_params(self, module_name):
        params = self.dependencies[module_name]
        new_params = struct.library_module_config.copy()
        new_params['build_path'] = new_params["build_path"].format(module_name=module_name)
        if isinstance(params, str):
            new_params["version"] = params
        if isinstance(params, dict):
            new_params.update(params)
        return new_params

    def __build_dependency(self, depend_name):
        library_module = LibraryModule(depend_name, self.__get_module_params(depend_name))
        library_module.run_tasks()
        self.modules_results[depend_name] = library_module.get_results()

    def build_dependencies(self):
        dependencies_count = len(self.dependencies)
        for i, name in enumerate(self.dependencies):
            print(cconfig.percents_output.format(i / dependencies_count))
            self.__build_dependency(name)
        print(cconfig.percents_output.format(1.))
from core.Dependencies.library_module import LibraryModule
import config
import core.sys_config as s_config


class Dependencies:
    def __init__(self):
        self.modules_results = {}

    def __build_dependency(self, depend_name):
        library_module = LibraryModule(depend_name, config.dependencies[depend_name])
        library_module.prepare()
        self.modules_results[depend_name] = library_module.get_results()

    def build_dependencies(self):
        dependencies_count = len(config.dependencies)
        for i, name in enumerate(config.dependencies):
            print(s_config.percents_output.format(i / dependencies_count))
            self.__build_dependency(name)
        print(s_config.percents_output.format(1.))

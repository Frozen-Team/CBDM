import time

from core.Dependencies.library_module import LibraryModule
import config
import core.sys_config as s_config


class Dependencies:
    @staticmethod
    def get_results():
        return LibraryModule.results

    @staticmethod
    def __build_dependency(depend_name):
        library_module = LibraryModule(depend_name, config.dependencies[depend_name])
        library_module.prepare()
        library_module.write_results()

    def build_dependencies(self):
        starts = int(time.time())
        dependencies_count = len(config.dependencies)
        for i, name in enumerate(config.dependencies):
            print(s_config.percents_output.format(i / dependencies_count))
            self.__build_dependency(name)
        print(s_config.percents_output.format(1.))

        ends = time.time()
        total = ends - starts
        print("""
        ===== ALL TASKS COMPLETED SUCCESSFULLY =====


        Starts on {}.
        Ends on {}.
        Total: {}""".format(time.ctime(starts), time.ctime(ends), time.strftime('%H:%M:%S', time.gmtime(total))))

import importlib
import os
import json

from core.TemporaryDir import TemporaryDir
import core.sys_config as s_config
import core.default_structures as structs


project_location = os.getcwd() + os.path.sep


class LibraryModule:
    current_working_module_results = {}

    def __init__(self, module_name, configs):
        self.module_name = module_name
        self.module_location = project_location + s_config.modules_location.format(module_name=module_name)
        self.full_module_location = os.path.abspath(self.module_location)
        self.__check_if_module_exists()

        self.tasks_list = self.__load_module_file(s_config.tasks_list_file, True)

        self.module_configs = configs
        LibraryModule.flush_results()

    def __check_if_module_exists(self):
        if not os.path.exists(self.module_location):
            exc_str = s_config.no_module_error.format(module_name=self.module_name, full_path=self.full_module_location)
            raise Exception(exc_str)

    def __check_if_module_file_exists(self, file_name, required):
        tasks_file_location = self.module_location + os.path.sep + file_name + '.py'
        if not os.path.isfile(tasks_file_location):
            if required:
                raise Exception(s_config.no_file_error.format(file_name=tasks_file_location))
            else:
                return False
        return True

    def __load_module_file(self, file_name, required):
        if not self.__check_if_module_file_exists(file_name, required) and not required:
            return False
        module_name = s_config.modules_py_mod_location.format(file=file_name, module_name=self.module_name)
        return importlib.import_module(module_name)

    @staticmethod
    def __set_cache(var, value):
        if not os.path.isfile('ModuleCache'):
            with open('ModuleCache', 'w+') as new_file:
                new_file.write("")
        with open('ModuleCache', 'r+') as cache_file:
            try:
                file = cache_file.read()
                json_data = json.loads(file)
            except:
                json_data = {}
            json_data[var] = value
            with open('ModuleCache', 'w+') as cache_file_write:
                cache_file_write.write(json.dumps(json_data))

    @staticmethod
    def __get_cache():
        try:
            with open('ModuleCache', 'r+') as cache_file:
                file = cache_file.read()
                json_data = json.loads(file)
        except:
            json_data = {}
        return json_data

    def module_need_rebuild(self):
        cache = LibraryModule.__get_cache()
        need_rebuild = 'rebuild' in self.module_configs and self.module_configs['rebuild']
        already_built = 'built' in cache and cache['built']
        return need_rebuild or not already_built

    def prepare(self):
        TemporaryDir.enter(self.full_module_location)
        print("###### Preparing module '{0}' ####".format(self.module_name))
        LibraryModule.current_working_module = self.module_name
        if self.module_need_rebuild():
            fnc = self.function_in_tasks_exist(s_config.module_prepare_function)
            if bool(fnc):
                fnc(self.module_configs)
                print("###### Library was successfully built #### ")
                LibraryModule.__set_cache('built', True)
        else:
            print("###### Library has been processed... Skipping #### ")
        TemporaryDir.leave()

    def function_in_tasks_exist(self, file_name):
        attr_exist = hasattr(self.tasks_list, file_name)
        if not attr_exist:
            return False
        attr = getattr(self.tasks_list, file_name)
        attr_is_func = hasattr(attr, '__call__')
        return attr if attr_is_func else False

    def get_results(self):
        LibraryModule.current_working_module_results = structs.default_dependency_struct.copy()
        TemporaryDir.enter(self.full_module_location)
        fnc = self.function_in_tasks_exist(s_config.module_integration_function)
        if bool(fnc):
            fnc(self.module_configs)

        TemporaryDir.leave()
        return LibraryModule.current_working_module_results

    @staticmethod
    def flush_results():
        LibraryModule.current_working_module_results = structs.default_dependency_struct.copy()
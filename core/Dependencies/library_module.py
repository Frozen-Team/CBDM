import importlib
import os
import sys
import core.sys_config as s_config
import core.default_structures as structs
import core.Dependencies.Tasks as Tasks
import platform
import json


class LibraryModule:
    def __init__(self, module_name, configs):
        self.module_name = module_name

        self.module_location = s_config.modules_location.format(module_name=module_name)
        self.full_module_location = os.path.abspath(self.module_location)
        self.__check_if_module_exists()

        self.tasks_list = self.__load_module_file(s_config.tasks_list_file, True)
        self.additional_tasks = self.__load_module_file(s_config.additional_tasks_file, False)

        self.results = structs.default_dependency_struct.copy()
        self.module_configs = configs

    def __check_if_module_exists(self):
        if not os.path.exists(self.module_location):
            exc_str = s_config.no_module_error.format(module_name=self.module_name, full_path=self.full_module_location)
            raise Exception(exc_str)
            sys.exit(5)

    def __check_if_module_file_exists(self, file_name, required):
        tasks_file_location = self.module_location + os.path.sep + file_name + '.py'
        if not os.path.isfile(tasks_file_location):
            if required:
                raise Exception(s_config.no_file_error.format(file_name=tasks_file_location))
                sys.exit(5)
            else:
                return False
        return True

    def __load_module_file(self, file_name, required):
        if not self.__check_if_module_file_exists(file_name, required) and not required:
            return False
        module_name = s_config.modules_py_mod_location.format(file=file_name, module_name=self.module_name)
        return importlib.import_module(module_name)

    def __prepare_task_params(self, task_params, module_params):
        """
        Format task params using module config
        For example:
            Module config {"language":"ru"}
            Task params {"task": "test_task", "some_param":"param_value_{language}"}
            Result will be {"task": "test_task", "some_param":"param_value_ru"}
        :return: Formatted task params
        """
        result = {}
        format_dict = {"module_name": self.module_name}
        for key, val in module_params.items():
            if isinstance(val, str):
                format_dict[key] = val
        for key, task_param in task_params.items():
            if isinstance(task_param, str):
                result[key] = task_param.format(**format_dict)
            else:
                result[key] = task_param
        return result

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

    def run_tasks(self):
        print("###### Working on '{0}' ####".format(self.module_name))
        project_location = os.getcwd()
        os.chdir(self.module_location)
        cache = LibraryModule.__get_cache()
        need_rebuild = 'rebuild' in self.module_configs and self.module_configs['rebuild']
        already_built = 'built' in cache and cache['built']
        if need_rebuild or not already_built:
            if hasattr(self.tasks_list, 'build_tasks'):
                for task in self.tasks_list.build_tasks:
                    self.__run_task(task)

            print("###### Library was successfully built #### ")
            LibraryModule.__set_cache('built', True)
        elif already_built and not need_rebuild:
            print("###### Library has been processed... Skipping #### ")

        if hasattr(self.tasks_list, 'integration_tasks'):
            for task in self.tasks_list.integration_tasks:
                self.__run_task(task)
        os.chdir(project_location)

    def __run_task(self, task):
        if not LibraryModule.__validate_task(task):
            return False
        task_name = task['task']

        is_user_task = "user_task" in task and task['user_task']
        task_description = task['description'] if "description" in task else False

        if is_user_task:
            task_exist = bool(self.additional_tasks) & hasattr(self.additional_tasks, task_name)
        else:
            task_exist = hasattr(Tasks, task_name)

        if not task_exist:
            exception_error = s_config.no_task_error.format(task_name=task_name, module_name=self.module_name)
            raise Exception(exception_error)
            sys.exit(10)
        if task_description:
            print('Running task: ' + task_description)
        if is_user_task:
            task_function = getattr(self.additional_tasks, task_name)
        else:
            task_function = getattr(Tasks, task_name)

        task_params = self.__prepare_task_params(task, self.module_configs)
        task_function(self.module_name, task_params, self.module_configs, self.results)

    @staticmethod
    def __validate_task(task):
        if "task" not in task:
            return False
        if "platform" in task:
            if task['platform'].lower() != platform.system().lower():
                return False
        return True

    def get_results(self):
        return self.results
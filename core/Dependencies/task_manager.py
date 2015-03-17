import importlib
import os
import sys
import core.sys_config as s_config
import core.default_structures as structs
import core.Dependencies.Tasks as Tasks


class TasksManager:
    def __init__(self, module_name, configs):
        self.module_name = module_name
        self.module_location = s_config.modules_location.format(module_name=module_name)
        self.full_module_location = os.path.abspath(self.module_location)
        self.__check_if_module_exists()

        self.tasks_list = self.__load_module_file(s_config.tasks_list_file, True)
        self.additional_tasks = self.__load_module_file(s_config.additional_tasks_file, False)

        self.results = structs.default_dependency_struct.copy()
        self.configs = configs

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

    def run_tasks(self):
        project_location = os.getcwd()
        os.chdir(self.module_location)
        for task in self.tasks_list.tasks:
            if "task" not in task:
                continue
            user_task = "user_task" in task and task['user_task']
            user_task_not_exists = user_task and self.additional_tasks is False
            task_not_exist = not hasattr(Tasks, task['task']) \
                if not user_task else not hasattr(self.additional_tasks, task['task'])
            if task_not_exist or user_task_not_exists:
                exc_error = s_config.no_task_error.format(task_name=task['task'], module_name=self.module_name)
                raise Exception(exc_error)
                sys.exit(10)
            f_task = getattr(self.additional_tasks, task['task']) if user_task else getattr(Tasks, task['task'])
            f_task(self.module_name, task, self.configs, self.results)



        os.chdir(project_location)

    def get_results(self):
        return self.results
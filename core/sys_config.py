import os
percents_output = "<<{0}>>"

# Modules settings
modules_location = "core{sep}modules{sep}{{module_name}}{sep}".format(sep=os.path.sep)
modules_py_mod_location = 'core.modules.{module_name}.{file}'

additional_tasks_file = "tasks"
tasks_list_file = "tasks_list"

default_modules_build_path = "core{sep}modules{sep}{{module_name}}{sep}build{sep}".format(sep=os.path.sep)


# errors

no_file_error = 'File {file_name} wasn\'t found'
no_module_error = 'Module {module_name} wasn\'t found ({full_path})'
no_task_error = 'Can\'t find task {task_name} in module {module_name}'
no_external_program_error = 'Program "{program_name}" wasn\'t found on your computer. Please check PATH variable'
no_module_param_error = 'Module {module_name} required param {param_name}'
no_module_local_param_error = 'Error in module: {module_name}. Required local param {param_name}'
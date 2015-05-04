import os

percents_output = "<<{0}>>"

tools_directory = os.path.abspath('Tools')
log_folder = 'log'
# Modules settings
modules_location = os.path.join("core", "modules", "{module_name}")
modules_py_mod_location = 'core.modules.{module_name}.{file}'

additional_tasks_file = "tasks"
tasks_list_file_old = "tasks_list"

tasks_list_file = "tasks_list_new"

module_prepare_function = 'build'
module_integration_function = 'integration'
# errors

no_file_error = 'File {file_name} wasn\'t found'
no_module_error = 'Module {module_name} wasn\'t found ({full_path})'
no_task_error = 'Can\'t find task {task_name} in module {module_name}'
no_external_program_error = 'Program "{program_name}" wasn\'t found on your computer. Please check PATH variable'
no_module_param_error = 'Module {module_name} required param {param_name}'
no_module_local_param_error = 'Error in module: {module_name}. Required local param {param_name}'
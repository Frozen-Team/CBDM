import os
import sys

from core import sys_config
from core.Dependencies.library_module import LibraryModule
from core.Tasks import vcs, fs
import core.common_defs as defs
import core.cbdm_repositories as repos

help_message = defs.load_message('cbdm_module_help')


def exec_command():
    if len(sys.argv) < 3:
        print(help_message)
        sys.exit(1)
    command = sys.argv[2]
    modules = sys.argv[3::]
    if command == 'install':
        for module_name in modules:
            if LibraryModule.module_exists(module_name):
                print('Module "{}" already in system. Skipping'.format(module_name))
                continue
            module_params = repos.find_module(module_name)
            if not bool(module_params):
                print('Module "{}" wasnt\'t found'.format(module_name))
                continue
            module_repo = module_params['repo']
            module_dir = sys_config.modules_location.format(module_name=module_name)
            vcs.git_clone(module_repo, module_dir)
            print('----- Module {} was successfully installed'.format(module_name))
        sys.exit(0)
    elif command == 'delete':
        for module_name in modules:
            if LibraryModule.module_exists(module_name):
                fs.remove(LibraryModule.get_module_location(module_name))
        sys.exit(0)
    elif command == 'list':
        modules_dir = os.path.join('core', 'modules')
        modules = [o for o in os.listdir(modules_dir) if o != '__pycache__' and
                   os.path.isdir(os.path.join(modules_dir, o))]
        print(" , ".join(modules))
        sys.exit(0)
    elif command == 'is_builded':
        for module_name in modules:
            module = LibraryModule(module_name, {'rebuild': False})
            print(module_name + " - " + ("Not builded" if str(module.module_need_rebuild()) else "Builded"))
            sys.exit(1)
    elif command == 'build':
        params = sys.argv[4::]
        building_params = {'rebuild': True}
        for param in params:
            param = param.split('=')
            if len(param) < 2:
                continue
            key = param[0]
            value = '='.join(param[1::])
            building_params[key] = value
        module_name = modules[0]
        module = LibraryModule(module_name, building_params)
        module.prepare()
    elif command == 'show_results':
        module_name = modules[0]
        module = LibraryModule(module_name, {'rebuild': False})
        module.prepare()
        print(module.write_results())
    elif command == 'exists':
        for module_name in modules:
            print(module_name + " - " + ("Exists" if LibraryModule.module_exists(module_name) else "No module"))
    else:
        print(help_message)
        sys.exit(1)
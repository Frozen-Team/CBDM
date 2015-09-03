import json
import os
import sys
import config
import core.common_defs as defs
import core.cbdm_repositories as repos
from core import sys_config
from core.dependencies.library_module import LibraryModule
from core.tasks import vcs, fs




help_message = defs.load_message('tools_help')

tools_manager_path = os.path.join(config.directories['project_dir'], 'core', 'tools_manager')
repos_filename = os.path.join(tools_manager_path, 'tools_repositories.json')


def get_tool_path(name=''):
    if name != '':
        return os.path.join(tools_manager_path, name)
    else:
        return os.path.join(tools_manager_path, 'new_module')


def get_tool_info_path(name=''):
    return os.path.join(get_tool_path(name), 'info.json')


def add_tool(module_url):
    # TODO: Check if module already in repository list
    tool_info_path = get_tool_info_path()
    clone_path = get_tool_path()

    if os.path.exists(clone_path):
        fs.remove(clone_path)

    vcs.git_clone(module_url, clone_path)

    if not os.path.exists(tool_info_path):
        defs.critical('Cannot add tool: Invalid tool repository', -1)

    tool_name = ''
    version = ''
    with open(tool_info_path, 'r') as info_file:
        info = json.load(info_file)
        if all(t in info for t in ('type', 'name', 'version')):
            if not info['type'] == 'tool':
                defs.critical('Cannot add tool: Is not a tool', -2)
            tool_name = info['name']
            version = info['version']
        else:
            defs.critical('Cannot add tool: Invalid tool info', -3)
    if tool_name == '' or version == '':
        defs.critical('Cannot add tool: Invalid tool info', -4)

    tool_path = get_tool_path(tool_name)
    if os.path.exists(tool_path):
        fs.remove(tool_path)

    # TODO: Improve checks if destination path is exists in fs.rename()
    fs.rename(clone_path, tool_path)
    parsed = {}
    #  TODO: Json parser\dumper as class
    try:
        with open(repos_filename, 'r') as info_file:
            loaded = info_file.read()
            if loaded == '':
                loaded = '{}'
            parsed = json.loads(loaded)
    except IOError as e:
        defs.critical('I/O error({0}): {1}'.format(e.errno, e.strerror), -5)
    except:
        defs.critical('Unexpected error: {0}'.format(sys.exc_info()[0]), -100)

    try:
        with open(repos_filename, 'w') as info_file:
            new_tool_info = {'url': module_url, 'installed': 'False', 'version': version}
            parsed[tool_name] = new_tool_info
            json.dump(parsed, info_file, indent=4, sort_keys=True)
    except IOError as e:
        defs.critical('I/O error({0}): {1}'.format(e.errno, e.strerror), -6)
    except:
        defs.critical('Unexpected error: {0}'.format(sys.exc_info()[0]), -7)


def remove_tool(name):
    print('remove_tool')


def install_tool(name):
    print('install_tool')


def uninstall_tool(name):
    print('uninstall_tool')

def update_tool(name):
    print('update tool')

def tool_version(name):
    print('Version')


def tools_exec():
    args_count = len(sys.argv)
    if args_count < 4 or args_count > 4:
        print(help_message)
        sys.exit(1)

    command = sys.argv[2]
    param = sys.argv[3]

    if command == 'add':
        add_tool(param)
    elif command == 'remove':
        remove_tool(param)
    elif command == 'install':
        install_tool(param)
    elif command == 'uninstall':
        uninstall_tool(param)
    elif command == 'update':
        update_tool(param)
    elif command == 'version':
        tool_version(param)
    else:
        print('Undefined command: ' + command + '\n')
        print(help_message)
        sys.exit(1)





    modules = sys.argv[3::]
    # if command == 'install':
    #     for module_name in modules:
    #         if LibraryModule.module_exists(module_name):
    #             print('Module "{}" already in system. Skipping'.format(module_name))
    #             continue
    #         module_params = repos.find_module(module_name)
    #         if not bool(module_params):
    #             print('Module "{}" wasnt\'t found'.format(module_name))
    #             continue
    #         module_repo = module_params['repo']
    #         module_dir = sys_config.modules_location.format(module_name=module_name)
    #         vcs.git_clone(module_repo, module_dir)
    #         print('----- Module {} was successfully installed'.format(module_name))
    #     sys.exit(0)
    # elif command == 'delete':
    #     for module_name in modules:
    #         if LibraryModule.module_exists(module_name):
    #             fs.remove(LibraryModule.get_module_location(module_name))
    #     sys.exit(0)
    # elif command == 'list':
    #     modules_dir = os.path.join('core', 'modules')
    #     modules = [o for o in os.listdir(modules_dir) if o != '__pycache__' and
    #                os.path.isdir(os.path.join(modules_dir, o))]
    #     print(" , ".join(modules))
    #     sys.exit(0)
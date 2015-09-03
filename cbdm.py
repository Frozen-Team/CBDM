import sys

import config
from core.CmakeGenerator import CmakeGeneratorFromDeps as CMakeGenerator
import core.cbdm_repositories as repos
import core.cbdm_modules as modules
import core.common_defs as defs
import core.tools_manager.tools_manager as tools_manager
from core.dependencies.dependencies import Dependencies
from core.env_project_install import project_install_to_env

tools_manager.add_tool('https://github.com/Frozen-Team/cbdm-7z-tool')

# help_message = defs.load_message('help')
#
# if len(sys.argv) > 1:
#     command = sys.argv[1]
#     if command == 'module':
#         modules.exec_command()
#         sys.exit(0)
#     elif command == 'repos':
#         repos.exec_command()
#         sys.exit(0)
#     elif command == 'tools':
#         tools_manager.tools_exec()
#         sys.exit(0)
#     elif command == 'build':
#         pass
#     else:
#         print(help_message)
#         sys.exit(0)
#
# dependencies = Dependencies()
# dependencies.build_dependencies()
# project_install_to_env()
#
# cmakeBuilder = CMakeGenerator(config.directories['solutionDir'], config.projectName,
#                               dependencies.get_results())
# cmakeBuilder.set_target_name('test_project')
# cmakeBuilder.is_executable()
# cmakeBuilder.set_files_masks(['*.cpp'])
# cmakeBuilder.generate()


# TODO CMake builder
# cmakeBuilder.cmake_file.run()



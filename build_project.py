# encoding: utf8
import os
import sys
import config
# from core.cmake import Cmake
from core.Dependencies.dependencies import Dependencies

# For very IMPORTANT!!!! purposes
# def recursively_delete_files_from_folder(directory):
#     extensions = []
#     for root, dirnames, filenames in os.walk(directory):
#         for filename in filenames:
#             fileName, fileExtension = os.path.splitext(filename)
#             if fileExtension not in extensions:
#                 extensions.append(fileExtension)
#     print(extensions)
# recursively_delete_files_from_folder('.')

dependencies = Dependencies(config.dependencies)
dependencies.build_dependencies()



# cmake = Cmake(config.directories["solutionDir"], dependencies.modules_results)
# cmake.save()
# cmake.run()
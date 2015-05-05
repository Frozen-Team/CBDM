# encoding: utf8
import time
# from core.cmake import Cmake
from core.Dependencies.dependencies import Dependencies

# For very IMPORTANT!!!! purposes
# def recursively_delete_files_from_folder(directory):
# extensions = []
# for root, dirnames, filenames in os.walk(directory):
# for filename in filenames:
#             fileName, fileExtension = os.path.splitext(filename)
#             if fileExtension not in extensions:
#                 extensions.append(fileExtension)
#     print(extensions)
# recursively_delete_files_from_folder('.')
starts = int(time.time())
dependencies = Dependencies()
dependencies.build_dependencies()
ends = int(time.time())
print('starts on {}. Ends on {}. Total seconds: {}'.format(starts, ends, ends - starts))


# cmake = Cmake(config.directories["solutionDir"], dependencies.modules_results)
# cmake.save()
# cmake.run()
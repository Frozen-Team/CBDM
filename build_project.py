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
ends = time.time()
total = ends - starts
print("""
===== ALL TASKS COMPLETED SUCCESSFULLY =====


Starts on {}.
Ends on {}.
Total: {}""".format(time.ctime(starts), time.ctime(ends), time.strftime('%H:%M:%S', time.gmtime(total))))


# cmake = Cmake(config.directories["solutionDir"], dependencies.modules_results)
# cmake.save()
# cmake.run()
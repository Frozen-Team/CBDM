# encoding: utf8
import os
import sys
import config
# from core.cmake import Cmake
from core.Dependencies.dependencies import Dependencies

dependencies = Dependencies(config.dependencies)
dependencies.build_dependencies()


# cmake = Cmake(config.directories["solutionDir"], dependencies.modules_results)
# cmake.save()
# cmake.run()
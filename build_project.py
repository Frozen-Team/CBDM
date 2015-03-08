# encoding: utf8
import config
from core.cmake import Cmake
from core.dependencies import Dependencies
Deps = Dependencies(config.dependencies)
Deps.build_dependencies()

cmake = Cmake(Deps.modules_results)

cmake.build()
cmake.run()
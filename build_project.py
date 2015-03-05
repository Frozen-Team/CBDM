# encoding: utf8
import config
from core.cmake import Cmake
from core.dependencies import Dependencies

Deps = Dependencies(config.dependencies)
Deps.build_dependencies()
cmake = Cmake(sources_dir=config.directories["solutionDir"],
              project_name=config.projectName,
              build_dir=config.directories["buildDir"],
              cmake_version=config.cmakeVersion,
              dependencies=Deps.modules_results
              )
cmake.build()
cmake.run()
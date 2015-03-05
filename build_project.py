# encoding: utf8
import config
from core.cmake import Cmake
from core.dependencies import Dependencies

DPS = Dependencies(config.dependencies)
DPS.build_dependencies()
CM = Cmake(sources_dir=config.directories["solutionDir"],
           build_dir=config.directories["buildDir"],
           cmake_version=config.cmakeVersion
           )
CM.build()
CM.run()
# for dep_name, params in dependencies.items():

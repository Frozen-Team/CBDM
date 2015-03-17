# encoding: utf8
import config
from core.cmake import Cmake
<<<<<<< HEAD
from core.Dependencies.dependencies import Dependencies

=======
from core.dependencies import Dependencies
>>>>>>> bfa307ac3ef8ddccef6b9be52825cd7d8edc3f51
dependencies = Dependencies(config.dependencies)
dependencies.build_dependencies()


<<<<<<< HEAD
=======

>>>>>>> bfa307ac3ef8ddccef6b9be52825cd7d8edc3f51
cmake = Cmake(config.directories["solutionDir"], dependencies.modules_results)
cmake.save()
cmake.run()
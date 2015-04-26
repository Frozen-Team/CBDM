import os
from config import directories
from core.default_structures import cleanup_extensions

repository_dir = "sources"
glew_path = os.path.join(directories["downloadDir"], 'glew.zip')
build_tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "download_file",
     "destination": glew_path,
     "url": "https://sourceforge.net/projects/glew/files/glew/{version}/glew-{version}.zip/download"},
    {"task": "unzip", "file_location": glew_path, "destination": 'Lib'},
    {"task": "make",
     "output_dir": 'build',
     "vcxproj_file": "Lib/glew-{version}/build/vc12/glew_static.vcxproj",
     "makefile": "sources/glew-{version}/Makefile",
     "linux_dependencies": {
         "Ubuntu": ['libx11-dev', 'freeglut3-dev']
     },
     "params": {
         "SYSTEM": 'Windows',
         'GLEW_DEST': 'libs'
     }
     },
    {"task": "rdfff", "directory": "Lib", "extensions": cleanup_extensions["c++"], 'description': 'Cleaning up trash..'}
]
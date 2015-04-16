import os
from config import directories

repository_dir = "sources"
glew_path = os.path.join(directories["downloadDir"], 'glew.zip')
build_tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "https://github.com/glfw/glfw.git", "sources_dir": repository_dir},
    {"task": "git_checkout", "sources_dir": repository_dir, "branch": "glew-{version}"},
    {"task": "configure", "directory": "glew-{version}/", "params": {"a": 1, "b": 2}},
    {"task": "make",
     "output_dir": 'build',
     "vcxproj_file": "glew-{version}/vc12/glew_static.vcxproj",
     "makefile": "glew-{version}/Makefile"},
    {"task": "make_install", "directory": "glew-{version}/", "params": {"a": 1, "b": 2}},
]


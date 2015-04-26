import os
from config import directories

v8_path = directories["libFolder"] + os.path.sep
download_path = os.path.join(directories["downloadDir"], 'depot_tools.zip')
gyp_path = directories["libFolder"] + "{0}build{0}gyp".format(os.path.sep)
build_tasks = [
    # {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    # {"task": "git_clone", "repository": "https://chromium.googlesource.com/chromium/tools/depot_tools.git",
    #  "sources_dir": v8_path},

    # {"task": "git_clone", "repository": "https://chromium.googlesource.com/external/gyp/{}", "sources_dir": gyp_path},
    # {"task": "download_file",
    #  "destination": download_path,
    #  "url": "https://src.chromium.org/svn/trunk/tools/depot_tools.zip"},
    # {"task": "un_7_zip", "file_location": download_path, "destination": v8_path},

    # {"task": "prepare_v8", "user_task": True},
    {"task": "git_checkout", "sources_dir": v8_path, "branch": "{version}"},
    {"task": "generate_v8_project", "architecture": "x64", "user_task": True},
    {"task": "make",
     "output_dir": 'build',
     "vcxproj_file": "glew-{version}/vc12/glew_static.vcxproj",
     "makefile": "glew-{version}/Makefile"},

    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
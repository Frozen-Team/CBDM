import os
from config import directories

v8_path = directories["libFolder"] + "/"
download_path = os.path.join(directories["downloadDir"], 'depot_tools.zip')
gyp_path = directories["libFolder"] + "/build/gyp"
tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "https://chromium.googlesource.com/chromium/tools/depot_tools.git",
     "sources_dir": v8_path},
    # {"task": "git_checkout", "sources_dir": v8_path, "branch": "{version}"},
    # {"task": "git_clone", "repository": "https://chromium.googlesource.com/external/gyp/{}", "sources_dir": gyp_path},
    # {"task": "download_file",
    #  "destination": download_path,
    #  "url": "https://src.chromium.org/svn/trunk/tools/depot_tools.zip"},
    # {"task": "un_7_zip", "file_location": download_path, "destination": 'Tools'},
    # {"task": "generate_v8_project", "user_task": True},

    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
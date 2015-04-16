import os
from config import directories

boost_path = os.path.join(directories["downloadDir"], 'boost.7z')
libFolder = directories["libFolder"] + "/"
full_path = os.path.abspath(".")
tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    # {"task": "download_file", "destination": boost_path,
    #  "url": "http://sourceforge.net/projects/boost/files/boost/1.57.0/boost_{version}.7z/download"},
    # {"task": "un_7_zip", "file_location": boost_path, "destination": libFolder},
    # {'task': 'rename_boost', 'user_task': True},
    # {"task": "set_boost_var", "user_task": True}
    {"task": "build_boost", "user_task": True}

    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
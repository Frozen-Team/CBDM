import os
from config import directories

glm_path = os.path.join(directories["downloadDir"], 'glm.zip')
build_tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    {"task": "download_file",
     "destination": glm_path,
     "url": "http://sourceforge.net/projects/ogl-math/files/glm-{version}/glm-{version}.zip/download"},
    {"task": "un_7_zip", "file_location": glm_path, "destination": 'Lib'},
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
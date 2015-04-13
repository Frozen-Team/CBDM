import os
from config import directories

fmod_path = os.path.join(directories["downloadDir"], 'fmod.exe')
tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "download_file", "destination":  fmod_path,
     "url": "http://www.fmod.org/download/fmodstudio/api/Win/fmodstudioapi{version}win-installer.exe"},
    {"task": "un_7_zip", "file_location": fmod_path, "destination": directories["libFolder"] + "/"},
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
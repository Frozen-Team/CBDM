import os
from config import directories

fbxsdk_path = os.path.join(directories["downloadDir"], 'fbx.exe')
libFolder = directories["libFolder"] + "/"
build_tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    {"task": "download_file", "destination": fbxsdk_path,
     "url": "http://images.autodesk.com/adsk/files/fbx{version}_fbxsdk_vs2013_win.exe"},
    {"task": "un_7_zip", "file_location": fbxsdk_path, "destination": libFolder},
    {"task": "move_files", "from_path": libFolder + "/$_OUTDIR", "to_path": "Lib/"}
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
import os
from config import directories

p7z_arch_path = os.path.join(directories["downloadDir"], '7z.zip')
build_tasks = [
    {"task": "download_file", "destination": p7z_arch_path,
     "url": "http://www.7-zip.org/a/7za920.zip"},
    {"task": "unzip", "file_location": p7z_arch_path, "destination": directories["tools_path"] + "/"},
]
import os
from config import directories

build_tasks = [
    {"task": "download_file",
     "destination": 'git.exe',
     "url": "https://dl.dropboxusercontent.com/u/92011034/git.zip", "description": "Downloading..."},
    {"task": "unzip", "file_location": 'git.exe', "destination": directories['tools_path'] + '/git/',
     "description": "Extracting..."},
]
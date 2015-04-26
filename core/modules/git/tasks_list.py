from config import directories

build_tasks = [
    {"task": "download_file",
     "destination": 'git.zip',
     "url": "https://dl.dropboxusercontent.com/u/92011034/git.zip", "description": "Downloading..."},
    {"task": "unzip", "file_location": 'git.zip', "destination": directories['tools_path'] + '/git/',
     "description": "Extracting..."},
]
integration_tasks = [
    {'task': 'add_path_to_git', 'user_taske': True}
]
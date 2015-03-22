repository_dir = "sources"
tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "download_file",
     "destination": 'sources.zip',
     "url": "https://sourceforge.net/projects/glew/files/glew/{version}/glew-{version}.zip/download"},
    {"task": "unzip", "file_location": "sources.zip", "destination": 'sources'},
    {"task": "make",
     "output_dir": 'build',
     "vcxproj_file": "glew-{version}/vc12/glew_static.vcxproj",
     "makefile": "sources/glew-{version}/Makefile",
     "linux_dependencies": {
        "Ubuntu":['libx11-dev', 'freeglut3-dev']
     },
     "params": {
         "SYSTEM": 'linux',
         'GLEW_DEST': 'libs'
     }
     }
]
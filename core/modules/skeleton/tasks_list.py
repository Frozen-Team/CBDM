repository_dir = "sources"
tasks = [
    {"task": "test", "user_task": True},
    {"task": "check_dependencies", "programs": ['git', '7z'], "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "git://git.frozen-team.com/Glew.git", "sources_dir": repository_dir},
    {"task": "git_checkout", "sources_dir": repository_dir, "branch": "glew-{version}"},
    {"task": "configure", "directory": "glew-{version}/", "params": {"a": 1, "b": 2}},
    {"task": "make",
     "output_dir": 'build',
     "vcxproj_file": "glew-{version}/vc12/glew_static.vcxproj",
     "makefile": "glew-{version}/Makefile"},
    {"task": "make_install", "directory": "glew-{version}/", "params": {"a": 1, "b": 2}},

    {"task": "add_library", "config": ("linux", "x86", "debug"), "library_location": "/Debug/x64/glew32sd.lib"},
    {"task": "add_location", "location": "/Debug/x64/glew32sd.lib"},
    {"task": 'remove_file_by_mask', 'mask': '*.c'},
    # {"task": "download_file", "url": "http://nodejs.org/dist/v0.12.0/node-v0.12.0.tar.gz", "destination": "node.tar.gz"},
    # {"task": "download_file", "url": "https://sourceforge.net/projects/glew/files/glew/1.12.0/glew-1.12.0.zip/download",
    #  "destination": "test.zip"},
    # {"task": "download_file", "url": "http://tiny.cc/4ogrvx", "destination": "test.7z"},

    # uncompress
    # {"task": "untar", "file_location": "node.tar.gz"},
    # {"task": "unzip", "file_location": "test.zip", "destination": None},
    # {"task": "un_7_zip", "file_location": "test.7z", "destination": "test-7z/test/test/test"},
]
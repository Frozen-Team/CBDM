repository_dir = "sources"
tasks = [
    {"task": "test", "user_task": True},
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "git://git.frozen-team.com/Glew.git", "sources_dir": repository_dir},
    {"task": "git_checkout", "sources_dir": repository_dir, "branch": "glew-{version}"},
    # {"task": "compile", "vcxproj_file": "build/vc12/glew_static.vcxproj", "makefile": "build/Makefile"},
    {"task": "add_library", "config": ("linux", "x86", "debug"), "library_location": "/Debug/x64/glew32sd.lib"},
    {"task": "add_location", "location": "/Debug/x64/glew32sd.lib"},
    {"task": "download_file", "url": "http://glew.sourceforge.net/glew.png", "destination": "icon.jpg"},
    # {"task": "download_file", "url": "https://sourceforge.net/projects/glew/files/glew/1.12.0/glew-1.12.0.zip/download",
    #  "destination": "test.zip"},
    {"task": "unzip", "file_location": "test.zip", "destination": None}


]
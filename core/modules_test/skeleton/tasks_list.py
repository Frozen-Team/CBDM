repository_dir = "sources"
tasks = [
    {"task": "test", "user_task": True},
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "git://git.frozen-team.com/Glew.git", "sources_dir": repository_dir},
    {"task": "git_checkout", "sources_dir": repository_dir, "branch": "glew-{version}"},
    # {"task": "compile", "vcxproj_file": "build/vc12/glew_static.vcxproj", "makefile": "build/Makefile"},
    {"task": "add_library", "config": ("linux", "x86", "debug"), "library_location": "/Debug/x64/glew32sd.lib"},
    {"task": "add_location", "location": "/Debug/x64/glew32sd.lib"},
]
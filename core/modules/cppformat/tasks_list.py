from config import directories

cppformat_path = directories["libFolder"] + "/"
build_tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "https://github.com/cppformat/cppformat.git", "sources_dir": cppformat_path},
    {"task": "git_checkout", "sources_dir": cppformat_path, "branch": "{version}"},
    {"task": "cmake_generate", "sources_dir": cppformat_path, "destination_dir": cppformat_path + "Win32",
     "architecture": "Win32", },
    {"task": "cmake_generate", "sources_dir": cppformat_path, "destination_dir": cppformat_path + "Win64",
     "architecture": "Win64", },
    {"task": "make", "vcxproj_file": cppformat_path + "Win32/format.vcxproj"},
    {"task": "make", "vcxproj_file": cppformat_path + "Win64/format.vcxproj"}
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
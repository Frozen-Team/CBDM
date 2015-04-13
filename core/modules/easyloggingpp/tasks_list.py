from config import directories

easyloggingpp_path = directories["libFolder"] + "/"
tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "https://github.com/easylogging/easyloggingpp.git", "sources_dir":
        easyloggingpp_path},
    {"task": "git_checkout", "sources_dir": easyloggingpp_path, "branch": "{version}"},
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
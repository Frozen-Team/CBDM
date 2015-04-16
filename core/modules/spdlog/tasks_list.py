from config import directories

spdlog_path = directories["libFolder"] + "/"
build_tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "git_clone", "repository": "https://github.com/gabime/spdlog.git", "sources_dir": spdlog_path},
    {"task": "git_checkout", "sources_dir": spdlog_path, "branch": "{version}"},
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
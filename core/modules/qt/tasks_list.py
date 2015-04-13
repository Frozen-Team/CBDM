import os
from config import directories

qt_x86_path = os.path.join(directories["downloadDir"], 'qt_x86.7z')
qt_x64_path = os.path.join(directories["downloadDir"], 'qt_x64.7z')
qt_vs_addin_path = os.path.join(directories["downloadDir"], 'qt_vs_addin.exe')
libFolder = directories["libFolder"] + "/"
tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "download_file", "destination": qt_vs_addin_path,
     "url": "http://download.qt.io/official_releases/vsaddin/qt-vs-addin-1.2.4-opensource.exe"},
    {"task": "install_addin_user", "exec_path": qt_vs_addin_path, 'user_task': True},
    {"task": "download_file", "destination": qt_x86_path,
     "url": "http://download.qt.io/online/qtsdkrepository/windows_x86/desktop/qt5_54/qt.54.win32_msvc2013/"
            "{version}qt5_essentials.7z"},
    {"task": "un_7_zip", "file_location": qt_x86_path, "destination": libFolder},
    {"task": "download_file", "destination": qt_x64_path,
     "url": "http://download.qt.io/online/qtsdkrepository/windows_x86/desktop/qt5_54/qt.54.win64_msvc2013_64/"
            "{version}qt5_essentials.7z"},
    {"task": "un_7_zip", "file_location": qt_x64_path, "destination": libFolder},
    # {"task": "add_location", "location": "eigen_sources/Eigen/src/"},
]
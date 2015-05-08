import os
import subprocess
import re
from core.Tasks import check_dependencies, fs, net, archives
from config import directories
from core.common_defs import is_windows

qt_archive = 'qt.7z'
build_directory = os.path.abspath(os.path.join(directories['buildDir'], 'qt'))
qt_vs_addin_path = 'qt_vs_addin.exe'
qt_x64_path = 'http://download.qt.io/online/qtsdkrepository/windows_x86/desktop/qt{0}_{1}/qt.{1}.win64_msvc2013_64/' \
              '{2}qt5_essentials.7z'
qt_x86_path = 'http://download.qt.io/online/qtsdkrepository/windows_x86/desktop/qt{0}_{1}/qt.{1}.win32_msvc2013/' \
              '{2}qt5_essentials.7z'


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    version = module_params['version']
    major_version = re.match('^[0-9]+', version).group(0)
    mm_version = str(re.match('^[0-9]+\.[0-9]+', version).group(0)).replace('.', '')
    fs.remove(build_directory)

    if is_windows():
        print('This may take a while')
        net.download_file(qt_x64_path.format(major_version, mm_version, version), qt_archive)
        archives.extract_7_zip(qt_archive, build_directory)
        net.download_file(qt_x64_path.format(major_version, mm_version, version), qt_archive)
        archives.extract_7_zip(qt_archive, build_directory)

        net.download_file('http://download.qt.io/official_releases/vsaddin/qt-vs-addin-1.2.4-opensource.exe',
                          qt_vs_addin_path)
        print('Running Qt Visual Studio Addin installer')
        if os.path.exists(qt_vs_addin_path):
            subprocess.call([qt_vs_addin_path], shell=True)
        else:
            raise Exception('Cannot find Qt VS Addin installer')
            sys.exit(80)

        fs.remove(qt_archive)
        fs.remove(qt_vs_addin_path)
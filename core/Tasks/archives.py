import os
from shutil import which
from zipfile import ZipFile
import subprocess
from core.tools.seven_z import SevenZ

__author__ = 'saturn4er'
import core.Tasks.fs as fs


def extract_zip(archive, destination=''):
    fs.create_path_to(destination)
    print('Extract by zip: %s -> %s' % (archive, destination))
    with ZipFile(archive, 'r') as archive:
        archive.extractall(destination)


def extract_7_zip(archive, destination):
    print('Extract by 7z: %s -> %s' % (archive, destination))
    s_z_file = SevenZ(archive)
    s_z_file.extract(destination)


def extract_tar(archive, destination):
    archiver_loc = which('tar')
    if not os.path.exists(destination):
        os.makedirs(destination)
    if archiver_loc is None:
        raise Exception("TAR IS NOT INSTALLED ON SYSTEM")
        sys.exit(1)
    exec_command = [archiver_loc, '-xzf', archive]
    if destination:
        exec_command.extend('-C "{}"'.format(destination))
    subprocess.Popen(" ".join(exec_command), shell=True).communicate()
import os
from shutil import which
from zipfile import ZipFile
import subprocess
from core import sys_config
from core.tools.seven_z import SevenZ

__author__ = 'saturn4er'
import core.Tasks.fs as fs


def extract_zip(archive, destination=''):
    fs.require_full_path(destination)
    print('Extract by zip: %s -> %s' % (archive, destination))
    with ZipFile(archive, 'r') as archive:
        archive.extractall(destination,)


def extract_7_zip(archive, destination=False):
    if not bool(destination):
        destination = './'
    print('Extract by 7z: %s -> %s' % (archive, destination))
    s_z_file = SevenZ(archive)
    s_z_file.extract(destination)


def extract_tar(archive, destination=False):
    archiver_loc = which('tar')
    if not os.path.exists(destination):
        os.makedirs(destination)
    if archiver_loc is None:
        raise Exception("TAR IS NOT INSTALLED ON SYSTEM")
        sys.exit(1)
    exec_command = [archiver_loc, '-xzvf', archive]
    log_filename = os.path.join(sys_config.log_folder, 'untar.log')
    fs.require_full_path(log_filename)
    if destination:
        exec_command.append('-C "{}"'.format(destination))
    with open(log_filename, 'a+') as log_file:
        process = subprocess.Popen(" ".join(exec_command), shell=True, stdout=log_file, stderr=log_file)
        process.communicate()
        if process.returncode:
            raise Exception("TAR EXTRACTION WAS FINISHED WITH CODE: " + str(process.returncode))
            sys.exit(1)
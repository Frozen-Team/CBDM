import os
import subprocess

from core import sys_config
from core.Dependencies.library_module import LibraryModule
from core.Tasks import fs


class SevenZ:
    seven_z_built = False
    seven_z_path = ''

    def __init__(self, archive_name):
        self.path_to_7z = SevenZ.install_7z()
        self.archive_name = archive_name

    def extract(self, destination):

        if not os.path.isfile(self.archive_name):
            raise Exception("Archive is not exist")

        if not os.path.isdir(destination):
            os.makedirs(destination)

        exec_command = '{archiver} x "{location}" -o"{destination}" -y'.format(archiver=self.path_to_7z,
                                                                               location=self.archive_name,
                                                                               destination=destination)
        log_filename = os.path.join(sys_config.log_folder, '7z.log')
        fs.create_path_to(log_filename)
        with open(log_filename, 'w+') as log_file:
            process = subprocess.Popen(exec_command, shell=True, stdout=log_file, stderr=log_file)
            process.communicate()
            result_code = process.returncode
            if result_code != 0:
                raise Exception("Extracting file error")

    @staticmethod
    def install_7z():
        if not SevenZ.seven_z_built:
            install_module = LibraryModule('7z', {'rebuild': True})
            install_module.prepare()
            SevenZ.seven_z_build = True
            SevenZ.seven_z_path = install_module.write_results()['path']
        return SevenZ.seven_z_path
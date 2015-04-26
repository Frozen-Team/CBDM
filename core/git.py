import os
import subprocess
import re
import sys

import core.Dependencies.library_module as l_m


class Repo:
    program_builded = False
    program_path = ''

    def __init__(self, directory, log_file=None):
        self.git_path = Repo.install_git()
        self.directory = os.path.abspath(directory)
        self.rel_dir = directory
        self.log_std = open(log_file, 'w') if log_file else open(os.devnull)

    @staticmethod
    def install_git():
        if not Repo.program_builded:
            install_module = l_m.LibraryModule('git', {'rebuild': False})
            install_module.run_tasks()
            Repo.program_builded = True
            Repo.program_path = install_module.get_results()['path']
        return Repo.program_path

    def is_repo(self):
        return os.path.isdir(self.directory + os.path.sep + ".git")

    def get_branches(self):
        if not self.is_repo():
            raise Exception("Not a repository(" + os.path.abspath(self.directory) + ")")
            sys.exit(1)
        process = subprocess.Popen([self.git_path, 'branch'], cwd=self.directory, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()
        result = re.findall('([a-zA-Z0-9./=-]+?)\\n', out.decode())
        process = subprocess.Popen([self.git_path, 'tag'], cwd=self.directory, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()
        result.extend(re.findall("([a-zA-Z0-9./=-]+?)\\n", out.decode()))
        return result

    def branch_exists(self, branch_name):
        return branch_name in self.get_branches()

    def clone(self, repository):
        if os.path.exists(self.rel_dir):
            print("Repository folder already exists({0})".format(self.directory))
            return
        clone_command = [self.git_path, 'clone', repository, '"{0}"'.format(self.rel_dir)]
        subprocess.call(" ".join(clone_command), stdout=self.log_std, stderr=self.log_std, shell=True)

    def checkout(self, branch):
        if not self.branch_exists(branch):
            raise Exception('Trying to checkout to not existing branch({0})'.format(branch))
            sys.exit(1)
        subprocess.call([self.git_path, 'checkout', branch], stdout=self.log_std, stderr=self.log_std, cwd=self.directory, shell=True)


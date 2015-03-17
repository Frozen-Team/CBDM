<<<<<<< HEAD
import os
import subprocess
import re
import sys
import shutil


class Repo:
    def __init__(self, directory, log_file=None):
        # TODO: download git if not installed
        if shutil.which('git') is None:
            raise Exception("GIT IS NOT INSTALLED ON SYSTEM")
            sys.exit(1)
        self.directory = os.path.abspath(directory)
        self.rel_dir = directory
        self.log_std = open(log_file, 'w') if log_file else open(os.devnull)

    def is_repo(self):
        return os.path.exists(self.directory + '\\.git')

    def get_branches(self):
        if not self.is_repo():
            raise Exception("Not a repository(" + os.path.abspath(self.directory) + ")")
            sys.exit(1)
        branches_str = subprocess.check_output(['git', 'branch'], cwd=self.directory, shell=True).decode()
        result = re.findall('([a-zA-Z0-9./=-]+?)\\n', branches_str)
        tags_str = subprocess.check_output(['git', 'tag'], cwd=self.directory, shell=True).decode()
        result.extend(re.findall('([a-zA-Z0-9./=-]+?)\\n', tags_str))
        return result

    def branch_exists(self, branch_name):
        return branch_name in self.get_branches()

    def clone(self, repository):
        if os.path.exists(self.rel_dir):
            print("Repository folder already exists({0})".format(self.directory))
            return
        clone_command = ['git', 'clone', repository, '"{0}"'.format(self.rel_dir)]
        subprocess.call(" ".join(clone_command), stdout=self.log_std, stderr=self.log_std, shell=True)

    def checkout(self, branch):
        if not self.branch_exists(branch):
            raise Exception('Trying to checkout to not existing branch({0})'.format(branch))
            sys.exit(1)
        subprocess.call(['git', 'checkout', branch], stdout=self.log_std, stderr=self.log_std, cwd=self.directory, shell=True)

=======
__author__ = 'Ярослав'
import os
import subprocess
import re
import sys
import shutil


class Repo:
    def __init__(self, directory, log_file=None):
        # TODO: download git if not installed
        if shutil.which('git') is None:
            raise Exception("GIT IS NOT INSTALLED ON SYSTEM")
            sys.exit(1)
        self.directory = os.path.abspath(directory)
        self.rel_dir = directory
        self.log_std = open(log_file, 'w') if log_file else open(os.devnull)

    def is_repo(self):
        return os.path.exists(self.directory + '\\.git')

    def get_branches(self):
        if not self.is_repo():
            raise Exception("Not a repository(" + os.path.abspath(self.directory) + ")")
            sys.exit(1)
        branches_str = subprocess.check_output(['git', 'branch'], cwd=self.directory, shell=True).decode()
        result = re.findall('([a-zA-Z0-9./=-]+?)\\n', branches_str)
        tags_str = subprocess.check_output(['git', 'tag'], cwd=self.directory, shell=True).decode()
        result.extend(re.findall('([a-zA-Z0-9./=-]+?)\\n', tags_str))
        return result

    def branch_exists(self, branch_name):
        return branch_name in self.get_branches()

    def clone(self, repository):
        if os.path.exists(self.rel_dir):
            print("Repository folder already exists({0})".format(self.directory))
            return
        clone_command = ['git', 'clone', repository, '"{0}"'.format(self.rel_dir)]
        subprocess.call(" ".join(clone_command), stdout=self.log_std, stderr=self.log_std, shell=True)

    def checkout(self, branch):
        if not self.branch_exists(branch):
            raise Exception('Trying to checkout to not existing branch({0})'.format(branch))
            sys.exit(1)
        subprocess.call(['git', 'checkout', branch], stdout=self.log_std, stderr=self.log_std, cwd=self.directory, shell=True)

>>>>>>> bfa307ac3ef8ddccef6b9be52825cd7d8edc3f51

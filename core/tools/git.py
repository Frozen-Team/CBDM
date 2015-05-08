import os
import subprocess
import re
import sys

import core.Dependencies.library_module as l_m
from core.Tasks import fs


class Repo:
    program_built = False
    program_path = ''

    def __init__(self, directory, log_file=None):
        self.git_path = Repo.install_git()
        self.directory = os.path.abspath(directory)
        self.rel_dir = directory
        fs.require_full_path(log_file)
        self.log_std = open(log_file, 'a+') if log_file else open(os.devnull)

    @staticmethod
    def install_git():
        if not Repo.program_built:
            install_module = l_m.LibraryModule('git', {'rebuild': False})
            install_module.prepare()
            Repo.program_built = True
            Repo.program_path = install_module.get_results()['path']
        return Repo.program_path

    def is_repo(self):
        return os.path.isdir(self.directory + os.path.sep + '.git')

    def get_branches(self):
        if not self.is_repo():
            raise Exception('Not a repository(' + os.path.abspath(self.directory) + ')')
            sys.exit(1)
        get_branches_command = ' '.join([self.git_path, 'branch'])
        process = subprocess.Popen(get_branches_command, cwd=self.directory, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()
        result = re.findall('([a-zA-Z0-9./=-]+?)\\n', out.decode())
        get_tags_command = ' '.join([self.git_path, 'tag'])
        process = subprocess.Popen(get_tags_command, cwd=self.directory, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()
        result.extend(re.findall('([a-zA-Z0-9./=-]+?)\\n', out.decode()))
        return result

    def branch_exists(self, branch_name):
        return branch_name in self.get_branches()

    def clone(self, repository):
        if os.path.exists(self.rel_dir):
            print('Repository folder already exists({0})'.format(self.directory))
            return
        clone_command = ' '.join([self.git_path, 'clone', repository, self.rel_dir])
        process = subprocess.Popen(clone_command, stderr=self.log_std, stdout=self.log_std, shell=True)
        process.communicate()

    def checkout(self, branch):
        if not self.branch_exists(branch):
            raise Exception('Trying to checkout to not existing branch({0})'.format(branch))
            sys.exit(1)
        command = ''.join([self.git_path, 'checkout', branch])
        subprocess.Popen(command, stdout=self.log_std, stderr=self.log_std,
                        cwd=self.directory, shell=True)


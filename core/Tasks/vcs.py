import os
from shutil import rmtree

from core.tools.git import Repo
import core.sys_config as s_config

__author__ = 'saturn4er'

log_file = os.path.join(s_config.log_folder, 'git.txt')

def git_clone(repo, repo_dir='', overwrite=True):
    print('Cloning {repo} to {repo_dir}'.format(repo=repo, repo_dir=repo_dir))
    repository = Repo(repo_dir, log_file)
    if repository.is_repo() and overwrite:
        rmtree(repo_dir, ignore_errors=False)
    repository.clone(repo)


def git_checkout(repo_dir, branch):
    repository = Repo(repo_dir, log_file)
    repository.checkout(branch)
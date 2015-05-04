from shutil import rmtree
from core.Dependencies.library_module_new import LibraryModule
from core.tools.git import Repo
import core.Tasks.fs as fs

__author__ = 'saturn4er'


def git_clone(repo, repo_dir='', overwrite=True):
    print('Cloning {repo} to {repo_dir}'.format(repo=repo, repo_dir=repo_dir))
    repository = Repo(repo_dir, LibraryModule.current_working_module + '_git.log')
    if repository.is_repo() and overwrite:
        rmtree(repo_dir, ignore_errors=False)
    repository.clone(repo)


def git_checkout(repo_dir, branch):
    repository = Repo(repo_dir, LibraryModule.current_working_module + '_git.log')
    repository.checkout(branch)
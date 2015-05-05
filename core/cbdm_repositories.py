import os
import sys
import urllib.request as net
import json

import core.common_defs as defs


help_message = defs.load_message('cbdm_respositories_help')
import argparse
import config

parser = argparse.ArgumentParser(description='Process some integers.')
repos_filename = os.path.join(config.directories['project_dir'], 'core', 'Dependencies', 'repositories.json')


def find_module(module_name):
    repos = get_repos()
    for repo in repos:
        try:
            repo_stream = net.urlopen(repo)
            repo_modules = json.loads(repo_stream.read().decode())
            if module_name in repo_modules and 'repo' in repo_modules[module_name]:
                return repo_modules[module_name]
        except:
            print('Problems with repo: ' + repo)
    return False


def get_repos():
    try:
        with open(repos_filename, 'r') as repos_file:
            repos = repos_file.read()
            repos_list = json.loads(repos)
    except FileNotFoundError:
        repos_list = []
    return repos_list


def write_repos(repos):
    with open(repos_filename, 'w+') as repos_file:
        repos_file.write(json.dumps(repos))


def validate_repo(repo):
    try:
        net.urlopen(repo)
    except:
        return False
    return True


def exec_command():
    if len(sys.argv) < 4:
        print(help_message)
        sys.exit(1)
    command = sys.argv[2]
    repo_url = sys.argv[3]

    print(repos_filename)
    if command == 'add':

        repos = get_repos()
        if repo_url in repos:
            print('Repository already in system')
            sys.exit(1)
        if not validate_repo(repo_url):
            print('Bad repository')
            sys.exit(1)
        repos.append(repo_url)
        write_repos(repos)
        print('Repository was successfully added to system')
        sys.exit(0)

    elif command == 'remove':
        repos = get_repos()
        if repo_url not in repos:
            print('Repository not in system')
            sys.exit(1)
        repos.remove(repo_url)
        write_repos(repos)
        sys.exit(0)
    else:
        print(help_message)
        sys.exit(1)
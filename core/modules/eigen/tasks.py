from glob import glob
import os
import sys


def rename_sources_dir(module_name, task_params, module_params, result):
    sources_dir = glob('eigen-eigen-*')
    if len(sources_dir) == 0:
        raise Exception('No directories like "eigen-eigen-*"')
        sys.exit(5)
    if len(sources_dir) > 1:
        raise Exception('More than one folder with name "eigen-eigen-*"')
        sys.exit(5)
    sources_dir = sources_dir[0]
    os.rename(sources_dir, 'eigen_sources')
from urllib.request import urlretrieve

__author__ = 'saturn4er'

import core.Tasks.fs as fs


def download_file(url, destination=''):
    print('Downloading file %s to %s' % (url, destination))
    fs.create_path_to(destination)
    urlretrieve(url, destination)
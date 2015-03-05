__author__ = 'Ярослав'
import os, subprocess


class Git:
    @staticmethod
    def clone(repository, destination):
        subprocess.call(['git', 'clone', repository, destination])

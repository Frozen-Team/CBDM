from errno import EEXIST
from shutil import which, rmtree
import sys
import subprocess
import shutil
import os
import platform

from config import directories, cmakeGenerator
from core.tools.git import Repo
from core.modules.cmake.tasks_list import cmake_exe_path
import core.sys_config as s_config
from core.tools.vcxproj import Builder




















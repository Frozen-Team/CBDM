from glob import glob
import os
import sys
import shutil
from config import directories


def cleanup_tools(module_name, task_params, module_params, result):
    shutil.rmtree(directories["tools_path"] + "/")
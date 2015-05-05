# encoding: utf8
import time
import sys

import core.cbdm_modules as modules
import core.common_defs as defs
from core.Dependencies.dependencies import Dependencies


help_message = defs.load_message('help')
if len(sys.argv) < 2:
    print(help_message)
    sys.exit(1)

if sys.argv[1] == 'module':
    modules.exec_command()
sys.exit(1)

starts = int(time.time())
dependencies = Dependencies()
dependencies.build_dependencies()
ends = time.time()
total = ends - starts
print("""
===== ALL TASKS COMPLETED SUCCESSFULLY =====


Starts on {}.
Ends on {}.
Total: {}""".format(time.ctime(starts), time.ctime(ends), time.strftime('%H:%M:%S', time.gmtime(total))))

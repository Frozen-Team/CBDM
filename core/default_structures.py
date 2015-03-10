import core.sys_config as cconfig
import os
default_dependency_struct = {"libs": {
    "x64": {
        "debug": "",  # can be also a list
        "release": "",  # can be also a list
    },
    "x32": {
        "debug": "",  # can be also a list
        "release": "",  # can be also a list
    }
},
                             "headers": "",  # could be a list
                             "cmake_before": "",
                             "cmake_after": ""
}
module_config = {
    "version": 0,
    "build_path": os.path.realpath(cconfig.default_modules_build_path),
    "rebuild": False
}
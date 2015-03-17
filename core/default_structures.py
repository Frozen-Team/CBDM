import core.sys_config as cconfig
import os

default_dependency_struct = {"libs": {
    "linux": {
        "x64": {
            "debug": [],
            "release": [],
        },
        "x86": {
            "debug": [],
            "release": [],
        }
    },
    'windows': {
        "x64": {
            "debug": [],
            "release": [],
        },
        "x86": {
            "debug": [],
            "release": [],
        }
    }
},
                             "headers": [],
                             "cmake_before": "",
                             "cmake_after": ""
}
module_config = {
    "version": 0,
    "build_path": os.path.realpath(cconfig.default_modules_build_path),
    "rebuild": False
}

def build(params):
    return {
        "libs": {
            "x64": {
                "debug": "realpath_to_debug_x64_lib",  # can be also a list
                "release": "realpath_to_release_x32_lib",  # can be also a list
            },
            "x32": {
                "debug": "realpath_to_debug_x32_lib",  # can be also a list
                "release": "realpath_to_release_x32_lib",  # can be also a list
            },
        },
        "headers": "first headers folder"  # could be a list
    }


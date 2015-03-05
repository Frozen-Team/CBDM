def build(params):
    return {
        "libs": {
            "x64": {
                "debug": "realpath_to_debug_x64_lib",
                "release": "realpath_to_release_x32_lib",
            },
            "x32": {
                "debug": "realpath_to_debug_x32_lib",
                "release": "realpath_to_release_x32_lib",
            },
        },
        "headers": ["first headers folder", "second header folder"]  # could be a string
    }


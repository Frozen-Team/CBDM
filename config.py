import os

directories = {
    "solutionDir": "D:/Development/Script/Solution",
    "downloadDir": "Download",
    "libFolder": "Lib",
    "buildDir": "Build",
    "visualStudioDir": "C:/Program Files (x86)/Microsoft Visual Studio 12.0",
    "tools_path": os.path.abspath("Tools"),
    "project_dir": os.getcwd()
}

projectName = "FrozenEngine"
cmakeVersion = "3.1.3"
cmakeGenerator = "Visual Studio 12 2013"
buildArchitecture = "x64"  # x86 | x32
dependencies = {
    #
    # "cleanup": {
    # 'index': 0
    # },

    # DONE
    # "git": {
    # 'rebuild': True
    # },

    # DONE
    # "sqlite": {
    #     'rebuild': True,
    #     'version': '3080900'
    # },

    # DONE
    # "cmake": {
    #     'index': 0,
    #     "version": "3.2.1",
    #     'rebuild': True
    # },

    # DONE
    # "qt": {
    # "version": "5.4.1-0",
    # 'rebuild': True
    # },

    # DONE
    "glew": {
        "version": "1.12.0",
        'rebuild': True
    },

    # DONE
    # "FMOD": {
    #     "version": "10600",
    #     'rebuild': True
    # },

    # DONE
    # "eigen": {
    #     "version": "3.2.4",
    #     'rebuild': True
    # },

    # DONE
    # "glfw": {
    #     "version": "3.1.1",
    #     'rebuild': True
    # },

    # DONE
    # "cppformat": {
    #     "version": "1.1.0",
    #     'rebuild': True
    # },

    # DONE
    # "spdlog": {
    #     "version": "master",
    #     'rebuild': True
    # },

    # DONE
    # "easyloggingpp": {
    #     "version": "v9.80",
    #     'rebuild': True
    # },

    # DONE
    # "freeimage": {
    #     "version": "3170",
    #     'rebuild': True
    # },

    # Use from FreeImage
    # "zlib"

    # DONE
    # "freetype": {
    #     "version": "2.5.5",
    #     'rebuild': True
    # }

    # DONE
    # "glm": {
    #     "version": "0.9.6.3",
    #     'rebuild': True
    # }

    # DONE
    # "fbxsdk": {
    #     "version": "20151",
    #     'rebuild': True
    # }

    # DONE
    # "boost": {
    #     "version": "1_57_0",
    #     'rebuild': True
    # }

    # "v8": {
    #     "version": "4.4.16",
    #     'rebuild': True
    # }

    # sqlite
    # assimp
    # GLraw
    # freetype-gl




    # "skeleton": {
    #     "version": "1.12.0",
    #     'rebuild': True
    # },


    # 'module_skeleton': {
    # "version": "version",
    # "build_path": "build_pat",
    # "rebuild": True
    # }
}

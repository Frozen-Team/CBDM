import os

directories = {
    "solutionDir": os.path.abspath("test_project"),
    "solution_third_party_dir": os.path.abspath('test_project/3dparty'),
    "buildDir": os.path.abspath("Build"),
    "visualStudioDir": "H:\Applications\Visual Studio 13",
    "tools_path": os.path.abspath("Tools"),
    "project_dir": os.getcwd()
}

projects = {
    'audio': {
        'dir': os.path.join('test_project', 'src', 'audio'),
        'files': ['*.cpp'],
        'include_dirs': [],

        'have_own_cmake': False
    }
}

projectName = "FrozenEngine"
cmakeVersion = "3.1.3"
cmakeGenerator = "Visual Studio 12"
buildArchitecture = "x64"  # x86 | x64

visual_studio_toolset = 'v120'
visual_studio_runtime_library = 'MD'

dependencies = {

    # DONE
    # "sqlite": {
    #     'type': 'static',
    #     'version': '3080900',
    #     'rebuild': False
    # },
    #
    # # DONE
    # # "qt": {
    # # "version": "5.4.1-0",
    # # 'rebuild': True
    # # },
    #
    # DONE
    # "glew": {
    #     "version": "1.12.0",
    #     'rebuild': False
    # },
    #
    # # Finished
    # "FMOD": {
    # "version": "10600",
    # 'rebuild': True
    # },
    #
    "sdl": {
        'major_version': 2,
        "version": '2.0.3',
        # 'rebuild': True
    },
    # # DONE
    # "eigen": {
    # "version": "3.2.4",
    #     'rebuild': False
    # },

    # # DONE
    # "glfw": {
    # "version": "3.1.1",
    #     'rebuild': True
    # },
    #
    # # DONE
    # "cppformat": {
    #     "version": "1.1.0",
    #     'rebuild': True
    # },
    #
    # # DONE
    # "spdlog": {
    #     "version": "master",
    #     'rebuild': True
    # },
    #
    # # DONE
    # "easyloggingpp": {
    #     "version": "v9.80",
    #     'rebuild': True
    # },
    #
    # # DONE
    # "freeimage": {
    #     "version": "3170",
    #     'rebuild': True
    # },
    #
    # # DONE
    # "freetype": {
    #     "version": "2.5.5",
    #     'rebuild': True
    # },
    #
    #
    # # DONE
    # "glm": {
    #     "version": "0.9.6.3",
    #     'rebuild': False
    # },
    #
    # # DONE
    # "fbxsdk": {
    #     "version": "20151",
    #     'rebuild': True
    # },

    # DONE
    # "boost": {
    # "version": "1_57_0",
    # 'rebuild': True
    # }

    # "v8": {
    # "version": "4.4.16",
    #     'rebuild': True
    # }
}

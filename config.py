import os

directories = {
    'solutionDir': 'D:/Development/CppDepManager/Solution',
    'downloadDir': 'Download',
    'libFolder': 'Lib',
    'buildDir': os.path.abspath('Build'),
    'visualStudioDir': 'C:\Program Files (x86)\Microsoft Visual Studio 12.0',
    'tools_path': os.path.abspath('Tools'),
    'project_dir': os.getcwd()
}

projectName = 'FrozenEngine'
cmakeVersion = '3.2.2'
cmakeGenerator = 'Visual Studio 12'
buildArchitecture = 'x64'  # x86 | x32
visual_studio_toolset = 'v120'
visual_studio_runtime_library = 'MD'

dependencies = {
    'sqlite': {
        'rebuild': False,
        'version': '3081001'
    },

    'glew': {
        'version': '1.12.0',
        'rebuild': False
    },

    'FMOD': {
        'version': '10602',
        'rebuild': False
    },

    'eigen': {
        'version': '3.2.4',
        'rebuild': False
    },

    'cppformat': {
        'version': '1.1.0',
        'rebuild': False
    },

    'easyloggingpp': {
        'version': 'v9.80',
        'rebuild': False
    },

    'freeimage': {
        'version': '3170',
        'rebuild': False
    },

    'freetype': {
        'version': '2.5.5',
        'rebuild': False
    },

    # 'fbxsdk': {
    #     'version': '20151',
    #     'rebuild': False
    # },

    'sdl': {
        'version': '2.0.3',
        'major_version': 2,
        'rebuild': False
    },

    'boost': {
        'version': '1.58.0',
        'rebuild': True
    },

    # 'v8': {
    #     'version': '4.4.16',
    #     'rebuild': False
    # },

    # 'qt': {
    #     'version': '5.4.1-0',
    #     'rebuild': False
    # },
}

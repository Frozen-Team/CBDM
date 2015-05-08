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
cmakeVersion = '3.1.3'
cmakeGenerator = 'Visual Studio 12'
buildArchitecture = 'x64'  # x86 | x32

visual_studio_toolset = 'v120'
visual_studio_runtime_library = 'MD'

dependencies = {

    # Finished
    # 'sqlite': {
    # 'rebuild': True,
    # 'version': '3080900'
    # },
    #
    # Finished
    # 'glew': {
    # 'version': '1.12.0',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'FMOD': {
    #     'version': '10600',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'eigen': {
    #     'version': '3.2.4',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'glfw': {
    #     'version': '3.1.1',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'cppformat': {
    #     'version': '1.1.0',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'spdlog': {
    #     'version': 'master',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'easyloggingpp': {
    #     'version': 'v9.80',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'freeimage': {
    #     'version': '3170',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'freetype': {
    #     'version': '2.5.5',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'glm': {
    #     'version': '0.9.6.3',
    #     'rebuild': True
    # },
    #
    # Finished
    # 'fbxsdk': {
    #     'version': '20151',
    #     'rebuild': True
    # },

    # Finished
    # 'boost': {
    #     'version': '1.58.0',
    #     'rebuild': True
    # }
    #
    'v8': {
        'version': '4.4.16',
        'rebuild': True
    }
    # Finished
    # 'qt': {
    #     'version': '5.4.1-0',
    #     'rebuild': True
    # },
}

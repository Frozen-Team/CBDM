import os
from config import directories

origin_dir = 'Origin'
fmod_path = 'fmod.exe'
build_directory = os.path.join(directories['buildDir'], 'fmod')
build_tasks = [
    {'task': 'check_dependencies', 'params': ['version'], 'description': 'Checking dependencies'},
    {'task': 'download_file', 'destination':  fmod_path,
     'url': 'http://www.fmod.org/download/fmodstudio/api/Win/fmodstudioapi{version}win-installer.exe',
     'description': 'Downloading FMOD'},
    {'task': 'un_7_zip', 'file_location': fmod_path, 'destination': origin_dir, 'description': 'Extracting FMOD'},

    {'task': 'rename_folder_by_mask', 'mask': os.path.join(origin_dir, 'api'), 'destination': build_directory,
     'overwrite': True,
     'description': 'Moving headers to build directory'},
    {'task': 'remove_file_by_mask', 'mask': origin_dir, 'description': 'Cleaning up trash'},
    {'task': 'remove_file_by_mask', 'mask': fmod_path, 'description': 'Removing downloaded file'}
]

integration_tasks = [
    {'task': 'add_location', 'location': os.path.join(build_directory, 'fsbank', 'inc'),
     'description': 'Adding fsbank headers location'},
    {'task': 'add_location', 'location': os.path.join(build_directory, 'lowlevel', 'inc'),
     'description': 'Adding lowlevel headers location'},
    {'task': 'add_location', 'location': os.path.join(build_directory, 'studio', 'inc'),
     'description': 'Adding studio headers location'},

    # TODO: Think about attaching fsbank
    # x86
    {'task': 'add_library', 'config': ('windows', 'x86', 'release'), 'library_location':
        os.path.join(build_directory, 'lowlevel', 'lib', 'fmod_vc.lib'),
     'description': 'Adding x86 lowlevel release lib'},
    {'task': 'add_library', 'config': ('windows', 'x86', 'debug'), 'library_location':
        os.path.join(build_directory, 'lowlevel', 'lib', 'fmodL_vc.lib'),
     'description': 'Adding x86 lowlevel debug lib'},

    # x64
    {'task': 'add_library', 'config': ('windows', 'x64', 'release'), 'library_location':
        os.path.join(build_directory, 'lowlevel', 'lib', 'fmod64_vc.lib'),
     'description': 'Adding x64 lowlevel release lib'},
    {'task': 'add_library', 'config': ('windows', 'x64', 'debug'), 'library_location':
        os.path.join(build_directory, 'lowlevel', 'lib', 'fmodL64_vc.lib'),
     'description': 'Adding x64 lowlevel debug lib'},


    # x86
    {'task': 'add_library', 'config': ('windows', 'x86', 'release'), 'library_location':
        os.path.join(build_directory, 'studio', 'lib', 'fmodstudio_vc.lib'),
     'description': 'Adding x86 studio release lib'},
    {'task': 'add_library', 'config': ('windows', 'x86', 'debug'), 'library_location':
        os.path.join(build_directory, 'studio', 'lib', 'fmodstudioL_vc.lib'),
     'description': 'Adding x86 studio debug lib'},

    # x64
    {'task': 'add_library', 'config': ('windows', 'x64', 'release'), 'library_location':
        os.path.join(build_directory, 'studio', 'lib', 'fmodstudio64_vc.lib'),
     'description': 'Adding x64 studio release lib'},
    {'task': 'add_library', 'config': ('windows', 'x64', 'debug'), 'library_location':
        os.path.join(build_directory, 'studio', 'lib', 'fmodstudioL64_vc.lib'),
     'description': 'Adding x64 studio debug lib'},
]
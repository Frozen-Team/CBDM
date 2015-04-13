import os
from config import directories

repository_dir = "sources"
freeimage_path = os.path.join(directories["downloadDir"], 'freeimage.zip')
tasks = [
    {"task": "check_dependencies", "programs": ['git'], "params": ("version", 'rebuild')},
    {"task": "download_file",
     "destination": freeimage_path,
     "url": "http://downloads.sourceforge.net/freeimage/FreeImage{version}.zip"},
    {"task": "unzip", "file_location": freeimage_path, "destination": 'Lib'},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/FreeImage.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/FreeImageLib/FreeImageLib.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/LibJPEG/LibJPEG.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/LibJXR/LibJXR.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/LibOpenJPEG/LibOpenJPEG.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/LibPNG/LibPNG.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/LibRawLite/LibRawLite.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/LibTIFF4/LibTIFF4.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/LibWebP/LibWebP.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/OpenEXR/OpenEXR.2013.vcxproj"},
    {"task": "check_runtime_library", "vcxproj_file": "Lib/FreeImage/Source/ZLib/ZLib.2013.vcxproj"},

    {"task": "make",
     "output_dir": 'build',
     "vcxproj_file": "Lib/FreeImage/FreeImage.2013.vcxproj",
     "makefile": "Lib/FreeImage/Makefile",
     "params": {
         "SYSTEM": 'Windows',
         'GLEW_DEST': 'libs'
     }
     }
]
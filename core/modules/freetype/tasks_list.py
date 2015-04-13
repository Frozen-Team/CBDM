import os
from config import directories

freetype_path = os.path.join(directories["downloadDir"], 'freetype.zip')
freetype_vcxproj = "Lib/freetype-{version}/builds/windows/vc2010/freetype.vcxproj"
tasks = [
    {"task": "check_dependencies", "params": ("version", 'rebuild')},
    {"task": "download_file",
     "destination": freetype_path,
     "url": "http://download.savannah.gnu.org/releases/freetype/freetype-{version}.tar.gz"},
    {"task": "un_7_zip", "file_location": freetype_path, "destination": 'Download'},
    {"task": "un_7_zip", "file_location": directories["downloadDir"] + "/freetype", "destination": 'Lib'},
    {"task": "check_runtime_library", "vcxproj_file": freetype_vcxproj},
    {"task": "make",
     "output_dir": 'build',
     "vcxproj_file": freetype_vcxproj,
     "makefile": "Lib/freetype-{version}/Makefile",
     },
]
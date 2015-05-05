import os

from config import directories
import config
from core.common_defs import is_windows
from core.default_structures import cleanup_extensions
from core.Tasks import check_dependencies, fs, net, archives, cmake, assembly


freeimage_path = 'freeimage.zip'
origin_dir = 'Origin'
build_directory = os.path.join(directories['buildDir'], 'freeimage')
lib_directory = os.path.join(build_directory, 'lib')
headers_dir = os.path.join(build_directory, 'include')


def build(module_params):
    check_dependencies(False, ['version'], module_params)
    fs.remove(origin_dir)
    freeimage_url = 'http://downloads.sourceforge.net/freeimage/FreeImage{version}.zip'.format(
        version=module_params['version'])
    net.download_file(freeimage_url, freeimage_path)
    archives.extract_zip(freeimage_path)
    fs.rename('FreeImage', origin_dir)
    fs.remove(freeimage_path)
    vcxproj_to_change = ('FreeImage.2013.vcxproj',
                         'Source/FreeImageLib/FreeImageLib.2013.vcxproj',
                         'Source/LibJPEG/LibJPEG.2013.vcxproj',
                         'Source/LibJXR/LibJXR.2013.vcxproj',
                         'Source/LibOpenJPEG/LibOpenJPEG.2013.vcxproj',
                         'Source/LibPNG/LibPNG.2013.vcxproj',
                         'Source/LibRawLite/LibRawLite.2013.vcxproj',
                         'Source/LibTIFF4/LibTIFF4.2013.vcxproj',
                         'Source/LibWebP/LibWebP.2013.vcxproj',
                         'Source/OpenEXR/OpenEXR.2013.vcxproj',
                         'Source/ZLib/ZLib.2013.vcxproj'
                         )
    print('Be patient. Freeimage compiling for a long time.')
    if is_windows():
        for vcxproj_file in vcxproj_to_change:
            vcxproj_file = os.path.join(origin_dir, vcxproj_file)
            assembly.set_vcxproj_platform_toolset(vcxproj_file, config.visual_studio_toolset)
            assembly.set_vcxproj_runtime_library(vcxproj_file, config.visual_studio_runtime_library)

        assembly.build_vcxproj(os.path.join(origin_dir, 'FreeImage.2013.vcxproj'), lib_directory)

    fs.rename(os.path.join(origin_dir, 'Source'), headers_dir, True)
    fs.clear(origin_dir, cleanup_extensions['c++'])


def integration(module_params):
    cmake.add_location(headers_dir)
    if is_windows():
        # x86
        cmake.add_library(('windows', 'x86', 'release'),
                          os.path.join(lib_directory, 'Release', 'Win32', 'FreeImage.lib'))
        cmake.add_library(('windows', 'x86', 'debug'), os.path.join(lib_directory, 'Debug', 'Win32', 'FreeImaged.lib'))
        # x64
        cmake.add_library(('windows', 'x64', 'release'), os.path.join(lib_directory, 'Release', 'x64', 'FreeImage.lib'))
        cmake.add_library(('windows', 'x64', 'debug'), os.path.join(lib_directory, 'Debug', 'x64', 'FreeImaged.lib'))
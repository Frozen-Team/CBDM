import os, glob
import subprocess


class Cmake:
    def __init__(self, sources_dir, build_dir, cmake_version):
        self._sourcesDir = sources_dir
        self._buildDir = build_dir
        self._cmakeVersion = cmake_version
        self._additionalFlags = {}

    @staticmethod
    def find_sources(sources_dir, relative_path=False):
        if not relative_path:
            relative_path = sources_dir
        files = glob.glob(sources_dir + "/*.h")
        files.extend(glob.glob(sources_dir + "/*.cpp"))
        full_path_files = [os.path.relpath(file_name, relative_path) for file_name in files]
        return full_path_files

    @staticmethod
    def set(var_name, var_value, file_handler):
        file_handler.writelines("set({0} {1}){2}".format(var_name, var_value, os.linesep))

    def set_flag(self, flag_name, flag_value):
        self._additionalFlags[flag_name] = flag_value

    def get_flags_string(self):
        format_flag = lambda f_name, f_val: "-{0}={1}".format(f_name, f_val)
        return " ".join([format_flag(flag, value) for flag, value in self._additionalFlags.iteritems()])

    def build(self):
        f = open(self._sourcesDir + '/CMakeLists.txt', 'w+')
        f.writelines("cmake_minimum_required(VERSION {0}){1}".format(self._cmakeVersion, os.linesep))
        self.set("CMAKE_RUNTIME_OUTPUT_DIRECTORY", "bin", f)
        main_project_files = self.find_sources(self._sourcesDir)
        self.set("SOURCES_FILES", " ".join(main_project_files), f)
        f.close()

    def run(self):

        source_directory = os.path.relpath(self._sourcesDir, "build")
        current_working_dir = os.getcwd()

        # changing working directory for change cmake output dir
        if not os.path.exists(self._buildDir):
            os.mkdir(self._buildDir, 666)
        os.chdir(self._buildDir)

        subprocess.call(['cmake', self.get_flags_string(), source_directory])

        # return to previous dir
        os.chdir(current_working_dir)

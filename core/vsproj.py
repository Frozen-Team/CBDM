from xml.dom import minidom
import re, os
import subprocess
import config


class VcprojConfiguration():
    def __init__(self, file_location, xml_root, arch=False, conf_name=False):
        self.file_loc = file_location
        self.xml_root = xml_root
        self.arch = arch
        self.conf_name = conf_name

    def get_configuration(self, configuration_name):
        return VcprojConfiguration(self.file_loc, self.xml_root, self.arch, configuration_name)

    def get_architecture(self, arch):
        return VcprojConfiguration(self.file_loc, self.xml_root, arch, self.conf_name)

    def set_runtime_librarie(self, config):
        for item in self._get_items():
            item.getElementsByTagName('RuntimeLibrary')[0].childNodes[0].nodeValue = config

    def save(self):
        self.xml_root.writexml(open(self.file_loc, 'w'), )

    def _get_items(self):
        reg_exp = self.conf_name if self.conf_name else '(.+?)'
        reg_exp += '\|'
        reg_exp += self.arch if self.arch else '(.+?)'
        reg_exp = re.compile(reg_exp)
        result = []
        for item in self.xml_root.getElementsByTagName("ItemDefinitionGroup"):
            cond = item.attributes['Condition'].value
            if not reg_exp.search(cond) is None:
                result.append(item)
        return result


class Vcproj:
    runtimeLibraries = {
        "MT": "MultiThreaded",
        "MTd": "MultiThreadedDebug",
        "MD": "MultiThreadedDLL",
        "MDd": "MultiThreadedDebugDLL",
    }

    def __init__(self, file_location):
        self.file_loc = os.path.abspath(file_location)
        self.xml_root = minidom.parse(file_location)

    def build(self, configurations=False, archs=False, output=False, rebuild=False, log_file=False):
        if not configurations:
            configurations = self.get_configurations_list()
        if not archs:
            archs = self.get_arch_list()
        vs_path = config.directories["visualStudioDir"]

        commands = ["@echo off"]
        build_command = "msbuild"
        build_command += " /t:Rebuild " if rebuild else ""
        if output is not False:
            output += "/{configuration}/{platform}/"
            build_command += " /p:OutDir=\"{0}\" ".format(os.path.abspath(output))
        build_command += "/p:Configuration=\"{configuration}\" /p:Platform=\"{platform}\" \"" + self.file_loc + "\""
        for arc_index, arch in enumerate(archs):
            commands.append('call "{vs_path}/VC/vcvarsall.bat" x86_amd64'.format(vs_path=os.path.abspath(vs_path)))
            for conf_index, configuration in enumerate(configurations):
                commands.append(build_command.format(configuration=configuration, platform=arch))
        bat_file = open('build.bat', 'w')
        bat_file.writelines(os.linesep.join(commands))
        bat_file.close()
        output = open(str(log_file), 'w') if log_file else open(os.devnull, 'w')
        subprocess.call('call build.bat', stderr=output, stdout=output, shell=True)
        os.system('call build.bat')
        os.remove('build.bat')


    def get_configuration(self, configuration_name):
        return VcprojConfiguration(self.file_loc, self.xml_root, conf_name=configuration_name)

    def get_architecture(self, arch):
        return VcprojConfiguration(self.file_loc, self.xml_root, arch=arch)

    def get_configurations_list(self):
        result = set()
        for item in self.xml_root.getElementsByTagName('Configuration'):
            result.add(item.childNodes[0].nodeValue)
        return result

    def get_arch_list(self):
        result = set()
        for item in self.xml_root.getElementsByTagName('Platform'):
            result.add(item.childNodes[0].nodeValue)
        return result
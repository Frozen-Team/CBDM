import core.sys_config as cconfig
import os


default_dependency_struct = {
    "link_directories": {},
    "libs": {},
    "headers": [],
    "cmake_before": "",
    "cmake_after": ""
}
cleanup_extensions = {
    'c++': ['', '.py', '.pyc', '.sample', '.idx', '.pack', '.iml', '.xml', '.ini', '.zip', '.chm', '.exe', '.txt',
            '.log', '.bat', '.yml', '.mk', '.rst', '.cc', '.python', '.css', '.html', '.conf', '.bii', '.cmake',
            '.vcxproj', '.filters', '.sdf', '.sln', '.suo', '.check_cache', '.bin', '.cxx', '.stamp', '.depend',
            '.list', '.c', '.obj', '.tlog', '.lastbuildstate', '.cpp', '.rule', '.lib', '.md', '.00', '.01',
            '.02', '.03', '.04', '.05', '.06', '.07', '.08', '.09', '.10', '.11', '.12', '.13', '.14', '.15', '.16',
            '.17', '.18', '.19', '.20', '.21', '.22', '.23', '.24', '.25', '.26', '.27', '.28', '.29', '.30', '.31',
            '.32', '.33', '.34', '.35', '.36', '.37', '.38', '.39', '.40', '.41', '.42', '.43', '.44', '.45', '.46',
            '.47', '.48', '.49', '.50', '.51', '.52', '.53', '.54', '.55', '.56', '.57', '.58', '.59', '.60', '.61',
            '.62', '.63', '.64', '.65', '.66', '.67', '.68', '.69', '.70', '.71', '.72', '.73', '.74', '.75', '.76',
            '.77', '.78', '.79', '.80', '.sh', '.dev', '.layout', '.bmp', '.pro', '.ui', '.user',
            '.BSD', '.GPL', '.LGPL', '.MINPACK', '.MPL2', '.README', '.in', '.cxxlist', '.main', '.dtd', '.f', '.dat',
            '.natvis', '.dox', '.js', '.png', '.plist', '.less', '.svg', '.m', '.pc', '.7z', '.settings', '.codereview',
            '.gclient', '.git-cl', '.testing', '.google', '.gif', '.mp3', '.p12', '.cfg', '.json', '.doctest', '.so',
            '.tex', '.old', '.yaml', '.pem', '.vbs', '.chromium', '.portable', '.rtf', '.crt', '.dll', '.def',
            '.manifest', '.cmd', '.bash', '.ico', '.tcl', '.pl', '.pm', '.al', '.pub', '.e2x', '.pod', '.bs', '.ix',
            '.ld', '.inc', '.eg', '.lst', '.tm', '.enc', '.msg', '.terms', '.xbm', '.ppm', '.eps', '.m4', '.java',
            '.xsl', '.cgi', '.vim', '.info', '.bar', '.utf-8', '.ca', '.cs', '.cp1250', '.de', '.el', '.cp737', '.eo',
            '.es', '.fr', '.hr', '.hu', '.it', '.euc', '.sjis', '.nb', '.nl', '.no', '.pt', '.ru', '.cp1251', '.sk',
            '.sv', '.iso9', '.big5', '.cnf', '.0', '.crl', '.win32pad', '.cnt', '.hlp', '.1', '.7', '.pyd', '.pyo',
            '.pth', '.egg-info', '.egg', '.rc', '.htm', '.idl', '.sct', '.asp', '.pys', '.a', '.pyw', '.license',
            '.md5', '.sha1', '.third_party', '.pkg', '.diff', '.gn', '.strongtalk', '.v8', '.valgrind', '.android',
            '.nacl', '.3', '.2', '.4', '.5', '.6', '.8', '.9', '.gyp', '.gypi', '.S', '.asm', '.golden', '.order',
            '.sb', '.in0', '.in1', '.strings', '.xib', '.storyboard', '.mm', '.pch', '.saves', '.swift', '.ext1',
            '.ext2', '.ext3', '.xcscheme', '.z', '.props', '.vsprops', '.s', '.ext', '.assem', '.gencc', '.printvars',
            '.stdout', '.blah', '.fontified', '.pbfilespec', '.xclangspec', '.git', '.applescript', '.TXT',
            '.modulemap', '.exp', '.ipp', '.status', '.out', '.js-script', '.default', '.func-info', '.gc-state',
            '.ignore-unknown', '.separate-ic', '.pyt', '.expectation', '.ac', '.am', '.pump', '.vcproj', '.cppclean',
            '.cbproj', '.groupproj', '.xcconfig', '.pbxproj', '.X', '.tcc', '.dd', '.SKIP', '.types', '.gni',
            '.isolate', '.patch', '.guess', '.sub', '.sed', '.mak', '.res', '.nrm', '.icu', '.ucm', '.dsp', '.dsw',
            '.GDI', '.Gnome', '.template', '.xlf', '.otf', '.ksh', '.scm', '.tmpl', '.flags', '.expected', '.lua',
            '.F', '.f90', '.vsmacros', '.dsptemplate', '.pfx']
}
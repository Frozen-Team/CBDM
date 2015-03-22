def build(params):
    return {
        "cmake_before": ["find_package(OpenGL)",
                    'if (OPENGL_FOUND)',
                    '    MESSAGE("OpenGL Correctly Found")',
                    '    include_directories(${{OPENGL_INCLUDE_DIR}})',
                    '    target_link_libraries({project_name} ${{OPENGL_gl_LIBRARY}})',
                    '    target_link_libraries({project_name} ${{OPENGL_gl_LIBRARY}})',
                    'else (OPENGL_FOUND)',
                    '    MESSAGE("OpenGL environment missing")',
                    'endif (OPENGL_FOUND)']
    }




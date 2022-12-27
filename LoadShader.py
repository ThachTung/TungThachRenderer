import numpy as np
from OpenGL.GL import *

def format_vertices(coordinate, triangles):
    all_triangles = []
    for t in range(0, len(triangles), 3):
        all_triangles.append(coordinate[triangles[t]])
        all_triangles.append(coordinate[triangles[t + 1]])
        all_triangles.append(coordinate[triangles[t + 2]])
    return np.array(all_triangles, np.float32)

def compile_shader(shader_type, shader_source):
    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, shader_source)
    glCompileShader(shader_id)
    compile_success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not compile_success:
        error_messages = glGetShaderInfoLog(shader_id)
        glDeleteShader(shader_id)
        error_messages = "\n" + error_messages.decode("utf-8")
        raise Exception(error_messages)
    return shader_id

def create_shader(vertex_shader, fragment_shader):
    vertex_shader_id = compile_shader(GL_VERTEX_SHADER, vertex_shader)
    fragment_shader_id = compile_shader(GL_FRAGMENT_SHADER, fragment_shader)
    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)
    glLinkProgram(program_id)
    link_success = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not link_success:
        info = glGetProgramInfoLog(program_id)
        raise RuntimeError(info)
    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)
    return program_id


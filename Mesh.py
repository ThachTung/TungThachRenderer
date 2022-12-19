import pygame

from LoadBufferData import *
from Uniform import *

class Mesh:
    def __init__(self, shader, vertices, vertex_colors, gl_type, translation=pygame.Vector3(0, 0, 0)):
        self.vertices = vertices
        self.vertex_colors = vertex_colors
        self.gl_type = gl_type
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        position = BufferData("vec3", self.vertices)
        position.create_buffer_data(shader, "position")
        colors = BufferData("vec3", self.vertex_colors)
        colors.create_buffer_data(shader, "vertex_color")
        self.translation = Uniform("vec3", translation)
        self.translation.find_variable(shader, "translation")

    def mesh_drawing(self):
        self.translation.load()
        glBindVertexArray(self.vao)
        glDrawArrays(self.gl_type, 0, len(self.vertices))



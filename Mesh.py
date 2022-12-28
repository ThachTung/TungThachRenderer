import pygame

from LoadBufferData import *
from Uniform import *
from Transformation import *

class Mesh:
    def __init__(self, shader, vertices, vertex_normals, vertex_uvs, vertex_colors, gl_type,
                 translation=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1,0)),
                 scale=pygame.Vector3(1, 1, 1),
                 moving_rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 moving_translation=pygame.Vector3(0, 0,0),
                 moving_scale=pygame.Vector3(1, 1, 1)):
        self.shader = shader
        self.vertices = vertices
        self.vertex_normals = vertex_normals
        self.vertex_uvs = vertex_uvs
        self.vertex_colors = vertex_colors
        self.gl_type = gl_type
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        position = BufferData("vec3", self.vertices)
        position.create_buffer_data(self.shader, "position")
        colors = BufferData("vec3", self.vertex_colors)
        colors.create_buffer_data(self.shader, "vertex_color")
        v_normals = BufferData("vec3", self.vertex_normals)
        v_normals.create_buffer_data(self.shader, "vertex_normal")
        self.transformation_mat = identity_matrix()
        self.transformation_mat = rotate_mesh(self.transformation_mat, rotation.angle, rotation.axis)
        self.transformation_mat = translate(self.transformation_mat, translation.x, translation.y, translation.z)
        self.transformation_mat = scale3(self.transformation_mat, scale.x, scale.y, scale.z)
        self.transformation_projection = Uniform("mat4", self.transformation_mat)
        self.transformation_projection.find_variable(self.shader, "model_mat")
        self.moving_rotation = moving_rotation
        self.moving_translation = moving_translation
        self.moving_scale = moving_scale

    def mesh_drawing(self):
        self.transformation_mat = rotate_mesh(self.transformation_mat, self.moving_rotation.angle,
                                              self.moving_rotation.axis)
        self.transformation_mat = translate(self.transformation_mat, self.moving_translation.x, self.moving_translation.y,
                                            self.moving_translation.z)
        self.transformation_mat = scale3(self.transformation_mat, self.moving_scale.x, self.moving_scale.y,
                                              self.moving_scale.z)
        self.transformation_projection = Uniform("mat4", self.transformation_mat)
        self.transformation_projection.find_variable(self.shader, "model_mat")
        self.transformation_projection.load()
        glBindVertexArray(self.vao)
        glDrawArrays(self.gl_type, 0, len(self.vertices))



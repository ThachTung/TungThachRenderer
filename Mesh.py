import pygame

from LoadBufferData import *
from Uniform import *
from Transformation import *
from Texture import *

class Mesh:
    def __init__(self,
                 shader=None,
                 image_file=None,
                 image_normal=None,
                 image_roughness=None,
                 vertices=None,
                 vertex_normals=None,
                 vertex_uvs=None,
                 vertex_colors=None,
                 gl_type=None,
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
        if self.vertices is not None:
            position = BufferData("vec3", self.vertices)
            position.create_buffer_data(self.shader.shader, "position")
        if self.vertex_colors is not None:
            colors = BufferData("vec3", self.vertex_colors)
            colors.create_buffer_data(self.shader.shader, "vertex_color")
        if self.vertex_normals is not None:
            v_normals = BufferData("vec3", self.vertex_normals)
            v_normals.create_buffer_data(self.shader.shader, "vertex_normal")
        if self.vertex_uvs is not None:
            v_uvs = BufferData("vec2", self.vertex_uvs)
            v_uvs.create_buffer_data(self.shader.shader, "vertex_uv")
        self.transformation_mat = identity_matrix()
        self.transformation_mat = rotate_mesh(self.transformation_mat, rotation.angle, rotation.axis)
        self.transformation_mat = translate(self.transformation_mat, translation.x, translation.y, translation.z)
        self.transformation_mat = scale3(self.transformation_mat, scale.x, scale.y, scale.z)
        self.transformation_projection = Uniform("mat4", self.transformation_mat)
        self.transformation_projection.find_variable(self.shader.shader, "model_mat")
        self.moving_rotation = moving_rotation
        self.moving_translation = moving_translation
        self.moving_scale = moving_scale
        self.texture = None
        self.texture_normal = None
        self.texture_roughness = None
        if image_file is not None:
            self.image = Texture(image_file)
            self.texture = Uniform("sampler2D", [self.image.texture_id, 1])
        if image_normal is not None:
            self.image_normal = Texture(image_normal)
            self.texture_normal = Uniform("sampler2D", [self.image_normal.texture_id, 2])
        if image_roughness is not None:
            self.image_roughness = Texture(image_roughness)
            self.texture_roughness = Uniform("sampler2D", [self.image_roughness.texture_id, 3])


    def mesh_drawing(self, camera, lights):
        self.shader.use()
        camera.update(self.shader.shader)
        if lights is not None:
            for light in lights:
                light.update(self.shader.shader)
        if self.texture is not None:
            self.texture.find_variable(self.shader.shader, "tex")
            self.texture.load()
        if self.texture_normal is not None:
            self.texture_normal.find_variable(self.shader.shader, "tex_normal")
            self.texture_normal.load()
        if self.texture_roughness is not None:
            self.texture_roughness.find_variable(self.shader.shader, "tex_roughness")
            self.texture_roughness.load()
        self.transformation_mat = rotate_mesh(self.transformation_mat, self.moving_rotation.angle,
                                              self.moving_rotation.axis)
        self.transformation_mat = translate(self.transformation_mat, self.moving_translation.x, self.moving_translation.y,
                                            self.moving_translation.z)
        self.transformation_mat = scale3(self.transformation_mat, self.moving_scale.x, self.moving_scale.y,
                                              self.moving_scale.z)
        self.transformation_projection = Uniform("mat4", self.transformation_mat)
        self.transformation_projection.find_variable(self.shader.shader, "model_mat")
        self.transformation_projection.load()
        glBindVertexArray(self.vao)
        glDrawArrays(self.gl_type, 0, len(self.vertices))



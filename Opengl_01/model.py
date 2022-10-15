import numpy as np
import glm
import pygame as pg
import moderngl as mgl
import pywavefront
#import pyassimp

class Model:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        # for linux projects
        # self.texture = self.get_texture(path='Opengl_01/textures/uvchecker.jpg')
        # for windows projects
        self.texture = self.get_texture(path='Opengl_01/models/wall_c.png')
        self.normal_texture = self.get_texture(path='Opengl_01/models/wall_n.png')
        self.on_init()

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)

        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()

        # AF
        texture.anisotropy = 32.0
        return texture
    def update(self):
        rot = (0, 0, 0)
        m_model = glm.rotate(self.m_model, rot[0], glm.vec3(1, 0, 0))
        self.shader_program['m_model'].write(m_model)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['camPos'].write(self.app.camera.position)

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model

    def on_init(self):
        # light
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.Ia'].write(self.app.light.Ia)
        self.shader_program['light.Id'].write(self.app.light.Id)
        self.shader_program['light.Is'].write(self.app.light.Is)


        self.shader_program['u_texture'].value = 0
        self.shader_program['n_texture'].value = 1
        self.texture.use(location=0)
        self.normal_texture.use(location=1)
        #self.shader_program['n_texture'] = 0
        #self.array_texture[0].use(location=0)

        #

        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program,
                                    [(self.vbo, '2f 3f 3f', 'in_texcoord_0', 'in_normal', 'in_position')])
        return vao

    def get_vertex_data(self):
        #use pyassimp for calculate tangent, bitangent
        #mesh = pyassimp.load('Opengl_01/models/wall.obj',processing=pyassimp.postprocess.aiProcess_Triangulate | pyassimp.postprocess.aiProcess_CalcTangentSpace)

        objs = pywavefront.Wavefront('Opengl_01/models/wall.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        # for linux project
        with open(f'Opengl_01/shaders/{shader_name}.vert') as file:
        # for windows project
        #with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        # for linux project
        with open(f'Opengl_01/shaders/{shader_name}.frag') as file:
        # for windows project
        #with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
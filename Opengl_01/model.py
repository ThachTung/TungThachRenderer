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
        self.roughness_texture = self.get_texture(path='Opengl_01/models/wall_r.png')
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
        self.shader_program['light.Id'].write(self.app.light.Id)
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
        self.shader_program['r_texture'].value = 2

        self.texture.use(location=0)
        self.normal_texture.use(location=1)
        self.roughness_texture.use(location=2)
  
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

class Skybox:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('skybox')
        self.vao = self.get_vao()
        self.texture = self.get_texture_cube(dir_path='Opengl_01/textures/skybox/', ext='png')
        self.on_init()

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        # textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def update(self):
        m_view = glm.mat4(glm.mat3(self.app.camera.m_view))
        self.shader_program['m_invProjView'].write(glm.inverse(self.app.camera.m_proj * m_view))

    def on_init(self):
        self.shader_program['u_texture_skybox'] = 0
        self.texture.use(location=0)

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()


    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program,
                                    [(self.vbo, '3f','in_position')])
        return vao

    def get_vertex_data(self):
        # in clip space
        z = 0.9999
        vertices = [(-1, -1, z), (3, -1, z), (-1, 3, z)]
        vertex_data = np.array(vertices, dtype='f4')
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
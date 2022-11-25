import glm
from shader import Shader
from buffer import VertexBuffer
from texture import Texture
class Model:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.shader_instance = Shader(self)
        self.vertices_buffer_instance = VertexBuffer(self)
        self.texture_instance = Texture(self)
        self.vertices_buffer = self.get_vertices_buffer()
        self.shader_program = self.get_shader_program('default')
        self.vertices_array = self.get_vertices_array()
        self.model = self.get_model_matrix()
        self.base_color_texture = self.texture_instance.get_texture(path='textures/wall/wall_c.png')
        self.normal_texture = self.texture_instance.get_texture(path='textures/wall/wall_n.png')
        self.roughness_texture = self.texture_instance.get_texture(path='textures/wall/wall_r.png')
        self.on_init()
    def get_model_matrix(self):
        model = glm.mat4()
        return model
    def update(self):
        rot = (0, 0, 0)
        model = glm.rotate(self.model, rot[0], glm.vec3(1, 0, 0))
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.dIntensity'].write(self.app.light.diffuse_intensity)
        self.shader_program['model'].write(model)
        self.shader_program['view'].write(self.app.camera.view)
        self.shader_program['camPosition'].write(self.app.camera.position)
    def on_init(self):
        # light
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.aIntensity'].write(self.app.light.ambient_intensity)
        self.shader_program['light.dIntensity'].write(self.app.light.diffuse_intensity)
        self.shader_program['light.sIntensity'].write(self.app.light.specular_intensity)

        self.shader_program['bTexture'].value = 0
        self.shader_program['nTexture'].value = 1
        self.shader_program['rTexture'].value = 2
        self.base_color_texture.use(location=0)
        self.normal_texture.use(location=1)
        self.roughness_texture.use(location=2)
  
        self.shader_program['projection'].write(self.app.camera.projection)
        self.shader_program['view'].write(self.app.camera.view)
        self.shader_program['model'].write(self.model)
    def get_shader_program(self, shader_name):
        program = self.shader_instance.get_shader_name(shader_name)
        return program
    def get_vertices(self):
        vertices_data = self.shader_instance.get_vertex_model('models/wall.obj')
        return vertices_data
    def get_vertices_buffer(self):
        vertices_buffer = self.vertices_buffer_instance.get_vertices_buffer(self.get_vertices())
        return vertices_buffer
    def get_vertices_array(self):
        vertices_array = self.vertices_buffer_instance.get_vertices_array(self.shader_program, self.vertices_buffer)
        return vertices_array
    def render(self):
        self.update()
        self.vertices_array.render()
    def destroy(self):
        self.vertices_buffer.release()
        self.shader_program.release()
        self.vertices_array.release()
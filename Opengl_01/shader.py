import pywavefront
import numpy

class Shader:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

    def get_shader_name(self, name):
        with open(f'shaders/{name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader,fragment_shader=fragment_shader)
        return program

    def get_vertex_model(self, model_name):
        # use pyassimp for calculate tangent, bitangent
        # mesh = pyassimp.load('Opengl_01/models/wall.obj',processing=pyassimp.postprocess.aiProcess_Triangulate | pyassimp.postprocess.aiProcess_CalcTangentSpace)
        object = pywavefront.Wavefront(model_name,cache=True,parse=True)
        material = object.materials.popitem()[1]
        vertices = material.vertices
        vertices = numpy.array(vertices, dtype='f4')
        return vertices


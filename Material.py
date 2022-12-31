from LoadShader import *

class Material:
    def __init__(self, vertex_shader, fragment_shader):
        self.shader = create_shader(open(vertex_shader).read(), open(fragment_shader).read())

    def use(self):
        glUseProgram(self.shader)
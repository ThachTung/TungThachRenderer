from OpenGL.GL import *

class Uniform:
    def __init__(self, data_type, data):
        self.data_type = data_type
        self.data = data
        self.variable_id = None

    def find_variable(self, shader, variable_name):
        self.variable_id = glGetUniformLocation(shader, variable_name)

    def load(self):
        if self.data_type == "vec3":
            glUniform3f(self.variable_id, self.data[0], self.data[1], self.data[2])
        if self.data_type == "mat4":
            glUniformMatrix4fv(self.variable_id, 1, GL_TRUE, self.data)

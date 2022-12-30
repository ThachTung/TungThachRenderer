from OpenGL.GL import *
import numpy as np

class BufferData:
    def __init__(self, data_type, data):
        self.data_type = data_type
        self.data = data
        self.vbo = glGenBuffers(1)
        self.load_buffer_data()

    def load_buffer_data(self):
        data = np.array(self.data, np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def create_buffer_data(self, shader, variable_name):
        variable_id = glGetAttribLocation(shader, variable_name)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        if self.data_type == "vec3":
            glVertexAttribPointer(variable_id, 3, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec2":
            glVertexAttribPointer(variable_id, 2, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(variable_id)
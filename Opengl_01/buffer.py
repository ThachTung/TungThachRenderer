class VertexBuffer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

    def get_vertices_buffer(self, vertices_data):
        vertices = vertices_data
        vertices_buffer = self.ctx.buffer(vertices)
        return vertices_buffer

    def get_vertices_array(self, shader, vertices_buffer):
        vertices_array = self.ctx.vertex_array(shader,
                                    [(vertices_buffer, '2f 3f 3f', 'in_texcoord_0', 'in_normal', 'in_position')])
        return vertices_array

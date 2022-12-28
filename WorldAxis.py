from Mesh import *

class WorldAxis(Mesh):
    def __init__(self, shader, position=pygame.Vector3(0, 0, 0)):
        self.vertices = [[-100, 0, 0],
                         [100, 0, 0],
                         [0, -100, 0],
                         [0, 100, 0],
                         [0, 0, -100],
                         [0, 0, 100]]
        self.colors = [[1.0, 0.0, 0.0],
                       [1.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.0, 0.0, 1.0],
                       [0.0, 0.0, 1.0]]
        super().__init__(shader=shader, vertices=self.vertices, vertex_colors=self.colors, gl_type=GL_LINES, translation=position)





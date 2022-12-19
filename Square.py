import pygame
from Mesh import *

class Square(Mesh):
    def __init__(self, shader, position=pygame.Vector3(0, 0, 0)):
        self.vertices = [[0.5, 0.5, -1.0],
                         [0.5, -0.5, -1.0],
                         [-0.5, -0.5, -1.0],
                         [-0.5, 0.5, -1.0]]
        self.colors = [[1.0, 0.0, 0.0],
                       [1.0, 0.5, 0.0],
                       [1.0, 1.0, 0.0],
                       [0.0, 1.0, 0.0]]
        super().__init__(shader, self.vertices, self.colors, GL_TRIANGLE_FAN, position)


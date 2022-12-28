import pygame
from MovingMesh import *
from LoadShader import *

class MovingCube(MovingMesh):
    def __init__(self, shader, position=pygame.Vector3(0, 0, 0), moving_rotation=(0, pygame.Vector3(0, 1, 0))):
        coordinates = [(0.5, -0.5, 0.5),
                         (-0.5, -0.5, 0.5),
                         (0.5, 0.5, 0.5),
                         (-0.5, 0.5, 0.5),
                         (0.5, 0.5, -0.5),
                         (-0.5, 0.5, -0.5),
                         (0.5, -0.5, -0.5),
                         (-0.5, -0.5, -0.5),
                         (0.5, 0.5, 0.5),
                         (-0.5, 0.5, 0.5),
                         (0.5, 0.5, -0.5),
                         (-0.5, 0.5, -0.5),
                         (0.5, -0.5, -0.5),
                         (0.5, -0.5, 0.5),
                         (-0.5, -0.5, 0.5),
                         (-0.5, -0.5, -0.5),
                         (-0.5, -0.5, 0.5),
                         (-0.5, 0.5, 0.5),
                         (-0.5, 0.5, -0.5),
                         (-0.5, -0.5, -0.5),
                         (0.5, -0.5, -0.5),
                         (0.5, 0.5, -0.5),
                         (0.5, 0.5, 0.5),
                         (0.5, -0.5, 0.5)]

        triangles = [0, 2, 3, 0, 3, 1, 8, 4, 5, 8, 5, 9, 10, 6, 7, 10, 7, 11, 12,
                          13, 14, 12, 14, 15, 16, 17, 18, 16, 18, 19, 20, 21, 22, 20, 22, 23]

        colors = [0.523, 0.143, 0.123,
                0.123, 0.589, 0.793,
                0.987, 0.567, 0.238,
                0.912, 0.765, 0.589,
                0.589, 0.765, 0.128,
                0.912, 0.589, 0.128,
                0.912, 0.589, 0.128,
                0.589, 0.765, 0.589,
                0.589, 0.589, 0.128,
                0.912, 0.589, 0.589,
                0.912, 0.912, 0.128,
                0.912, 0.912, 0.912,
                0.912, 0.765, 0.765,
                0.765, 0.765, 0.765,
                0.123, 0.765, 0.765,
                0.912, 0.123, 0.128,
                0.123, 0.123, 0.128,
                0.912, 0.123, 0.123,
                0.143, 0.765, 0.143,
                0.912, 0.143, 0.128,
                0.912, 0.765, 0.143,
                0.143, 0.143, 0.143,
                0.589, 0.143, 0.143,
                0.912, 0.143, 0.912,
                0.523, 0.143, 0.123,
                0.123, 0.589, 0.793,
                0.987, 0.567, 0.238,
                0.912, 0.765, 0.589,
                0.589, 0.765, 0.128,
                0.912, 0.589, 0.128,
                0.912, 0.589, 0.128,
                0.589, 0.765, 0.589,
                0.589, 0.589, 0.128,
                0.912, 0.589, 0.589,
                0.912, 0.912, 0.128,
                0.912, 0.912, 0.912]

        vertices = format_vertices(coordinates, triangles)
        super().__init__(shader, vertices, colors, GL_TRIANGLES, position, moving_rotation=moving_rotation)


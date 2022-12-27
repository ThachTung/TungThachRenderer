import pygame
from OpenGL.GL import *
from Mesh import *
from LoadShader import *
import random
class LoadMesh(Mesh):
    def __init__(self, path, shader, gl_type=GL_TRIANGLES, position=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 scale=pygame.Vector3(1, 1, 1)):
        coordinates, triangles = self.loading(path)
        vertices = format_vertices(coordinates, triangles)
        colors = []
        for c in range(len(vertices)):
            colors.append(random.random())
            colors.append(random.random())
            colors.append(random.random())
        super().__init__(shader, vertices, colors, gl_type, position, rotation, scale)


    def loading(self, path):
        vertices = []
        triangles = []
        with open(path) as mesh_file:
            line = mesh_file.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    vertices.append((vx, vy, vz))
                if line[:2] == "f ":
                    f1, f2, f3 = [value for value in line[2:].split()]
                    triangles.append([int(value) for value in f1.split('/')][0] - 1)
                    triangles.append([int(value) for value in f2.split('/')][0] - 1)
                    triangles.append([int(value) for value in f3.split('/')][0] - 1)
                line = mesh_file.readline()
        return vertices, triangles

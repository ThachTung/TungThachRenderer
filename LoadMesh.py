import pygame
import pyassimp
from OpenGL.GL import *
from Mesh import *
from LoadShader import *
import random
class LoadMesh(Mesh):
    def __init__(self,
                 path=None,
                 image_file=None,
                 image_normal=None,
                 image_roughness=None,
                 shader=None,
                 gl_type=GL_TRIANGLES,
                 position=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 scale=pygame.Vector3(1, 1, 1),
                 moving_rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 moving_translation=pygame.Vector3(0, 0,0),
                 moving_scale=pygame.Vector3(1, 1, 1)):
        coordinates, triangles, normals, normals_ind, uvs, uvs_ind, tangent = self.loading(path)
        vertices = format_vertices(coordinates, triangles)
        vertex_normals = format_vertices(normals, normals_ind)
        vertex_uvs = format_vertices(uvs, uvs_ind)
        vertex_tangents = format_vertices(tangent, triangles)
        colors = []
        for c in range(len(vertices)):
            colors.append(1) #random.random() to have random colors
            colors.append(1)
            colors.append(1)
        super().__init__(shader=shader,
                         image_file=image_file,
                         image_normal=image_normal,
                         image_roughness=image_roughness,
                         vertices=vertices,
                         vertex_normals=vertex_normals,
                         vertex_uvs=vertex_uvs,
                         vertex_colors=None,
                         gl_type=gl_type,
                         translation=position,
                         rotation=rotation,
                         scale=scale,
                         moving_rotation=moving_rotation,
                         moving_translation=moving_translation,
                         moving_scale=moving_scale,
                         vertex_tangents=vertex_tangents)


    def loading(self, path):
        vertices = []
        triangles = []
        normals = []
        normals_ind = []
        uvs = []
        uvs_ind = []
        tangent = []
        with open(path) as mesh_file:
            line = mesh_file.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    vertices.append((vx, vy, vz))
                if line[:2] == "vn":
                    vx, vy, vz = [float(value) for value in line[3:].split()]
                    normals.append((vx, vy, vz))
                if line[:2] == "vt":
                    ux, uy = [float(value) for value in line[3:].split()]
                    uvs.append((ux, uy))
                if line[:2] == "f ":
                    f1, f2, f3 = [value for value in line[2:].split()]
                    triangles.append([int(value) for value in f1.split('/')][0] - 1)
                    triangles.append([int(value) for value in f2.split('/')][0] - 1)
                    triangles.append([int(value) for value in f3.split('/')][0] - 1)
                    uvs_ind.append([int(value) for value in f1.split('/')][1] - 1)
                    uvs_ind.append([int(value) for value in f2.split('/')][1] - 1)
                    uvs_ind.append([int(value) for value in f3.split('/')][1] - 1)
                    normals_ind.append([int(value) for value in f1.split('/')][2] - 1)
                    normals_ind.append([int(value) for value in f2.split('/')][2] - 1)
                    normals_ind.append([int(value) for value in f3.split('/')][2] - 1)
                line = mesh_file.readline()

        scene = pyassimp.load(path, processing=pyassimp.postprocess.aiProcess_CalcTangentSpace)
        for index, mesh in enumerate(scene.meshes):
            tangent = mesh.tangents
        return vertices, triangles, normals, normals_ind, uvs, uvs_ind, tangent

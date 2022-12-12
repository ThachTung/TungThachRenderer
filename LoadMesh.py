from OpenGL.GL import *

class LoadMesh:
    def __init__(self, path, gl_type):
        self.vertices = []
        self.triangles = []
        self.mesh = path
        self.type = gl_type
        self.loading()

    def loading(self):
        with open(self.mesh) as mesh_file:
            line = mesh_file.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    self.vertices.append((vx, vy, vz))
                if line[:2] == "f ":
                    f1, f2, f3 = [value for value in line[2:].split()]
                    self.triangles.append([int(value) for value in f1.split('/')][0] - 1)
                    self.triangles.append([int(value) for value in f2.split('/')][0] - 1)
                    self.triangles.append([int(value) for value in f3.split('/')][0] - 1)
                line = mesh_file.readline()

    def drawing(self):
        for t in range(0, len(self.triangles), 3):
            glBegin(self.type)
            glVertex3fv(self.vertices[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t+1]])
            glVertex3fv(self.vertices[self.triangles[t+2]])
            glEnd()

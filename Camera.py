import numpy as np
import pygame
from OpenGL.GLU import *
from math import *
from Transformation import *
from Uniform import *

class Camera:
    def __init__(self, w, h):
        self.screen_width = w
        self.screen_height = h
        self.transformation = identity_matrix()
        self.yaw = 90
        self.pitch = 0
        self.last_mouse = pygame.math.Vector2(0, 0)
        self.mouse_sensitivities = 0.1
        self.movement_sensitivities = 0.5
        self.projection_matrix = self.perspective_matrix(60, self.screen_width/self.screen_height, 0.01, 10000)
        self.projection = Uniform("mat4", self.projection_matrix)

    def perspective_matrix(self, angle_of_view, aspect_ratio, near_plane, far_plane):
        a = radians(angle_of_view)
        d = 1.0/tan(a/2.0)
        r = aspect_ratio
        b = (far_plane + near_plane) / (near_plane - far_plane)
        c = far_plane * near_plane / (near_plane - far_plane)
        return np.array([[d/r, 0, 0, 0],
                         [0, d, 0, 0],
                         [0, 0, b, c],
                         [0, 0, -1, 0]], np.float32)
    def rotation(self, yaw, pitch):
        forward = pygame.Vector3(self.transformation[0, 2], self.transformation[1, 2], self.transformation[2, 2])
        up = pygame.Vector3(0, 1, 0)
        angle = forward.angle_to(up)
        self.transformation = rotate(self.transformation, yaw, "Y", False)
        if angle < 170 and pitch > 0 or angle > 30 and pitch < 0:
            self.transformation = rotate(self.transformation, pitch, "X", True)

    def update(self, shader):
        if pygame.mouse.get_visible():
            return

        mouses = pygame.mouse.get_pressed(3)
        if mouses[0]:
            mouse_position = pygame.mouse.get_pos()
            mouse_new = self.last_mouse - pygame.math.Vector2(mouse_position)

            pygame.mouse.set_pos(self.screen_width/2, self.screen_height/2)
            self.last_mouse = pygame.mouse.get_pos()

            self.rotation(mouse_new.x * self.mouse_sensitivities, mouse_new.y * self.mouse_sensitivities)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.transformation = translate(self.transformation, 0, 0, -self.movement_sensitivities)
        if keys[pygame.K_s]:
            self.transformation = translate(self.transformation, 0, 0, self.movement_sensitivities)
        if keys[pygame.K_a]:
            self.transformation = translate(self.transformation, -self.movement_sensitivities, 0, 0)
        if keys[pygame.K_d]:
            self.transformation = translate(self.transformation, self.movement_sensitivities, 0, 0)

        self.projection.find_variable(shader, "projection_mat")
        self.projection.load()
        lookat_mat = self.transformation
        lookat = Uniform("mat4", lookat_mat)
        lookat.find_variable(shader, "view_mat")
        lookat.load()


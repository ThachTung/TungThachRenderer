import pygame
from OpenGL.GLU import *
from math import *

class Camera:
    def __init__(self):
        self.camera = pygame.math.Vector3(0, 0, -50)
        self.up = pygame.math.Vector3(0, 1, 0)
        self.right = pygame.math.Vector3(1, 0, 0)
        self.forward = pygame.math.Vector3(0, 0, 1)
        self.look_at = self.camera + self.forward
        self.yaw = 90
        self.pitch = 0
        self.last_mouse = pygame.math.Vector2(0, 0)
        self.mouse_sensitivities = 0.01
        self.movement_sensitivties = 0.01

    def rotation(self, yaw, pitch):
        self.yaw += yaw
        self.pitch += pitch
        self.forward.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward.y = sin(radians(self.pitch))
        self.forward.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward.normalize()
        self.right = self.forward.cross(pygame.math.Vector3(0, 1, 0)).normalize()
        self.up = self.right.cross(self.forward).normalize()

    def update(self, screen_width, screen_height):
        if pygame.mouse.get_visible():
            return

        mouses = pygame.mouse.get_pressed(3)
        if mouses[0]:
            mouse_position = pygame.mouse.get_pos()
            mouse_new = self.last_mouse - pygame.math.Vector2(mouse_position)

            pygame.mouse.set_pos(screen_width/2, screen_height/2)
            self.last_mouse = pygame.mouse.get_pos()

            self.rotation(-mouse_new.x * self.mouse_sensitivities, mouse_new.y * self.mouse_sensitivities)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera += self.forward * self.movement_sensitivties
        if keys[pygame.K_s]:
            self.camera -= self.forward * self.movement_sensitivties
        if keys[pygame.K_a]:
            self.camera -= self.right * self.movement_sensitivties
        if keys[pygame.K_d]:
            self.camera += self.right * self.movement_sensitivties

        self.look_at = self.camera + self.forward
        gluLookAt(self.camera.x, self.camera.y, self.camera.z, self.look_at.x, self.look_at.y, self.look_at.z, self.up.x, self.up.y, self.up.z)
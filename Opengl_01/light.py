import glm
import pygame

class Light:
    def __init__(self, position=(3.0,3.0,3.0), color=(1.0,1.0,1.0)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.diffuse_value = 10.0
        self.ambient_intensity = self.color * 0.5
        self.diffuse_intensity = self.color * self.diffuse_value
        self.specular_intensity = self.color * 0.0
    def light_change(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.diffuse_value = self.diffuse_value + 10.0
            self.diffuse_intensity = self.color * self.diffuse_value
        if keys[pygame.K_s]:
            self.diffuse_value = self.diffuse_value - 10.0
            self.diffuse_intensity = self.color * self.diffuse_value


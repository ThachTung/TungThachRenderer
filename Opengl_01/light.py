import glm
import pygame as pg

class Light:
    def __init__(self, position=(3.0,3.0,3.0), color=(1.0,1.0,1.0)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.diffuse_value = 10.0

        #intensitives
        self.Ia = self.color * 0.5 #ambient
        self.Id = self.color * self.diffuse_value #diffuse
        self.Is = self.color * 0.0 #specular

    def light_change(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.diffuse_value = self.diffuse_value + 10.0
            self.Id = self.color * self.diffuse_value
        if keys[pg.K_s]:
            self.diffuse_value = self.diffuse_value - 10.0
            self.Id = self.color * self.diffuse_value


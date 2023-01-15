import pygame
from Transformation import *
from Uniform import *

class Light:
    def __init__(self, position=pygame.Vector3(0, 0, 0),
                 color=pygame.Vector3(1, 1, 1),
                 light_numbers=0,
                 light_intensity=1.0):
        self.transformation = identity_matrix()
        self.position = position
        self.color = color
        self.light_intensity = light_intensity
        self.light_variable = "light_data[" + str(light_numbers) + "].position"
        self.color_variable = "light_data[" + str(light_numbers) + "].color"
        self.intensity_variable = "light_data[" + str(light_numbers) + "].intensity"

    def update(self, shader):
        light_pos = Uniform("vec3", self.position)
        light_pos.find_variable(shader, self.light_variable)
        light_pos.load()
        color = Uniform("vec3", self.color)
        color.find_variable(shader, self.color_variable)
        color.load()

    def update_light(self, shader, intensity):
        light_intensity = Uniform("float", intensity)
        light_intensity.find_variable(shader, self.intensity_variable)
        light_intensity.load()

import glm
import pygame
from tkinter import  *
class Light:
    def __init__(self, position=(3.0,3.0,3.0), color=(1.0,1.0,1.0)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.diffuse_value = 10.0
        self.ambient_intensity = self.color * 0.5
        self.diffuse_intensity = self.color * self.diffuse_value
        self.specular_intensity = self.color * 0.0

        self.diffuse_light_label = Label(text="Diffuse Light Value")
        self.diffuse_light_slider = Scale(from_=0,to=100,command=self.get_value,orient=HORIZONTAL)
        self.pack_function()

    def pack_function(self):
        self.diffuse_light_label.pack()
        self.diffuse_light_slider.pack()
    def get_value(self,value):
        self.diffuse_value = float(value)
        self.diffuse_intensity = self.color * self.diffuse_value
    def light_change(self):
        self.diffuse_light_slider.update()



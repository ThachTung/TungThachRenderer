import glm
from tkinter import  *
class Light:
    def __init__(self, position=(3.0,3.0,3.0), color=(1.0,1.0,1.0)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.ambient_intensity = self.color * 0.5
        self.diffuse_intensity = self.color * 1.0
        self.specular_intensity = self.color * 0.0

        self.diffuse_light_label = Label(text="Diffuse Light Value")
        self.diffuse_light_slider = Scale(from_=0, to=100, command=self.get_light_intensity, orient=HORIZONTAL, length=250)
        self.light_xposition_label = Label(text="Light Position: X Axis")
        self.light_xposition_slider = Scale(from_=-100, to=100, command=self.get_light_xposition, orient=HORIZONTAL, length=250)
        self.light_yposition_label = Label(text="Light Position: Y Axis")
        self.light_yposition_slider = Scale(from_=-100, to=100, command=self.get_light_yposition, orient=HORIZONTAL,
                                            length=250)
        self.light_zposition_label = Label(text="Light Position: Z Axis")
        self.light_zposition_slider = Scale(from_=-100, to=100, command=self.get_light_zposition, orient=HORIZONTAL,
                                            length=250)

        self.pack_function()

    def pack_function(self):
        self.diffuse_light_label.pack()
        self.diffuse_light_slider.pack()
        self.light_xposition_label.pack()
        self.light_xposition_slider.pack()
        self.light_yposition_label.pack()
        self.light_yposition_slider.pack()
        self.light_zposition_label.pack()
        self.light_zposition_slider.pack()
    def get_light_intensity(self,value):
        self.diffuse_intensity = self.color * float(value)

    def get_light_xposition(self, value):
        self.position.x = float(value)
    def get_light_yposition(self, value):
        self.position.y = float(value)
    def get_light_zposition(self, value):
        self.position.z = float(value)
    def light_change(self):
        self.diffuse_light_slider.update()
        self.light_xposition_slider.update()
        self.light_yposition_slider.update()
        self.light_zposition_slider.update()



from tkinter import *
from Light import *
class Ui:
    def __init__(self, shader):
        self.shader = shader
        self.lights_number = 1
        self.lights_intensity = 1.0
        self.root = Tk()
        self.root.geometry("200x300")
        self.frame = Frame(self.root)
        self.frame.pack()

        self.lights = []
        self.light_label, self.light = self.panel_init()


    def panel_init(self):
        light_button = Button(self.frame, text="Add Light", command=self.add_light)
        light_button.pack()
        light_label = Label(self.frame, text="Light Intensity")
        light_label.pack()
        light = Scale(self.frame, from_=0.0, to=10000.0, orient=HORIZONTAL, command=self.get_value)
        light.pack()

        return light_label, light
    def add_light(self):
        #for num in range(0, self.lights_number):
        self.lights.append(Light(position=pygame.Vector3(40, 20, 50),
                                 color=pygame.Vector3(1, 1, 1),
                                 light_numbers=0))
        self.lights.append(Light(position=pygame.Vector3(40, 20, -50),
                                 color=pygame.Vector3(1, 1, 1),
                                 light_numbers=1))
        self.lights.append(Light(position=pygame.Vector3(-40, 20, 50),
                                 color=pygame.Vector3(1, 1, 1),
                                 light_numbers=2))
        self.lights.append(Light(position=pygame.Vector3(-40, 20, -50),
                                 color=pygame.Vector3(1, 1, 1),
                                 light_numbers=3))



        #self.lights_number += 1
    def get_value(self, values):
        self.lights_intensity = float(self.light.get())
    def update(self):
        self.light.update()
        for light in self.lights:
            light.update_light(self.shader.shader, self.lights_intensity)
    def destroy(self):
        self.light.destroy()
        self.light_label.destroy()

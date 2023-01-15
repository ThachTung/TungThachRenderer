from tkinter import *
from Light import *
class Ui:
    def __init__(self, shader):
        self.shader = shader
        self.root = Tk()
        self.root.geometry("200x300")
        self.frame = Frame(self.root)
        self.frame.pack()

        self.lights = []
        self.light_label, self.light = self.panel_init()
        self.lights_intensity = 1.0


    def panel_init(self):
        light_button = Button(self.frame, text="Add Light", command=self.add_light)
        light_button.pack(padx=2, side=TOP)
        light_label = Label(self.frame, text="Light Intensity")
        light_label.pack(padx=2, side=LEFT)
        light = Scale(self.frame, from_=0.0, to=100.0, orient=HORIZONTAL, command=self.get_value)
        light.pack(padx=2, side=LEFT)
        return light_label, light

    def add_light(self):
        self.lights.append(Light(position=pygame.Vector3(0, 5, 5),
                                 color=pygame.Vector3(1, 1, 1),
                                 light_numbers=0,
                                 light_intensity=self.lights_intensity))
    def get_value(self, values):
        self.lights_intensity = float(self.light.get())
        for light in self.lights:
            light.update_light(self.shader.shader, self.lights_intensity)

    def update(self):
        self.light.update()

    def destroy(self):
        self.light.destroy()
        self.light_label.destroy()

from tkinter import *

class Ui:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("200x300")

        self.light_intensity = None
        self.light = self.panel_init()


    def panel_init(self):
        light = Scale(self.root, from_=0.0, to=100.0, orient=HORIZONTAL, command=self.get_value)
        light.pack()
        return light
    def get_value(self, values):
        print(type(self.light.get()))

    def update(self):
        self.light.update()

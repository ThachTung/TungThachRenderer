import pygame
import moderngl
import sys
from model import *
from camera import Camera
from light import Light

#main function
class GraphicsEngine:
    def __init__(self, win_size=(1280,720)):
        pygame.init()
        self.WIN_SIZE = win_size

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        pygame.display.set_mode(self.WIN_SIZE, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        #pygame.event.set_grab(True)
        #pygame.mouse.set_visible(False)

        self.ctx = moderngl.create_context()
        #enable flag for seeing outside of cube
        #self.ctx.front_face = 'cw' # backface culling
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        self.clock = pygame.time.Clock()
        self.time = 0
        self.delta_time = 0

        self.light = Light()
        self.camera = Camera(self)
        self.scene = Model(self)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.scene.destroy()
                pygame.quit()
                sys.exit()
    def render(self):
        #clear framebuffer
        self.ctx.clear(color=(0.18, 0.18, 0.23))
        #render scene
        self.scene.render()
        #swap buffer
        pygame.display.flip()
    def get_time(self):
        self.time = pygame.time.get_ticks() * 0.001
    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.light.light_change()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()

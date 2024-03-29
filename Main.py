import pygame
from pygame.locals import *
from Camera import *
from WorldAxis import *
from LoadMesh import *
from Light import *
from Material import *
from Ui import *
import os

class Engine:
    def __init__(self):
        self.vertex_shader = "shader/texturever.vs"
        self.fragment_shader = "shader/texturefrag.vs"
        self.axis_vertex_shader = "shader/axisver.vs"
        self.axis_fragment_shader = "shader/axisfrag.vs"
        self.pbr_vertex_shader = "shader/pbrver.vs"
        self.pbr_fragment_shader = "shader/pbrfrag.vs"

        # constant location of pygame window
        self.x_location = 100
        self.y_location = 100
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (self.x_location, self.y_location)

        pygame.init()

        self.screen_width = 1880
        self.screen_height = 920
        self.background_color = (0.0, 0.0, 0.0, 1.0)
        self.drawing_color = (1.0, 1.0, 1.0, 1.0)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("TungThachRenderer")
        pygame.display.gl_set_attribute(GL_DEPTH_SIZE, 32)  # --for fixing triangles on the edges of 3D object

        self.shader_program = Material(self.pbr_vertex_shader, self.pbr_fragment_shader)
        self.axis_shader_program = Material(self.axis_vertex_shader, self.axis_fragment_shader)
        self.camera = None
        self.world_axis = None
        self.vao = None
        self.clock = pygame.time.Clock()

        self.ui = Ui(shader=self.shader_program)

        self.lights = self.ui.lights
        #only see 1 side of face
        glEnable(GL_CULL_FACE)


    def load_shader(self):
        self.camera = Camera(self.screen_width, self.screen_height)

        self.wall = LoadMesh(path="model/cad_dry_box.obj",
                             image_file="texture/tex_box_Base_color.png",
                             image_normal="texture/tex_box_Normal_OpenGL.png",
                             image_roughness="texture/tex_box_Roughness.png",
                             image_metallic="texture/tex_box_Metallic.png",
                             shader=self.shader_program,
                             position=pygame.Vector3(0, 0, 0),
                             scale=pygame.Vector3(0.5,0.5,0.5),
                             rotation=Rotation(0, pygame.Vector3(0, 1, 0)))

        self.world_axis = WorldAxis(self.axis_shader_program)
        #enable depth buffer for handling small triangles on the edges of object - not aliasing
        glEnable(GL_DEPTH_TEST)

        #enable alpha blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        #gamma correction enabled
        #glEnable(GL_FRAMEBUFFER_SRGB)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #self.world_axis.mesh_drawing(self.camera, None)
        self.wall.mesh_drawing(self.camera, self.lights)

    def main_loop(self):
        done = False
        self.load_shader()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                    if event.key == K_SPACE:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
            self.ui.update()
            self.display()
            # swap buffer
            pygame.display.flip()
            self.clock.tick(60)
        self.ui.destroy()
        pygame.quit()

Engine().main_loop()
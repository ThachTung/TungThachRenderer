import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import *
from Camera import *
from WorldAxis import *
from LoadBufferData import *
from Square import *
import LoadShader
import os

class Engine:
    def __init__(self):
        self.vertex_shader = r'''
        #version 330 core
        
        in vec3 position;
        in vec3 vertex_color;
        uniform mat4 projection_mat;
        uniform mat4 model_mat;
        uniform mat4 view_mat;
        out vec3 color;
        
        void main()
        {
            gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1.0);
            color = vertex_color;
        }
        '''
        self.fragment_shader = r'''
        #version 330 core
        
        in vec3 color;
        out vec4 frag_color;
        
        void main()
        {
            frag_color = vec4(color, 1.0);
        }
        '''

        # constant location of pygame window
        self.x_location = 500
        self.y_location = 150
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (self.x_location, self.y_location)

        pygame.init()
        self.screen_width = 1000
        self.screen_height = 800
        self.background_color = (0.0, 0.0, 0.0, 1.0)
        self.drawing_color = (1.0, 1.0, 1.0, 1.0)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("TungThachRenderer")

        # mesh = LoadMesh("model/wall.obj", GL_LINE_LOOP)
        self.shader_program = None
        self.square = None
        self.vao = None
        self.vertex_count = 0

    def load_shader(self):
        self.shader_program = LoadShader.create_shader(self.vertex_shader, self.fragment_shader)
        self.square = Square(self. shader_program, position=pygame.Vector3(-0.5, 0.5, 0.0))
        self.world_axis = WorldAxis(self.shader_program, position=pygame.Vector3(0, 0, 0))
        self.camera = Camera(self.shader_program, self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader_program)
        self.camera.update()
        self.world_axis.mesh_drawing()
        self.square.mesh_drawing()


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
            self.display()
            # swap buffer
            pygame.display.flip()

        pygame.quit()

Engine().main_loop()
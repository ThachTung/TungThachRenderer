import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import *
from Camera import *
from WorldAxis import *
import LoadShader
import os

class Engine:
    def __init__(self):
        self.vertex_shader = r'''
        #version 330 core
        void main()
        {
            gl_Position = vec4(0,0,0,1);
        }
        '''
        self.fragment_shader = r'''
        #version 330 core
        out vec4 frag_color;
        void main()
        {
            frag_color = vec4(0,1,0,1);
        }
        '''

        # constant location of pygame window
        self.x_location = 500
        self.y_location = 150
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (self.x_location, self.y_location)

        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        self.screen_width = 1000
        self.screen_height = 800
        self.background_color = (0.0, 0.0, 0.0, 1.0)
        self.drawing_color = (1.0, 1.0, 1.0, 1.0)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("TungThachRenderer")
        self.shader_program = None

        # mesh = LoadMesh("model/wall.obj", GL_LINE_LOOP)
        self.camera = Camera()
        self.world_axis = WorldAxis()
        self.shader_program = None
        self.vao = None

    def init_engine(self):
        glClearColor(self.background_color[0], self.background_color[1], self.background_color[2],
                     self.background_color[3])
        glColor(self.drawing_color)

        # projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, (self.screen_width / self.screen_height), 0.01, 1000)

    def camera_view(self):
        # model view
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, self.screen.get_width(), self.screen.get_height())
        glEnable(GL_DEPTH_TEST)
        self.camera.update(self.screen.get_width(), self.screen.get_height())

    def load_shader(self):
        self.shader_program = LoadShader.create_shader(self.vertex_shader, self.fragment_shader)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        glPointSize(10)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader_program)
        glDrawArrays(GL_POINTS, 0, 1)
        # glRotatef(1, 10, 10, 1)
        #self.camera_view()

        # draw_lines
        #self.world_axis.drawing_line()

    '''
        #---Load Mesh from LoadMesh.py---#
        glPushMatrix()
        #line thickness
        glLineWidth(2)
        mesh.drawing()
        glPopMatrix()
    '''

    '''
    def init_ortho():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, 720, 0, 1024) #gluOrtho2D(left,right,bottom,top)

    def draw_stars(x , y, size):
        glPointSize(size)
        glBegin(GL_POINTS)
        glVertex2i(x, y)
        glEnd()
    '''

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
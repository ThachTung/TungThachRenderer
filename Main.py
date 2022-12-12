import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import *
from Camera import *
pygame.init()

screen_width = 1000
screen_height = 800
background_color = (0.0, 0.0, 0.0, 1.0)
drawing_color = (1.0, 1.0, 1.0, 1.0)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("TungThachRenderer")

mesh = LoadMesh("wall.obj", GL_LINE_LOOP)
camera = Camera()

def init():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    #projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width/screen_height), 0.01, 1000)

def camera_view():
    #model view
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update(screen.get_width(), screen.get_height())

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glRotatef(1, 10, 10, 1)
    camera_view()
    glPushMatrix()
    #glLineWidth(10) - line thickness
    mesh.drawing()
    glPopMatrix()

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

done = False
init()
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
    display()
    #swap buffer
    pygame.display.flip()

pygame.quit()
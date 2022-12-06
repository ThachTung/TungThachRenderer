import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL Window")

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 720, 0, 1024) #(0, 720, 1024, 0) will flip Y --- gluOrtho2D(left,right,bottom,top)

def draw_stars(x , y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

done = False
init_ortho()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_stars(10, 10, 5)
    draw_stars(20, 10, 10)
    draw_stars(10, 50, 15)
    draw_stars(15, 70, 5)
    draw_stars(100, 70, 15)
    draw_stars(100, 150, 10)
    draw_stars(150, 250, 20)
    draw_stars(300, 600, 50)

    pygame.display.flip()
    pygame.time.wait(100)

pygame.quit()
from OpenGL.GLU import *
from OpenGL.GL import *

class WorldAxis:
    def __init__(self):
        self.draw_type = GL_LINES
        self.line_width = 4
        self.color_xaxis = (1, 0, 0)
        self.color_yaxis = (0, 1, 0)
        self.color_zaxis = (0, 0, 1)
        self.drawing_line()

    def drawing_line(self):
        glBegin(self.draw_type)
        glColor(self.color_xaxis)
        glVertex3d(-500, 0, 0)
        glVertex3d(500, 0, 0)

        glColor(self.color_yaxis)
        glVertex3d(0, -500, 0)
        glVertex3d(0, 500, 0)

        glColor(self.color_zaxis)
        glVertex3d(0, 0, -500)
        glVertex3d(0, 0, 500)

        glEnd()

        #positive sphere
        sphere = gluNewQuadric()

        glColor(self.color_xaxis)
        glPushMatrix()
        glTranslated(50, 0, 0)
        gluSphere(sphere, 1, 10, 10)
        glPopMatrix()

        glColor(self.color_yaxis)
        glPushMatrix()
        glTranslated(0, 50, 0)
        gluSphere(sphere, 1, 10, 10)
        glPopMatrix()

        glColor(self.color_zaxis)
        glPushMatrix()
        glTranslated(0, 0, 50)
        gluSphere(sphere, 1, 10, 10)
        glPopMatrix()




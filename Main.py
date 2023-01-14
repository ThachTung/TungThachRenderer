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
        pygame.display.gl_set_attribute(GL_DEPTH_SIZE, 32)  # --for fixing triangles on the edges of 3D object

        self.shader_program = None
        self.axis_shader_program = None
        self.camera = None
        self.lights = []
        self.world_axis = None
        self.vao = None
        self.clock = pygame.time.Clock()

        self.ui = Ui()

        #only see 1 side of face
        glEnable(GL_CULL_FACE)

    def load_shader(self):
        #self.shader_program = Material(self.vertex_shader, self.fragment_shader)
        self.shader_program = Material(self.pbr_vertex_shader, self.pbr_fragment_shader)
        self.axis_shader_program = Material(self.axis_vertex_shader, self.axis_fragment_shader)
        self.camera = Camera(self.screen_width, self.screen_height)
        self.lights.append(Light(position=pygame.Vector3(0, 5, 5),
                            color=pygame.Vector3(1, 1, 1), light_numbers=0))
        '''
        self.lights.append(Light(position=pygame.Vector3(0, 5, -6),
                                 color=pygame.Vector3(1, 1, 1), light_numbers=1))
        '''

        self.wall = LoadMesh(path="model/wall.obj", image_file="texture/wallBC.png", image_normal="texture/wallN.png",
                             image_roughness="texture/wallR.png", shader=self.shader_program,
                             position=pygame.Vector3(0, 0, 0),
                             rotation=Rotation(0, pygame.Vector3(0, 1, 0)))
        '''
        #edit obj_file: vt data to control UV
        self.plane = LoadMesh('model/plane.obj', "texture/window.png", self.shader_program,
                             scale=pygame.Vector3(1, 1, 1),
                             rotation=Rotation(0, pygame.Vector3(0, 1, 0)))
        self.cube = LoadMesh('model/cube.obj', "texture/crate.png", self.shader_program,
                             position=pygame.Vector3(0, -1, 0),
                              scale=pygame.Vector3(1, 1, 1),
                              rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                             moving_rotation=Rotation(1, pygame.Vector3(0, 1, 0)))
        '''
        #self.cube2 = Cube(self.axis_shader_program, position=pygame.Vector3(0, 1, 0))
        self.world_axis = WorldAxis(self.axis_shader_program)
        #enable depth buffer for handling small triangles on the edges of object - not aliasing
        glEnable(GL_DEPTH_TEST)

        #enable alpha blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.world_axis.mesh_drawing(self.camera, None)
        self.wall.mesh_drawing(self.camera, self.lights)
        #self.square.mesh_drawing()
        #self.cube.mesh_drawing()
        #self.wall.mesh_drawing()
        #self.cube.mesh_drawing(self.camera, self.lights)
        #self.cube2.mesh_drawing(self.camera, None)
        #object with transparent texture must be drawed at last
        #self.plane.mesh_drawing(self.camera, self.lights)

    def main_loop(self):
        done = False
        self.load_shader()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while not done:
            self.ui.update()
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
            self.clock.tick(60)
        pygame.quit()

Engine().main_loop()
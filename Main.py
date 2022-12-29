import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadBufferData import *
from Camera import *
from WorldAxis import *
from Square import *
from Cube import *
from LoadMesh import *
from Light import *
import LoadShader
import os

class Engine:
    def __init__(self):
        self.vertex_shader = r'''
        #version 330 core
        
        in vec3 position;
        in vec3 vertex_color;
        in vec3 vertex_normal;
        uniform mat4 projection_mat;
        uniform mat4 model_mat;
        uniform mat4 view_mat;
        out vec3 color;
        out vec3 normal;
        out vec3 frag_pos;
        //out vec3 light_pos;
        out vec3 cam_pos;
        
        void main()
        {
            // static light_pos at camera view
            //light_pos = vec3(inverse(model_mat) * vec4(view_mat[3][0], view_mat[3][1], view_mat[3][2], 1));
            //light_pos = vec3(model_mat * vec4(5, 5, 5, 1));
            //light_pos = vec3(5, 5, 5);
            
            //camera pos
            cam_pos = vec3(inverse(model_mat) * vec4(view_mat[3][0], view_mat[3][1], view_mat[3][2], 1));
            gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1.0);
            //normal = mat3(transpose(inverse(model_mat))) * vertex_normal;
            normal = vec3(model_mat * vec4(vertex_normal, 1));
            frag_pos = vec3(model_mat * vec4(position, 1.0));
            color = vertex_color;
        }
        '''
        self.fragment_shader = r'''
        #version 330 core
        
        in vec3 color;
        in vec3 normal;
        in vec3 frag_pos;
        in vec3 cam_pos;
        out vec4 frag_color;
        
        struct Light
        {
            vec3 position;
            vec3 color;
        };
        
        #define NUM_LIGHTS 2
        uniform Light light_data[NUM_LIGHTS];
        
        vec4 CreateLight(vec3 light_pos, vec3 light_color, vec3 normal, vec3 frag_pos, vec3 view_dir)
        {        
            //ambient
            float ambient_strength = 0.1;
            vec3 ambient = ambient_strength * light_color;
            
            //diffuse
            vec3 norm = normalize(normal);
            vec3 light_dir = normalize(light_pos - frag_pos);
            float diff = max(dot(light_dir, norm), 0.001);
            vec3 diffuse = diff * light_color;
            
            //specular
            float specular_strength = 1.0;
            vec3 reflect_dir = normalize(-light_dir - norm);
            float spec = pow(max(dot(view_dir, reflect_dir), 0.001), 32);
            vec3 specular = specular_strength * spec * light_color;
            
            return vec4(color * (diffuse + ambient + specular), 1.0);
        }
        
        void main()
        {
            vec3 light_color = vec3(1, 0, 0);
            vec3 view_dir = normalize(cam_pos - frag_pos);
            
            for (int i=0; i < NUM_LIGHTS; i++)
            {
                frag_color += CreateLight(light_data[i].position, light_data[i].color, normal, frag_pos, view_dir);
            }
        }
        '''

        # constant location of pygame window
        self.x_location = 500
        self.y_location = 150
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (self.x_location, self.y_location)

        pygame.init()
        #pygame.display.gl_set_attribute(GL_DEPTH_SIZE, 32) #--for fixing triangles on the edges of 3D object
        self.screen_width = 1000
        self.screen_height = 800
        self.background_color = (0.0, 0.0, 0.0, 1.0)
        self.drawing_color = (1.0, 1.0, 1.0, 1.0)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("TungThachRenderer")

        # mesh = LoadMesh("model/wall.obj", GL_LINE_LOOP)
        self.shader_program = None
        self.camera = None
        self.light1 = None
        self.light2 = None
        self.world_axis = None
        self.square = None
        self.cube = None
        self.moving_cube = None
        self.mesh = None
        self.vao = None
        self.vertex_count = 0
        self.clock = pygame.time.Clock()

    def load_shader(self):
        self.shader_program = LoadShader.create_shader(self.vertex_shader, self.fragment_shader)
        #self.square = Square(self. shader_program, position=pygame.Vector3(-0.5, 0.5, 0.0))
        #self.world_axis = WorldAxis(self.shader_program)
        #self.cube = Cube(self.shader_program, position=pygame.Vector3(0, 2, 0))
        #self.moving_cube = Cube(self.shader_program, position=pygame.Vector3(0, 0, 0), moving_rotation=Rotation(1, pygame.Vector3(0, 1, 0)))
        self.camera = Camera(self.shader_program, self.screen_width, self.screen_height)
        self.light1 = Light(self.shader_program, position=pygame.Vector3(2, 1, 2),
                            color=pygame.Vector3(1, 0, 0), light_numbers=0)
        self.light2 = Light(self.shader_program, position=pygame.Vector3(-2, 1, -2),
                            color=pygame.Vector3(0, 1, 0), light_numbers=1)
        self.mesh = LoadMesh('model/wall.obj', self.shader_program,
                             scale=pygame.Vector3(0.1, 0.1, 0.1),
                             rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                             moving_rotation=Rotation(1, pygame.Vector3(0, 1, 0)))
        glEnable(GL_DEPTH_TEST)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader_program)
        self.camera.update()
        self.light1.update()
        self.light2.update()
        #self.world_axis.mesh_drawing()
        #self.square.mesh_drawing()
        #self.cube.mesh_drawing()
        #self.moving_cube.mesh_drawing()
        self.mesh.mesh_drawing()


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
            self.clock.tick(60)

        pygame.quit()

Engine().main_loop()
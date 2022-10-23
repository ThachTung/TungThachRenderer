import glm
import pygame as pg

FOV = 50 #deg
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVE = 0.1

class Camera:
    def __init__(self, app, position=(0,0,4),yaw=-90,pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0,1,0)

        self.right = glm.vec3(1,0,0)
        self.forward = glm.vec3(0,0,-1)

        self.yaw = yaw
        self.pitch = pitch

        #view_matrix
        self.m_view = self.get_view_matrix()

        #projection matrix
        self.m_proj = self.get_projection_matrix()
    
    def update(self):
        self.move()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()


    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
        
        self.forward.x = glm.cos(yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward,glm.vec3(0,1,0)))
        self.up = glm.normalize(glm.cross(self.right,self.forward))

    def move(self):
        velocity = SPEED * self.app.delta_time
        rel_x, rel_y = pg.mouse.get_rel()
        mouses = pg.mouse.get_pressed(num_buttons=3)
        keys = pg.key.get_pressed()
   
        if keys[pg.K_LALT] and mouses[2]:
            self.position += self.forward * velocity * rel_x * SENSITIVE
        if keys[pg.K_LALT] and mouses[0]:
            self.yaw += rel_x * SENSITIVE * velocity
            self.pitch -= rel_y * SENSITIVE * velocity * 0.05
        if keys[pg.K_LALT] and mouses[1]:
            self.position += (self.up * velocity * (-rel_y) * SENSITIVE + self.right * velocity * SENSITIVE * rel_x)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)

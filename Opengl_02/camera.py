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

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
        
        self.forward.x = glm.cos(yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward,glm.vec3(0,1,0)))
        self.up = glm.normalize(glm.cross(self.right,self.forward))

    def update(self):
        self.move()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        rel_x, rel_y = pg.mouse.get_rel()
        mouses = pg.mouse.get_pressed(num_buttons=3)
        keys = pg.key.get_pressed()
        if keys[pg.K_LALT] and mouses[2]== True:
            self.position += self.forward * velocity * rel_x * SENSITIVE
        if keys[pg.K_LALT] and mouses[0]== True:
            self.yaw += rel_x * SENSITIVE * velocity
            self.pitch -= rel_y * SENSITIVE * velocity * 0.05
            # self.pitch = max(-89, min(89, self.pitch))
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_LALT] and mouses[1] == True:
            self.position += self.up * velocity * rel_x * SENSITIVE
        if mouses[0] == True or mouses[1] == True or mouses[2] == True:
            # mouse settings
            pg.event.set_grab(True)
            pg.mouse.set_visible(False)
        else:
            pg.event.set_grab(False)
            pg.mouse.set_visible(True)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
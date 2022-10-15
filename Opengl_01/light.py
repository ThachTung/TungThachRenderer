import glm

class Light:
    def __init__(self, position=(3.0,3.0,3.0), color=(1.0,1.0,1.0)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        #intensitives
        self.Ia = self.color * 0.5 #ambient
        self.Id = self.color * 0.8 #diffuse
        self.Is = self.color * 1.0 #specular

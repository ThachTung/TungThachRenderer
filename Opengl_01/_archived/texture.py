import pygame
import moderngl

class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
    def get_texture(self, path):
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)

        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                       data=pygame.image.tostring(texture, 'RGB'))
        texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        texture.build_mipmaps()

        texture.anisotropy = 32.0
        return texture

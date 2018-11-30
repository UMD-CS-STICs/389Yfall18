import pygame

class Pedestrian(object):

    id_counter = 0

    def __init__(self, x, y, vx, vy, img_path, camera):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.sprite = pygame.image.load(img_path)
        self.camera = camera
        self.mask = pygame.mask.from_threshold(self.sprite, (0,0,0), (127, 127, 127))
        self.id = Pedestrian.id_counter
        Pedestrian.id_counter += 1

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def blit(self, surface):
        offsetx = self.sprite.get_width() / 2
        offsety = self.sprite.get_height() / 2

        surface.blit(self.sprite, (self.x - offsetx - self.camera.x, self.y - offsety - self.camera.y))

    def get_width(self):
        return self.sprite.get_width()

    def get_height(self):
        return self.sprite.get_height()

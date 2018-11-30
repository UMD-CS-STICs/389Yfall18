import pygame

class Road(object):
    def __init__(self, width, height, camera):
        self.width = width
        self.height = height
        self.line_height = 10
        self.line_width = 80
        self.line_gap = 20
        self.camera = camera
        self.x = 0

    def update(self, vx, dt):
        dx = dt*vx
        sign = lambda x: 1 if x >= 0 else -1
        self.x += sign(dx)*(abs(dx) % (self.line_width + self.line_gap))

    def blit(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (0, -self.camera.y-self.height/2, self.width, self.height))
        x = self.x
        while x < self.width:
            pygame.draw.rect(surface, (255, 255, 0), (x, -self.camera.y-self.line_height/2, self.line_width, self.line_height))
            x += self.line_width + self.line_gap

import pygame

class Landmark(object):
    def __init__(self, x, y, camera):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.camera = camera

    def blit(self, surface, robot=None):
        x = self.x - self.camera.x
        y = self.y - self.camera.y
        pygame.draw.rect(surface, (0, 255, 0), (x - self.width/2, y - self.height/2, self.width, self.height))
        if robot:
            pygame.draw.line(surface, (0, 0, 255), (x, y), (robot.x - self.camera.x, robot.y - self.camera.y), 2)

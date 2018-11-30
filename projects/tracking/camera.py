import pygame

class Camera(object):
    def __init__(self, screen, x, y, offsetx=0, offsety=0):
        self.screen = screen
        self.x = x
        self.y = y
        self.offsetx = offsetx
        self.offsety = offsety
        self.follow_obj = None

    def follow(self, obj):
        self.follow_obj = obj

    def update(self, xonly=False):
        if self.follow_obj:
            self.x = self.follow_obj.x - self.screen.get_width() / 2 - self.offsetx
            if xonly:
                self.y = -self.screen.get_height() / 2 - self.offsety
            else:
                self.y = self.follow_obj.y - self.screen.get_height() / 2 - self.offsety

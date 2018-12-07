import pygame
from maze import *
from landmark import *
from robot import *
from camera import *

class World:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 900))
        self.camera = Camera(self.screen, 0, 0)
        self.maze = Maze(0, 0, 'maze.jpg', self.camera)
        self.landmarks = [Landmark(random.random()*self.maze.get_width(), random.random()*self.maze.get_height(), self.camera) for _ in xrange(10)]
        self.negative_landmarks = [Landmark(random.random()*self.maze.get_width(), random.random()*self.maze.get_height(), self.camera) for _ in xrange(0)]
        self.robot = RobotBin(20, 175, 'car.png', self.camera, self.landmarks, self.negative_landmarks, self.maze)
        self.camera.follow(self.robot)

    def update(self):
        self.robot.controls()
        self.camera.update()

    def get_width(self):
        return self.maze.get_width()

    def get_height(self):
        return self.maze.get_height()

    def blit(self):
        self.screen.fill((255, 255, 255))
        self.maze.blit(self.screen)
        self.robot.blit(self.screen)
        for landmark in self.landmarks:
            landmark.blit(self.screen)
        self.hfilter.blit(self.screen, self.camera)
        pygame.display.flip()

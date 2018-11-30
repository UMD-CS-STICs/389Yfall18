'''
The main program for the simulation. You will make some modifications to this file when answering
questions about the project.
'''

import pygame
import math
import numpy as np
from robot import *
from camera import *
from pedestrian import *
from road import *
import random
from pygame import gfxdraw


### Initialize graphics ###
pygame.init()
screen = pygame.display.set_mode((1200, 900))
camera = Camera(screen, 0, 0, -300, 0)
robot = RobotSimple(0, 0, 300, 0, 'car.png', camera)
road = Road(1200, 300, camera)
kalman_filter = KalmanFilter()
clock = pygame.time.Clock()
camera.follow(robot)


def spawn():
    x = 400 + 700 * random.random()
    if random.random() > 0.5:
        y = 300
        vy = -100 + -200 * random.random()
    else:
        y = -300
        vy = 100 + 200 * random.random()

    robot.pedestrians.append(Pedestrian(
        robot.x + x, y, 0, vy, 'pedestrian.png', camera))

t = pygame.time.get_ticks()
FREQ = 30

# Loop until QUIT event recieved
while pygame.QUIT not in (event.type for event in pygame.event.get()):
    old_vx, old_vy = robot.vx, robot.vy

    ### Update World ###
    camera.update(True)
    robot.update(1. / FREQ, kalman_filter.states)
    road.update(-robot.vx, 1. / FREQ)
    for pedestrian in robot.pedestrians:
        pedestrian.update(1. / FREQ)

    new_vx, new_vy = robot.vx, robot.vy

    accel_x, accel_y = (new_vx - old_vx) * FREQ, (new_vy - old_vy) * FREQ
    control_signal = np.array([[accel_x], [accel_y]])

    kalman_filter.prediction(control_signal)
    z, Q = robot.get_pedestrian_measurements()
    kalman_filter.measurement(z, Q)

    ### Draw World ###
    screen.fill((255, 255, 255))
    road.blit(screen)
    robot.blit(screen)
    for pedestrian in robot.pedestrians:
        pedestrian.blit(screen)

    if pygame.time.get_ticks() - t > 1000:
        t = pygame.time.get_ticks()
        for i in range(random.randint(1, 3)):
            spawn()

    for i in kalman_filter.states.keys():
        x, y, vx, vy = kalman_filter.states[i].flatten()
        cov = kalman_filter.covariances[i]
        width = 2 * math.sqrt(5.991 * cov[0, 0])
        height = 2 * math.sqrt(5.991 * cov[1, 1])
        ellipse_surface = pygame.Surface((width + 2, height + 2), pygame.SRCALPHA, 32)
        radius = 3 if 3 < min(width, height) // 2 else 0
        pygame.draw.ellipse(ellipse_surface, (255, 0, 0), (0, 0, width, height), radius)
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (int(robot.x + x - camera.x), int(robot.y + y - camera.y)),
            3
        )
        screen.blit(
            ellipse_surface,
            (robot.x + x - ellipse_surface.get_width() / 2 - camera.x,
             robot.y + y - ellipse_surface.get_height() / 2 - camera.y)
        )

    # Remove pedestrians outside the robot's sight
    robot.pedestrians = [p for p in robot.pedestrians if p.y + p.get_height(
    ) / 2 > -400 and p.y - p.get_height() / 2 < 400 and p.x - robot.x > -300]

    pygame.display.flip()
    clock.tick(FREQ)

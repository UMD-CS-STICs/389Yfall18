import pygame
import math
import numpy as np
import random
from random import random
from kfslam import *
from landmark import *
from robot import *
from camera import *

### Params ###
SIZE = 800
NUM_LANDMARKS = random.randint(30, 35)


### Initialize graphics ###
pygame.init()
screen = pygame.display.set_mode((1200, 900))
camera = Camera(screen, 0, 0)
landmarks = [Landmark(random.random() * SIZE,
                      random.random() * SIZE, camera) for _ in range(NUM_LANDMARKS)]
robot = RobotKFSlam(34, 263, 'car.png', camera,
                    landmarks)
camera.follow(robot)
clock = pygame.time.Clock()


def draw_ellipse(screen, x, y, width, height, camera):
    ellipse_surface = pygame.Surface(
        (width + 2, height + 2), pygame.SRCALPHA, 32)
    radius = 3 if 3 < min(width, height) // 2 else 0
    pygame.draw.ellipse(ellipse_surface, (255, 0, 0),
                        (0, 0, width, height), radius)
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (int(x - camera.x), int(y - camera.y)),
        3
    )
    screen.blit(
        ellipse_surface,
        (x - ellipse_surface.get_width() / 2 - camera.x,
         y - ellipse_surface.get_height() / 2 - camera.y)
    )

### Initialize Filter ###
kalman_filter = KFSlam(robot)

# Loop until QUIT event recieved
while pygame.QUIT not in (event.type for event in pygame.event.get()):
    prev_x, prev_y = robot.x_odom, robot.y_odom

    ### Update World ###
    robot.controls()
    camera.update()

    ## Motion Update ##
    odom = robot.odometry()
    kalman_filter.prediction(
        np.array([[robot.x_odom - prev_x], [robot.y_odom - prev_y]]))

    ## Measurement Update ##
    detections = robot.detect_landmarks()
    # Detections should already be landmark - odom => check the detect_landmarks()
    # function to confirm.
    kalman_filter.measurement(detections, robot.Q())

    ### Draw World ###
    screen.fill((255, 255, 255))
    robot.blit(screen)
    x = kalman_filter.states[0,0]
    y = kalman_filter.states[1,0]
    width = 2 * math.sqrt(200.991 * kalman_filter.covariances[0, 0])
    height = 2 * math.sqrt(200.991 * kalman_filter.covariances[1, 1])
    draw_ellipse(screen, x, y, width, height, camera)
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (int(kalman_filter.states[0,0] - camera.x), int(kalman_filter.states[1,0] - camera.y)),
        3
    )

    for landmark in landmarks:
        landmark.blit(screen)

    for d in detections:
        i = list(d.keys())[0]
        x, y = d[i][0], d[i][1]
        Landmark(x + robot.x, y + robot.y, camera).blit(screen, robot)

    # Draws covarianaces ovals
    for i in range(int((kalman_filter.states.shape[0] - 2) / 2)):
        x = kalman_filter.states[2 * (i + 1)]
        y = kalman_filter.states[2 * (i + 1) + 1]
        width = 2 * \
            math.sqrt(
                200.991 * kalman_filter.covariances[2 * (i + 1), 2 * (i + 1)])
        height = 2 * \
            math.sqrt(
                200.991 * kalman_filter.covariances[2 * (i + 1) + 1, 2 * (i + 1) + 1])
        draw_ellipse(screen, x, y, width, height, camera)

    pygame.display.flip()
    clock.tick(10)

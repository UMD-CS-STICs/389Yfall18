import pygame
import numpy as np
import math
import random
from kalmanfilter import KalmanFilter


class RobotBin(object):

    def __init__(self, x, y, img_path, camera, landmarks, negative_landmarks, maze):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(img_path)
        self.mask = pygame.mask.from_surface(self.sprite)
        self.camera = camera
        self.x_odom = x
        self.y_odom = y
        self.x_noise = 0.08
        self.y_noise = 0.08
        self.z_noise = 10
        self.phit = 0.9
        self.pfalse = 0.01
        self.max_sense_dist = 100
        self.landmarks = landmarks
        self.negative_landmarks = negative_landmarks
        self.maze = maze

    def blit(self, surface):
        x = self.x - self.sprite.get_width() / 2
        y = self.y - self.sprite.get_height() / 2
        surface.blit(self.sprite, (x - self.camera.x, y - self.camera.y))

    def move(self, dx, dy, collision_mask, tolerance=0.001):
        if abs(dx) < tolerance and abs(dy) < tolerance:
            return
        new_x = self.x + dx
        new_y = self.y + dy

        offsetx = int(new_x - self.sprite.get_width() / 2 + 0.5)
        offsety = int(new_y - self.sprite.get_height() / 2 + 0.5)

        if collision_mask and collision_mask.overlap_area(self.mask, (offsetx, offsety)) == 0:
            self.x_odom += new_x - self.x + \
                np.random.normal(
                    scale=abs(dx) * self.x_noise) if dx != 0 else 0
            self.y_odom += new_y - self.y + \
                np.random.normal(
                    scale=abs(dy) * self.y_noise) if dy != 0 else 0

            self.x = new_x
            self.y = new_y
        else:
            self.move(dx / 1.5, dy / 1.5, collision_mask)

    def controls(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.move(0, -20, self.maze.mask)
        if pressed[pygame.K_DOWN]:
            self.move(0, 20, self.maze.mask)
        if pressed[pygame.K_LEFT]:
            self.move(-20, 0, self.maze.mask)
        if pressed[pygame.K_RIGHT]:
            self.move(20, 0, self.maze.mask)

    def odometry(self):
        return self.x_odom, self.y_odom

    def detect_landmarks(self):
        detected = []
        for i, landmark in enumerate(self.landmarks):
            dist = math.sqrt((self.x - landmark.x)**2 +
                             (self.y - landmark.y)**2)
            if 0 < dist < self.max_sense_dist and random.random() < self.phit:
                x = self.x_odom + landmark.x - self.x + \
                    np.random.normal(scale=self.z_noise)
                y = self.y_odom + landmark.y - self.y + \
                    np.random.normal(scale=self.z_noise)
                detected.append((x, y))

        for landmark in self.negative_landmarks:
            dist = math.sqrt((self.x - landmark.x)**2 +
                             (self.y - landmark.y)**2)
            if 0 < dist < self.max_sense_dist and random.random() < self.pfalse:
                x = self.x_odom + landmark.x - self.x + \
                    np.random.normal(scale=self.z_noise)
                y = self.y_odom + landmark.y - self.y + \
                    np.random.normal(scale=self.z_noise)
                detected.append((x, y))

        return detected


class RobotCar(object):

    def __init__(self, x, y, theta, img_path, camera):
        self.x = x
        self.y = y
        self.theta = theta
        self.sprite = pygame.transform.rotate(pygame.image.load(img_path), -90)
        self.sprite_rot = pygame.transform.rotate(
            self.sprite, math.degrees(theta))
        self.camera = camera

    def move(self, dr, dtheta, collision_mask, tolerance=0.001):
        if abs(dr) < tolerance and abs(dtheta) < tolerance:
            return
        new_theta = self.theta + dtheta
        new_x = self.x + dr * math.sin(new_theta)
        new_y = self.y + dr * math.cos(new_theta)
        new_sprite_rot = pygame.transform.rotate(
            self.sprite, math.degrees(new_theta))
        mask = pygame.mask.from_surface(new_sprite_rot)
        offsetx = int(new_x - new_sprite_rot.get_width() / 2 + 0.5)
        offsety = int(new_y - new_sprite_rot.get_height() / 2 + 0.5)

        if collision_mask and collision_mask.overlap_area(mask, (offsetx, offsety)) == 0:
            self.x = new_x
            self.y = new_y
            self.theta = new_theta % (2 * math.pi)
            self.sprite_rot = new_sprite_rot
        else:
            self.move(dr / 1.5, dtheta / 1.5, collision_mask)

    def blit(self, surface):
        x = self.x - self.sprite_rot.get_width() / 2 - self.camera.x
        y = self.y - self.sprite_rot.get_height() / 2 - self.camera.y
        surface.blit(self.sprite_rot, (x, y))

    def controls(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.move(10, 0, maze.mask)
        if pressed[pygame.K_DOWN]:
            self.move(-10, 0, maze.mask)
        if pressed[pygame.K_LEFT]:
            self.move(0, math.pi / 20, maze.mask)
        if pressed[pygame.K_RIGHT]:
            self.move(0, -math.pi / 20, maze.mask)


class RobotSimple(object):

    def __init__(self, x, y, vx, vy, img_path, camera):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.sprite = pygame.image.load(img_path)
        self.mask = pygame.mask.from_surface(self.sprite)
        self.camera = camera
        self.pedestrians = []

    def controls(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.move(0, -20)
        if pressed[pygame.K_DOWN]:
            self.move(0, 20)
        if pressed[pygame.K_LEFT]:
            self.move(-20, 0)
        if pressed[pygame.K_RIGHT]:
            self.move(20, 0)

    def update(self, dt, states):
        old_vx, old_vy = self.vx, self.vy
        new_vx, new_vy = self.search_vel(states, 5, dt, 10)
        self.vx, self.vy = new_vx, new_vy
        self.x += self.vx * dt
        self.y += self.vy * dt

    def obstacle_cost(self, x, inflation):
        return math.exp(-x**2 / (2 * inflation))

    def search_vel(self, obstacles, dv, dt, N):
        best_vx = self.vx
        best_vy = self.vy
        best_cost = float('inf')
        for vx in np.arange(self.vx - N * dv, self.vx + (N + 1) * dv, dv):
            if vx < -100:
                continue
            if vx > 600:
                break
            for vy in np.arange(self.vy - N * dv, self.vy + (N + 1) * dv, dv):
                if vy < -40:
                    continue
                if vy > 40:
                    break
                x = vx * dt
                y = vy * dt
                cost = 10 * abs(self.y + y) + 0.1 * abs(300 - vx)
                for i in obstacles:
                    obs_x = obstacles[i][0][0] + obstacles[i][2][0] * dt
                    obs_y = obstacles[i][1][0] + obstacles[i][3][0] * dt
                    d = math.sqrt((x - obs_x)**2 + (y - obs_y)**2)
                    cost += 20000 * self.obstacle_cost(d, 700)

                if cost < best_cost:
                    best_cost = cost
                    best_vx = vx
                    best_vy = vy
        return best_vx, best_vy

    def move(self, dx, dy, tolerance=0.001):
        new_x = self.x + dx
        new_y = self.y + dy
        self.x = new_x
        self.y = new_y

    def Q(self):
        return np.array(
            [[1000 * np.random.rand(), 0],
             [0, 1000 * np.random.rand()]]
        )

    def get_pedestrian_measurements(self):
        cov = self.Q()
        measurements = {}
        for p in self.pedestrians:
            measurements[p.id] = np.random.multivariate_normal(
                [p.x - self.x, p.y - self.y], cov, size=1).T
        return measurements, cov

    def blit(self, surface):
        x = self.x - self.sprite.get_width() / 2
        y = self.y - self.sprite.get_height() / 2
        surface.blit(self.sprite, (x - self.camera.x, y - self.camera.y))


class RobotKFSlam(object):

    def __init__(self, x, y, img_path, camera, landmarks):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(img_path)
        self.mask = pygame.mask.from_surface(self.sprite)
        self.camera = camera
        self.x_odom = x
        self.y_odom = y
        self.x_noise = 0.05
        self.y_noise = 0.05
        self.z_noise = 10
        self.phit = 0.9
        self.pfalse = 0.01
        self.max_sense_dist = 100
        self.landmarks = landmarks

    def blit(self, surface):
        x = self.x - self.sprite.get_width() / 2
        y = self.y - self.sprite.get_height() / 2
        surface.blit(self.sprite, (x - self.camera.x, y - self.camera.y))

    def move(self, dx, dy, tolerance=0.001):
        if abs(dx) < tolerance and abs(dy) < tolerance:
            return
        new_x = self.x + dx
        new_y = self.y + dy

        offsetx = int(new_x - self.sprite.get_width() / 2 + 0.5)
        offsety = int(new_y - self.sprite.get_height() / 2 + 0.5)

        self.x_odom += new_x - self.x + \
            np.random.normal(1, scale=abs(dx) * self.x_noise) if dx != 0 else 0
        self.y_odom += new_y - self.y + \
            np.random.normal(1, scale=abs(dy) * self.y_noise) if dy != 0 else 0

        self.x = new_x
        self.y = new_y

    def controls(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.move(0, -20)
        if pressed[pygame.K_DOWN]:
            self.move(0, 20)
        if pressed[pygame.K_LEFT]:
            self.move(-20, 0)
        if pressed[pygame.K_RIGHT]:
            self.move(20, 0)

    def odometry(self):
        return self.x_odom, self.y_odom

    def Q(self):
        return np.array(
            [[self.z_noise, 0],
             [0, self.z_noise]]
        )

    def detect_landmarks(self):
        detected = []
        for i, landmark in enumerate(self.landmarks):
            dist = math.sqrt((self.x - landmark.x)**2 +
                             (self.y - landmark.y)**2)
            if 0 < dist < self.max_sense_dist and random.random() < self.phit:
                x = landmark.x - self.x + np.random.normal(scale=self.z_noise)
                y = landmark.y - self.y + np.random.normal(scale=self.z_noise)
                detected.append({i: (x, y)})
        return detected

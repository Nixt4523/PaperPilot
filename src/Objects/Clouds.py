from math import cos, sin, radians
from random import randint, choice

import pygame
from pygame import Vector2 as vector


class Cloud:

    def __init__(self, window_width, window_height, layer):
        self.window_width = window_width
        self.window_height = window_height

        self.position = vector(
            randint(0, self.window_width), randint(0, self.window_height)
        )

        alpha = choice([100, 125, 150])
        self.color = (210, 210, 210, alpha)

        self.sizes = [60, 80, 120]
        self.speeds = [1.5, 2, 2.5]

        if layer is True:
            self.sizes = [250, 280, 300]
            self.speeds = [3, 4, 5]
            self.color[-1] = 225

        self.speed = choice(self.speeds)
        self.size = choice(self.sizes)

    def move(self, plane_position):
        self.position -= plane_position * (self.speed)

        if self.position.x < -self.size:
            self.position.x = self.window_width + self.size
        elif self.position.x > self.window_width + self.size:
            self.position.x = -self.size

        if self.position.y < -self.size:
            self.position.y = self.window_height + self.size
        elif self.position.y > self.window_height + self.size:
            self.position.y = -self.size

    def draw(self, window):
        cloud_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            cloud_surface,
            self.color,
            (self.size, self.size),
            self.size,
        )
        window.blit(
            cloud_surface, (self.position.x - self.size, self.position.y - self.size)
        )


class CloudManager:

    def __init__(self, window_width, window_height, num_clouds=10, background=False):
        self.window_width = window_width
        self.window_height = window_height
        self.layer = background
        self.clouds = [
            Cloud(window_width, window_height, self.layer) for _ in range(num_clouds)
        ]

    def update(self, plane_angle):

        plane_velocity = (
            vector(cos(radians(plane_angle)), -sin(radians(plane_angle))) / 10
        )

        for cloud in self.clouds:
            if self.layer == "foreground":
                cloud.move(plane_velocity * 10)
            else:
                cloud.move(plane_velocity)

    def draw(self, window):
        for cloud in self.clouds:
            cloud.draw(window)

    def spawn_clouds(self, plane_angle):

        direction_vector = vector(cos(radians(plane_angle)), sin(radians(plane_angle)))

        for _ in range(randint(1, 3)):
            cloud = Cloud(
                self.window_width,
                self.window_height,
                self.layer,
            )

            if direction_vector.x > 0:
                cloud.position.x = -cloud.size
            elif direction_vector.x < 0:
                cloud.position.x = self.window_width + cloud.size

            if direction_vector.y > 0:
                cloud.position.y = -cloud.size
            elif direction_vector.y < 0:
                cloud.position.y = self.window_height + cloud.size

            self.clouds.append(cloud)

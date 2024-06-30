from math import cos, sin, radians

import pygame
from pygame import Vector2 as vector
from pygame.image import load as load_image
from pygame.transform import rotate, scale_by as scale

from settings import *
from assets import assets


class Plane:

    def __init__(self, window_width, window_height):
        self.original_image = self.load_and_prepare_image()
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=(window_width // 2, window_height // 2))
        self.position = vector(self.rect.center)

        self.plane_angle = 90
        self.speed = PLANE_SPEED

    def load_and_prepare_image(self):
        image = load_image(assets["PLANE_IMAGE"]).convert_alpha()
        return scale(rotate(image, -90), 1)

    def draw(self, window):
        window.blit(self.image, self.rect)

    def move(self, keys, delta_time):

        if keys[pygame.K_a]:
            self.plane_angle = (self.plane_angle + PLANE_TURN_ANGLE) % 360
        if keys[pygame.K_d]:
            self.plane_angle = (self.plane_angle - PLANE_TURN_ANGLE) % 360

        direction = vector(
            cos(radians(-self.plane_angle)), sin(radians(-self.plane_angle))
        )
        self.position += direction * self.speed * delta_time
        self.rect.center = self.position

        self.image = rotate(self.original_image, self.plane_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def window_collision(self, window_width, window_height):

        if self.rect.right < 0:
            self.position.x = window_width
        if self.rect.left > window_width:
            self.position.x = 0

        if self.rect.top > window_height:
            self.position.y = 0
        if self.rect.bottom < 0:
            self.position.y = window_height

        self.rect.center = self.position

    def update(self, window, keys, window_width, window_height, delta_time):
        self.move(keys, delta_time)
        self.window_collision(window_width, window_height)
        self.draw(window)

    def is_collided(self, obj):
        offset = int(obj.rect.left - self.rect.left), int(obj.rect.top - self.rect.top)
        return self.mask.overlap(obj.mask, offset) is not None

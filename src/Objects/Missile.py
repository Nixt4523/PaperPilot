from random import randint, choice
from math import cos, sin, radians, degrees, atan2

import pygame
from pygame import Vector2 as vector
from pygame.image import load as load_image
from pygame.transform import rotate, scale_by as scale

from settings import *
from assets import assets


class Missile(pygame.sprite.Sprite):

    def __init__(self, plane, missile_type, window_width, window_height):
        super().__init__()
        self.plane = plane

        self.type = missile_type
        self.missile_type = [(1, 10), (2, 25), (3, 50)]

        self.window_width = window_width
        self.window_height = window_height

        self.original_image = self.load_and_prepare_image()
        self.image = self.original_image
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.get_spawn_position())
        self.position = vector(self.rect.center)

        self.speed = MISSILE_SPEED + (self.missile_type[self.type][1])
        self.missile_angle = self.calculate_missile_angle()
        self.turn_rate = MISSILE_TURN_ANGLE
        if self.type == 2:
            self.turn_rate += 0.1
        elif self.type == 3:
            self.turn_rate += 0.15

        self.spawn_time = pygame.time.get_ticks()
        self.exploded = False

        self.trails = []
        self.trail_timer = 0

    def load_and_prepare_image(self):
        image = load_image(assets["MISSILE_IMAGE"]).convert_alpha()
        return scale(rotate(image, -90), 1)

    def get_spawn_position(self):

        sides = ["top", "left", "bottom", "right"]
        side = choice(sides)

        if side == "top":
            return vector(randint(0, self.window_width), -self.window_height // 2)
        elif side == "left":
            return vector(-self.window_width // 2, randint(0, self.window_height))
        elif side == "right":
            return vector(
                self.window_width + self.window_width // 2,
                randint(0, self.window_height),
            )
        elif side == "bottom":
            return vector(
                randint(0, self.window_width),
                self.window_height + self.window_height // 2,
            )

    def calculate_missile_angle(self):
        direction = self.plane.position - self.position
        return -degrees(atan2(direction.y, direction.x))

    def draw(self, window):

        if not self.exploded:
            window.blit(self.image, self.rect)

    def move(self, delta_time):
        direction_vector = vector(
            cos(radians(-self.missile_angle)), sin(radians(-self.missile_angle))
        )
        to_plane_vector = self.plane.position - self.position
        angle_to_plane = direction_vector.angle_to(to_plane_vector)

        if abs(angle_to_plane) < 270:
            desired_angle = self.calculate_missile_angle()
            angle_difference = (desired_angle - self.missile_angle + 360) % 360

            if abs(angle_difference) > 2:
                if angle_difference < 270:
                    self.missile_angle += self.turn_rate
                else:
                    self.missile_angle -= self.turn_rate
            else:
                self.missile_angle = desired_angle

        self.missile_angle %= 360

        self.image = rotate(self.original_image, self.missile_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

        direction = vector(
            cos(radians(-self.missile_angle)), sin(radians(-self.missile_angle))
        )

        self.position += direction * self.speed * delta_time
        self.rect.center = self.position

    def window_collision(self):

        if self.rect.right < 0:
            self.position.x = self.window_width
        if self.rect.left > self.window_width:
            self.position.x = 0

        if self.rect.top > self.window_height:
            self.position.y = 0
        if self.rect.bottom < 0:
            self.position.y = self.window_height

        self.rect.center = self.position

    def is_collided(self, missile):
        return pygame.sprite.collide_mask(self, missile)

    def explode(self):
        self.exploded = True

    def update_trail(self, delta_time):

        if pygame.time.get_ticks() - self.trail_timer > choice([30, 80, 100]):
            self.trails.append([self.rect.center, 255, 4])
            self.trail_timer = pygame.time.get_ticks()

        fade_speed = [160, 140, 120]

        for point in self.trails:
            point[1] -= fade_speed[self.type] * delta_time
            if point[1] <= 0:
                self.trails.remove(point)

        self.trails = [point for point in self.trails if point[1] > 0]

    def draw_trail(self, window):

        for point in self.trails:

            color = (0, 0, 0, point[1])

            trail_surface = pygame.Surface(
                (point[2] * 2, point[2] * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(trail_surface, color, (point[2], point[2]), point[2])
            trail_rect = trail_surface.get_rect(center=point[0])
            window.blit(trail_surface, trail_rect)

    def update(self, window, delta_time):
        self.move(delta_time)
        self.window_collision()
        self.draw_trail(window)
        self.update_trail(delta_time)
        self.draw(window)

from random import randint

import pygame
from pygame import Vector2 as vector
from pygame.image import load as load_image
from pygame.transform import rotate

from assets import assets


class Coin(pygame.sprite.Sprite):

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height

        self.original_image = load_image(assets["COIN_IMAGE"])
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.position = vector(self.rect.center)

        self.generate_coin()

        self.angle = 0

    def generate_coin(self):
        offset = 100
        x = randint(
            self.image.get_width() + offset,
            self.window_width - self.image.get_width() - offset,
        )
        y = randint(
            self.image.get_height() + offset,
            self.window_height - self.image.get_height() - offset,
        )

        self.rect.center = (x, y)
        self.position = self.rect.center

    def draw(self, window):
        window.blit(self.image, self.rect)

    def update(self, window):
        self.angle += 0.25
        self.angle %= 360

        self.image = rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.position)

        self.draw(window)

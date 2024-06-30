from random import choice

import pygame
from pygame.math import Vector2 as vector
from pygame.sprite import GroupSingle, groupcollide, collide_mask

from Objects.Plane import Plane
from Objects.Missile import Missile
from Objects.Coin import Coin
from Objects.Clouds import CloudManager

from .game_state import GameState

from settings import *


class PlayingState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.initialize_game_objects()

    def initialize_game_objects(self):
        self.plane = Plane(self.game.window_width, self.game.window_height)
        self.cloud_manager = CloudManager(
            self.game.window_width,
            self.game.window_height,
            num_clouds=12,
        )
        self.top_cloud_manager = CloudManager(
            self.game.window_width,
            self.game.window_height,
            num_clouds=5,
            background=False,
        )

        self.missile_count = MISSILE_COUNT
        self.missile_exploded = 0
        self.missiles = pygame.sprite.Group()
        for _ in range(self.missile_count):
            self.spawn_missiles()

        self.coin = Coin(self.game.window_width, self.game.window_height)
        self.coin_group = GroupSingle(self.coin)
        self.coins_collected = 0
        self.coin_collected = False
        self.last_coin_time = pygame.time.get_ticks()

        self.explosions = []
        self.explosion_time = 0

        self.start_time = pygame.time.get_ticks()
        self.game_over = False

    def spawn_missiles(self):
        self.missiles.add(
            Missile(
                self.plane,
                choice([0, 1, 2]),
                self.game.window_width,
                self.game.window_height,
            )
        )

    def handle_events(self, events, keys):

        for event in events:
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                self.game.running = False

        if not self.game_over:
            self.handle_score()
            self.update_game_objects(keys)
            self.handle_warning()
            self.handle_time()
            self.handle_game_over()

    def update(self, delta_time):
        self.delta_time = delta_time
        if self.game_over:
            self.game_started = False
            self.game.set_state(self.game.game_over_state)

    def render(self):
        self.game.window.fill(BACKGROUND)
        self.cloud_manager.draw(self.game.window)
        self.handle_explosion()
        self.render_missile_trails()
        self.coin_group.draw(self.game.window)
        self.missiles.draw(self.game.window)
        self.game.window.blit(self.plane.image, self.plane.rect)
        self.top_cloud_manager.draw(self.game.window)
        self.handle_score()

    def render_missile_trails(self):
        for missile in self.missiles:
            missile.draw_trail(self.game.window)

    def update_game_objects(self, keys):
        self.cloud_manager.update(self.plane.plane_angle)
        self.top_cloud_manager.update(self.plane.plane_angle)

        self.handle_coin()
        self.handle_collision()
        self.handle_explosion()
        self.handle_missile_self_explosion()

        self.missiles.update(self.game.window, self.delta_time)
        self.plane.update(
            self.game.window,
            keys,
            self.game.window_width,
            self.game.window_height,
            self.delta_time,
        )

    def handle_coin(self):
        if self.coin_collected:
            current_tick = pygame.time.get_ticks()

            if current_tick - self.last_coin_time >= COIN_GENERATION_DURATION:
                self.coin_group.add(
                    Coin(self.game.window_width, self.game.window_height)
                )
                self.coin_collected = False

        if pygame.sprite.spritecollide(
            self.plane, self.coin_group, False, pygame.sprite.collide_mask
        ):
            self.coin_collected = True
            self.game.coin_collection_sound.play()
            self.coin_group.empty()
            self.last_coin_time = pygame.time.get_ticks()
            self.coins_collected += COIN_REWARD

        self.coin_group.update(self.game.window)

    def handle_warning(self):
        plane_position = vector(self.plane.rect.center)
        warning_played = False

        for missile in self.missiles:
            missile_position = vector(missile.rect.center)
            distance = plane_position.distance_to(missile_position)

            if distance <= WARNING_DISTANCE:
                if not self.game.warning_sound.get_num_channels():
                    self.game.warning_sound.play()
                warning_played = True
                break

        if not warning_played:
            self.game.warning_sound.stop()

    def handle_collision(self):

        collided_missiles = groupcollide(
            self.missiles, self.missiles, False, False, collide_mask
        )

        for missile1, missile2_list in collided_missiles.items():
            for missile2 in missile2_list:
                if (
                    missile1 != missile2
                    and not missile1.exploded
                    and not missile2.exploded
                ):
                    self.explode_missiles(missile1, missile2)
        self.remove_exploded_missiles()

    def explode_missiles(self, missile1, missile2):
        missile1.explode()
        missile2.explode()

        self.missile_exploded += 1
        self.missile_count = min(self.missile_count + 1, MAX_MISSILE_COUNT)

        self.explosions.append(
            {
                "position": missile1.rect.center,
                "time": pygame.time.get_ticks(),
            }
        )
        self.game.explosion_sound.play()

    def handle_missile_self_explosion(self):

        for missile in self.missiles:
            if (
                pygame.time.get_ticks() - missile.spawn_time
                >= MISSILE_SELF_DESTRUCTION_TIME
            ):
                missile.explode()
                self.explosions.append(
                    {
                        "position": missile.rect.center,
                        "time": pygame.time.get_ticks(),
                    }
                )
                self.play_explosion_sound()
                missile.kill()

    def handle_explosion(self):

        current_time = pygame.time.get_ticks()

        self.explosions = [
            explosion
            for explosion in self.explosions
            if current_time - explosion["time"] <= EXPLOSION_DURATION
        ]

        for explosion in self.explosions:
            explosion_rect = self.game.explosion_image.get_rect(
                center=explosion["position"]
            )
            self.game.window.blit(self.game.explosion_image, explosion_rect)

    def remove_exploded_missiles(self):

        for missile in self.missiles.copy():
            if (
                missile.exploded
                and pygame.time.get_ticks() - self.explosion_time >= EXPLOSION_DURATION
            ):
                self.missiles.remove(missile)

        while len(self.missiles) < self.missile_count:
            self.spawn_missiles()

    def play_explosion_sound(self):
        self.game.explosion_sound.play()

    def handle_score(self):

        stats = [
            (self.game.clock_image, self.handle_time()),
            (self.game.coin_image, self.coins_collected),
            (self.game.missile_explosion_image, self.missile_exploded),
        ]

        for index, (image, value) in enumerate(stats):
            self.draw_score(image, value, index + 1)

        self.game.score_manager.update_score(
            self.coins_collected * 25 + (self.missile_exploded * 10)
        )

    def draw_score(self, image, value, offset):
        stat_image_rect = image.get_rect(topleft=(25, 50 * offset))

        stat_text_surface = self.game.stat_font.render(str(value), True, FONT)
        stat_text_rect = stat_text_surface.get_rect(topleft=(75, 50 * offset))

        self.game.window.blit(stat_text_surface, stat_text_rect)
        self.game.window.blit(image, stat_image_rect)

    def handle_time(self):

        time_ms = pygame.time.get_ticks() - self.start_time
        time_s = time_ms // 1000

        minutes = time_s // 60
        seconds = time_s % 60

        return f"{minutes}:{seconds}"

    def handle_game_over(self):

        if any(self.plane.is_collided(missile) for missile in self.missiles):
            self.game_over = True
            self.game_started = False

            self.plane.position = (
                self.game.window_width // 2,
                self.game.window_height // 2,
            )
            self.missiles.empty()

            self.score = 0

import sys
import time

import pygame

from States.start_state import StartState
from States.playing_state import PlayingState
from States.game_over_state import GameOverState

from score_manager import ScoreManager

from utils import load_image, load_font, load_sound
from assets import assets


class Game:

    def __init__(self):
        self.initialize_pygame()
        self.setup_game_window()
        self.load_game_assets()
        self.setup_game_sounds_and_fonts()
        self.initialize_score_manager()
        self.setup_states()
        self.set_state(self.start_state)

    def initialize_score_manager(self):
        self.score_manager = ScoreManager()

    def setup_game_window(self):
        self.window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.display_info = pygame.display.Info()

        self.window_width = self.display_info.current_w
        self.window_height = self.display_info.current_h

        self.running = True
        self.game_started = False
        self.delta_time = 0
        self.clock = pygame.time.Clock()

    def load_game_assets(self):
        self.explosion_image = load_image(assets["EXPLOSION_IMAGE"]).convert_alpha()
        self.missile_explosion_image = load_image(
            assets["EXPLOSION_IMAGE_2"]
        ).convert_alpha()
        self.clock_image = load_image(assets["CLOCK_IMAGE"]).convert_alpha()
        self.coin_image = load_image(assets["COIN_IMAGE"]).convert_alpha()

    def setup_game_sounds_and_fonts(self):
        self.explosion_sound = load_sound(assets["EXPLOSION_SOUND"], 0.1)
        self.explosion_sound.fadeout(100)

        self.coin_collection_sound = load_sound(assets["COIN_SOUND"], 0.15)

        self.warning_sound = load_sound(assets["WARNING_SOUND"], 0.1)
        self.warning_sound.fadeout(150)

        self.stat_font = load_font(assets["GAME_FONT"])
        self.game_font = load_font(assets["GAME_FONT"], 200)

    def initialize_pygame(self):
        pygame.init()
        pygame.display.set_caption("PaperPilot")

    def setup_states(self):
        self.start_state = StartState(self)
        self.playing_state = PlayingState(self)
        self.game_over_state = GameOverState(self)

    def set_state(self, state):
        self.state = state

    def handle_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        self.state.handle_events(events, keys)

    def run(self):

        previous_time = time.time()

        while self.running:

            self.delta_time = time.time() - previous_time
            previous_time = time.time()

            self.handle_events()
            self.state.update(self.delta_time)
            self.state.render()

            pygame.display.update()

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()

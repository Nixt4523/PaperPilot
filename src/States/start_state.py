import pygame


from .game_state import GameState

from utils import load_font
from assets import assets
from settings import *


class StartState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.main_font = load_font(assets["GAME_FONT"], 200)
        self.secondary_font = load_font(assets["GAME_FONT"], 42)

    def handle_events(self, events, keys):
        for event in events:
            if (
                not self.game.game_started
                and self.game.running
                and keys[pygame.K_SPACE]
            ):
                self.game.game_started = True
                self.game.set_state(self.game.playing_state)

    def render(self):
        self.game.window.fill(BACKGROUND)
        offset = 40

        paper = self.main_font.render("Paper", True, FONT)
        paper_rect = paper.get_rect(
            center=(
                self.game.window_width // 2 - offset,
                self.game.window_height // 2 - offset,
            )
        )
        plane = self.main_font.render("Plane", True, FONT)
        plane_rect = plane.get_rect(
            center=(
                self.game.window_width // 2 + 120 - offset,
                self.game.window_height // 2 + 160 - offset,
            )
        )

        play_text = self.secondary_font.render("Press [space] to play", True, FONT)
        play_text_rect = play_text.get_rect(
            center=(self.game.window_width // 2, self.game.window_height // 2 + 300)
        )

        self.game.window.blit(paper, paper_rect)
        self.game.window.blit(plane, plane_rect)
        self.game.window.blit(play_text, play_text_rect)

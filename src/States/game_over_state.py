import pygame

from .game_state import GameState

from score_manager import ScoreManager

from utils import load_font
from assets import assets
from settings import *


class GameOverState(GameState):

    def __init__(self, game):
        super().__init__(game)

        self.score_manager = ScoreManager()

        self.game_font = load_font(assets["GAME_FONT"], 80)
        self.score_font = load_font(assets["GAME_FONT"], 500)
        self.quit_font = load_font(assets["GAME_FONT"], 40)

    def handle_events(self, events, keys):
        for event in events:

            if event.type == pygame.KEYDOWN and keys[pygame.K_q]:
                self.game.quit()

    def render(self):
        self.game.window.fill(BACKGROUND)

        game_over_text = self.game_font.render("Game Over", True, FONT)
        game_over_text_rect = game_over_text.get_rect(
            center=(self.game.window_width // 2, self.game.window_height // 2 - 300)
        )

        score = str(self.game.score_manager.score)

        score_text = self.score_font.render(score, True, FONT)
        score_text_rect = score_text.get_rect(
            center=(self.game.window_width // 2, self.game.window_height // 2)
        )

        high_score = str(self.game.score_manager.high_score)

        high_score_text = self.game_font.render(
            f"High Score : {high_score}", True, FONT
        )
        high_score_text_rect = high_score_text.get_rect(
            center=(self.game.window_width // 2, self.game.window_height // 2 + 250)
        )

        quit_text = self.quit_font.render("Press [q] to quit", True, FONT)
        quit_text_rect = quit_text.get_rect(
            center=(self.game.window_width // 2, self.game.window_height // 2 + 350)
        )

        self.game.window.blit(game_over_text, game_over_text_rect)
        self.game.window.blit(score_text, score_text_rect)
        self.game.window.blit(high_score_text, high_score_text_rect)
        self.game.window.blit(quit_text, quit_text_rect)

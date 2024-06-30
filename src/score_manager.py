import os
import json


class ScoreManager:

    def __init__(self):
        self.file_path = "highScore.json"
        self.score = 0
        self.high_score = self.load_high_score()

    def load_high_score(self):

        if not os.path.exists(self.file_path):
            return 0

        with open(self.file_path, "r") as file:
            data = json.load(file)
            high_score = data.get("highScore", 0)
            return high_score

    def save_high_score(self):
        data = {"highScore": self.high_score}
        with open(self.file_path, "w") as file:
            json.dump(data, file)

    def update_score(self, new_score):
        self.score = new_score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def reset_score(self):
        self.score = 0

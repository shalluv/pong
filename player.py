from const import *


class Player:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.ini_x = x
        self.ini_y = y
        self.velocity = 0.0
        self.score = int(0)
        self.initial_velocity = INITIAL_VELOCITY

    def move(self) -> None:
        if self.y + self.velocity > 0 and self.y + self.velocity < SCREEN_HEIGHT - STICK_HEIGHT:
            self.y += self.velocity

    def reset(self, is_reset_score: bool) -> None:
        self.x = self.ini_x
        self.y = self.ini_y
        self.velocity = 0.0
        self.initial_velocity = INITIAL_VELOCITY
        if is_reset_score:
            self.score = int(0)

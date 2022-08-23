from const import *
from pygame import Vector2

from entities.entity import Entity


class Player(Entity):
    ini_speed_y = INITIAL_SPEED

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, STICK_WIDTH, STICK_HEIGHT)
        self.ini_pos = Vector2(x, y)
        self.score = int(0)

    def reset(self, reset_score: bool) -> None:  # type: ignore[override]
        super().reset()
        Player.ini_speed_y = INITIAL_SPEED

        if reset_score:
            self.score = int(0)

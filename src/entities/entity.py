from typing import Union

from const import *
from pygame import Vector2


class Entity:
    def __init__(self, x: Union[float, int], y: Union[float, int], w: Union[float, int], h: Union[float, int]) -> None:
        self.pos = Vector2(x, y)
        self.speed = Vector2()
        self.width = w
        self.height = h

        self.ini_pos = Vector2(x, y)

    def move(self) -> None:
        if self.pos.y + self.speed.y > 0 and self.pos.y + self.speed.y < SCREEN_HEIGHT - self.height and self.pos.x + self.speed.x > 0 and self.pos.x - self.speed.x < SCREEN_WIDTH - self.width:
            self.pos += self.speed

    def reset(self) -> None:
        self.pos.x = self.ini_pos.x
        self.pos.y = self.ini_pos.y
        self.speed = Vector2()

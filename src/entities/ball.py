from random import choice, randint

from const import *
from pygame import Vector2

from entities.entity import Entity
from entities.player import Player


class Ball(Entity):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_SIZE, BALL_SIZE)

    def move(self, player_1: Player, player_2: Player) -> None:  # type: ignore[override]
        if(self.speed == Vector2() and (player_1.speed or player_2.speed)):
            self.speed.x = (randint(30, 70) * 0.01) * INITIAL_SPEED
            self.speed.y = ((INITIAL_SPEED - self.speed.x) * (INITIAL_SPEED + self.speed.x))**0.5

            self.speed.x *= choice([1, -1])
            self.speed.y *= choice([1, -1])
        self.pos += self.speed

    def collision(self, player_1: Player, player_2: Player) -> None:
        if(self.pos.y <= 0):
            self.speed.y = -self.speed.y
        elif(self.pos.y >= SCREEN_HEIGHT - BALL_SIZE):
            self.speed.y = -self.speed.y

        if(self.pos.x <= 0 or self.pos.x >= SCREEN_WIDTH - BALL_SIZE):
            if(self.pos.x <= 0):
                player_2.score += 1
            elif(self.pos.x >= SCREEN_WIDTH - BALL_SIZE):
                player_1.score += 1
            self.reset()
            player_1.reset(False)
            player_2.reset(False)

        if(self.pos.x <= player_1.pos.x + STICK_WIDTH and self.pos.x >= player_1.pos.x and self.pos.y <= player_1.pos.y + STICK_HEIGHT and self.pos.y >= player_1.pos.y):
            self.speed.x = -(self.speed.x + (-0.2 if self.speed.x < 0 else 0.2))
            self.speed.y += 0.2
            Player.ini_speed_y += 0.2
            self.pos.x = player_1.pos.x + STICK_WIDTH + BALL_SIZE
        elif(self.pos.x <= player_2.pos.x + STICK_WIDTH and self.pos.x >= player_2.pos.x and self.pos.y <= player_2.pos.y + STICK_HEIGHT and self.pos.y >= player_2.pos.y):
            self.speed.x = -(self.speed.x + (-0.2 if self.speed.x < 0 else 0.2))
            self.speed.y += 0.2
            Player.ini_speed_y += 0.2
            self.pos.x = player_2.pos.x - STICK_WIDTH - BALL_SIZE

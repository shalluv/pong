from random import choice, randint

from const import *
from player import Player


class Ball:
    def __init__(self) -> None:
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.velocity_x = 0.0
        self.velocity_y = 0.0

    def move(self, player_1: Player, player_2: Player) -> None:
        if(self.velocity_x == 0 and self.velocity_y == 0 and (player_1.velocity or player_2.velocity)):
            self.velocity_x = (
                0.1 + 0.01 * randint(0, 5)) * choice([-1, 1])
            self.velocity_y = (
                0.1 + 0.01 * randint(0, 5)) * choice([-1, 1])
        self.x += self.velocity_x
        self.y += self.velocity_y

        if(self.y <= 0):
            self.velocity_y = -self.velocity_y
        elif(self.y >= SCREEN_HEIGHT - BALL_SIZE):
            self.velocity_y = -self.velocity_y

        if(self.x <= 0 or self.x >= SCREEN_WIDTH - BALL_SIZE):
            if(self.x <= 0):
                player_2.score += 1
            elif(self.x >= SCREEN_WIDTH - BALL_SIZE):
                player_1.score += 1
            self.reset()
            player_1.reset(False)
            player_2.reset(False)

        self.collision(player_1, player_2)

    def collision(self, player_1: Player, player_2: Player) -> None:
        if(self.x <= player_1.x + STICK_WIDTH and self.x >= player_1.x and self.y <= player_1.y + STICK_HEIGHT and self.y >= player_1.y):
            self.velocity_x = -(self.velocity_x +
                                (0.1 if self.velocity_x > 0 else -0.1))
            self.velocity_y = self.velocity_y + \
                (0.1 if self.velocity_y > 0 else -0.1)
            self.x = player_1.x + STICK_WIDTH + BALL_SIZE
            player_1.initial_velocity += 0.1
            player_2.initial_velocity += 0.1
        elif(self.x <= player_2.x + STICK_WIDTH and self.x >= player_2.x and self.y <= player_2.y + STICK_HEIGHT and self.y >= player_2.y):
            self.velocity_x = -(self.velocity_x +
                                (0.1 if self.velocity_x > 0 else -0.1))
            self.velocity_y = self.velocity_y + \
                (0.1 if self.velocity_y > 0 else -0.1)
            self.x = player_2.x - STICK_WIDTH - BALL_SIZE
            player_1.initial_velocity += 0.1
            player_2.initial_velocity += 0.1

    def reset(self) -> None:
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.velocity_x = 0.0
        self.velocity_y = 0.0

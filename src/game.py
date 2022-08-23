import pygame
from pygame import (K_DOWN, K_UP, MOUSEBUTTONDOWN, QUIT, Color, K_s, K_w, Rect,
                    Vector2)
from pygame.surface import Surface

from const import *
from entities.ball import Ball
from entities.player import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()

        self.surface: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)

        self.player_1 = Player(OFFSET_X, (SCREEN_HEIGHT - STICK_HEIGHT) / 2)
        self.player_2 = Player(SCREEN_WIDTH - OFFSET_X, (SCREEN_HEIGHT - STICK_HEIGHT) / 2)
        self.ball = Ball()
        self.game_state = PLAYING

    def start(self) -> None:
        self.reset(True)

        # Game loop
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if (event.type == QUIT):
                    return

                elif (event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and self.game_state != PLAYING):
                    # if click on new game button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if(mouse_x >= NEW_GAME_BUTTON_X and mouse_y > NEW_GAME_BUTTON_Y and mouse_x <= NEW_GAME_BUTTON_X + NEW_GAME_BUTTON_WIDTH and mouse_y <= NEW_GAME_BUTTON_Y + NEW_GAME_BUTTON_HEIGHT):
                        self.game_state = PLAYING
                        self.reset(True)
            # Input handling
            keys = pygame.key.get_pressed()
            self.player_1.speed = Vector2()
            self.player_2.speed = Vector2()
            if(self.game_state == PLAYING):
                if(keys[K_w]):
                    self.player_1.speed.y = -Player.ini_speed_y
                if(keys[K_s]):
                    self.player_1.speed.y = Player.ini_speed_y
                if(keys[K_UP]):
                    self.player_2.speed.y = -Player.ini_speed_y
                if(keys[K_DOWN]):
                    self.player_2.speed.y = Player.ini_speed_y

            # Game processing
            if(self.game_state == PLAYING):
                self.player_1.move()
                self.player_2.move()
                self.ball.move(self.player_1, self.player_2)
                self.ball.collision(self.player_1, self.player_2)
                if(self.player_1.score == WINNING_SCORE):
                    self.game_state = PLAYER_1_WIN
                    self.reset(False)
                elif(self.player_2.score == WINNING_SCORE):
                    self.game_state = PLAYER_2_WIN
                    self.reset(False)

            # Display(output)
            self.surface.fill(WHITE)

            self.draw_stick(self.player_1.pos.x, self.player_1.pos.y, RED)
            self.draw_stick(self.player_2.pos.x, self.player_2.pos.y, BLUE)
            self.render_text(str(self.player_1.score), SCREEN_WIDTH // 2 - 100, 30, RED)
            self.render_text(str(self.player_2.score), SCREEN_WIDTH // 2 + 100 - 26, 30, BLUE)

            if(self.game_state == PLAYER_1_WIN):
                self.render_text("Player 1 wins!", SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 56, RED)
                self.draw_new_game_button(RED)
            elif(self.game_state == PLAYER_2_WIN):
                self.render_text("Player 2 wins!", SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 56, BLUE)
                self.draw_new_game_button(BLUE)
            elif(self.game_state == PLAYING):
                self.draw_line(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT, BLACK)
                self.draw_ball(self.ball.pos.x, self.ball.pos.y, BLACK)

            pygame.display.update()

    def draw_stick(self, x: float, y: float, color: Color):
        pygame.draw.rect(self.surface, color, Rect(x, y, STICK_WIDTH, STICK_HEIGHT))

    def draw_ball(self, x: float, y: float, color: Color):
        pygame.draw.circle(self.surface, color, (x, y), BALL_SIZE)

    def render_text(self, text: str, x: float, y: float, color: Color):
        font = pygame.font.SysFont("Arial", 72)
        text_surface = font.render(text, True, color)
        self.surface.blit(text_surface, (x, y))

    def draw_line(self, x1: float, y1: float, x2: float, y2: float, color: Color):
        pygame.draw.line(self.surface, color, (x1, y1), (x2, y2), 1)

    def draw_new_game_button(self, color: Color) -> None:
        pygame.draw.rect(self.surface, color, Rect(
            NEW_GAME_BUTTON_X, NEW_GAME_BUTTON_Y, NEW_GAME_BUTTON_WIDTH, NEW_GAME_BUTTON_HEIGHT))
        font = pygame.font.SysFont("Arial", 36)
        text_surface = font.render("New Game", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(NEW_GAME_BUTTON_X) + 100, int(NEW_GAME_BUTTON_Y) + 25)
        self.surface.blit(text_surface, text_rect)

    def reset(self, reset_score: bool):
        self.ball.reset()
        self.player_1.reset(reset_score)
        self.player_2.reset(reset_score)

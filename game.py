import pygame
from pygame import Color, Rect
from pygame.surface import Surface

from ball import Ball
from const import *
from player import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.surface: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)

        self.player_1 = Player(OFFSET_X, (SCREEN_HEIGHT - STICK_HEIGHT) / 2)
        self.player_2 = Player(SCREEN_WIDTH - OFFSET_X,
                        (SCREEN_HEIGHT - STICK_HEIGHT) / 2)
        self.ball = Ball()
        self.game_state = PLAYING
    
    def start(self) -> None:
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return
                elif (self.game_state == PLAYING and event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_w):
                        self.player_1.velocity = -self.player_1.initial_velocity
                    if (event.key == pygame.K_s):
                        self.player_1.velocity = self.player_1.initial_velocity
                    if (event.key == pygame.K_UP):
                        self.player_2.velocity = -self.player_2.initial_velocity
                    if (event.key == pygame.K_DOWN):
                        self.player_2.velocity = self.player_2.initial_velocity
                elif event.type == pygame.KEYUP:
                    if (event.key == pygame.K_w or event.key == pygame.K_s):
                        self.player_1.velocity = 0.0
                    if (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                        self.player_2.velocity = 0.0
                elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and self.game_state != PLAYING):
                    # if click on new game button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if(mouse_x >= NEW_GAME_BUTTON_X and mouse_y > NEW_GAME_BUTTON_Y and mouse_x <= NEW_GAME_BUTTON_X + NEW_GAME_BUTTON_WIDTH and mouse_y <= NEW_GAME_BUTTON_Y + NEW_GAME_BUTTON_HEIGHT):
                        self.game_state = PLAYING
                        self.ball.reset()
                        self.player_1.reset(True)
                        self.player_2.reset(True)

            if(self.game_state == PLAYING):
                self.player_1.move()
                self.player_2.move()
                self.ball.move(self.player_1, self.player_2)
                if(self.player_1.score == 10):
                    self.game_state = PLAYER_1_WIN
                    self.ball.reset()
                    self.player_1.reset(False)
                    self.player_2.reset(False)
                elif(self.player_2.score == 10):
                    self.game_state = PLAYER_2_WIN
                    self.ball.reset()
                    self.player_1.reset(False)
                    self.player_2.reset(False)

            self.surface.fill(WHITE)
            self.draw_stick(self.surface, self.player_1.x, self.player_1.y, RED)
            self.draw_stick(self.surface, self.player_2.x, self.player_2.y, BLUE)
            self.render_text(self.surface, str(self.player_1.score),
                        SCREEN_WIDTH // 2 - 100, 30, RED)
            self.render_text(self.surface, str(self.player_2.score),
                        SCREEN_WIDTH // 2 + 100 - 26, 30, BLUE)

            if(self.game_state == PLAYER_1_WIN):
                self.render_text(self.surface, "Player 1 wins!", SCREEN_WIDTH //
                            2 - 180, SCREEN_HEIGHT // 2 - 36, RED)
                self.draw_new_game_button(self.surface, NEW_GAME_BUTTON_X,
                                    NEW_GAME_BUTTON_Y, RED)
            elif(self.game_state == PLAYER_2_WIN):
                self.render_text(self.surface, "Player 2 wins!", SCREEN_WIDTH //
                            2 - 180, SCREEN_HEIGHT // 2 - 36, BLUE)
                self.draw_new_game_button(self.surface, NEW_GAME_BUTTON_X,
                                    NEW_GAME_BUTTON_Y, BLUE)
            elif(self.game_state == PLAYING):
                pygame.draw.line(self.surface, GRAY, (SCREEN_WIDTH // 2, 0),
                                (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 1)
                self.draw_ball(self.surface, self.ball.x, self.ball.y, BLACK)

            pygame.display.update()
            
    def draw_stick(self, surface: Surface, x: float, y: float, color: Color):
        pygame.draw.rect(surface, color, Rect(x, y, STICK_WIDTH, STICK_HEIGHT))


    def draw_ball(self, surface: Surface, x: float, y: float, color: Color):
        pygame.draw.circle(surface, color, (x, y), BALL_SIZE)


    def render_text(self, surface: Surface, text: str, x: float, y: float, color: Color):
        font = pygame.font.SysFont("Arial", 72)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (x, y))


    def draw_new_game_button(self, surface: Surface, x: float, y: float, color: Color) -> None:
        pygame.draw.rect(surface, color, Rect(
            x, y, NEW_GAME_BUTTON_WIDTH, NEW_GAME_BUTTON_HEIGHT))
        font = pygame.font.SysFont("Arial", 36)
        text_surface = font.render("New Game", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(x) + 100, int(y) + 25)
        surface.blit(text_surface, text_rect)

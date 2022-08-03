import random

import pygame
from pygame import Color, Rect
from pygame.surface import Surface

SCREEN_WIDTH: int = int(800)
SCREEN_HEIGHT: int = int(800)
CAPTION: str = str("Pong")

BLACK: Color = Color(0, 0, 0)
WHITE: Color = Color(255, 255, 255)
RED: Color = Color(255, 0, 0)
BLUE: Color = Color(0, 0, 255)
GRAY: Color = Color(100, 100, 100)

STICK_WIDTH: float = 10.0
STICK_HEIGHT: float = 100.0
BALL_SIZE: float = 10.0

STICK_INITIAL_VELOCITY: float = 0.3

OFFSET_X: float = 30.0

PLAYING = 0
PLAYER_1_WIN = 1
PLAYER_2_WIN = 2

NEW_GAME_BUTTON_X: float = SCREEN_WIDTH / 2.0 - 100.0
NEW_GAME_BUTTON_Y: float = SCREEN_HEIGHT / 2.0 + 36.0
NEW_GAME_BUTTON_WIDTH: float = 200.0
NEW_GAME_BUTTON_HEIGHT: float = 50.0


def main():

    pygame.init()
    surface: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)

    player_1_x = float(OFFSET_X)
    player_2_x = float(SCREEN_WIDTH - OFFSET_X - STICK_WIDTH)
    player_1_y = float((SCREEN_HEIGHT - STICK_HEIGHT) / 2)
    player_2_y = float((SCREEN_HEIGHT - STICK_HEIGHT) / 2)
    player_1_velocity = 0.0
    player_2_velocity = 0.0
    ball_x = float(SCREEN_WIDTH / 2)
    ball_y = float(SCREEN_HEIGHT / 2)
    ball_velocity_x = 0.0
    ball_velocity_y = 0.0
    player_1_score = int(0)
    player_2_score = int(0)
    stick_velocity = STICK_INITIAL_VELOCITY

    game_state = PLAYING

    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return
            elif (game_state == PLAYING and event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_w):
                    player_1_velocity = -stick_velocity
                if (event.key == pygame.K_s):
                    player_1_velocity = stick_velocity
                if (event.key == pygame.K_UP):
                    player_2_velocity = -stick_velocity
                if (event.key == pygame.K_DOWN):
                    player_2_velocity = stick_velocity
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_w or event.key == pygame.K_s):
                    player_1_velocity = 0.0
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    player_2_velocity = 0.0
            elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and game_state != PLAYING):
                # if click on new game button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if(mouse_x >= NEW_GAME_BUTTON_X and mouse_y > NEW_GAME_BUTTON_Y and mouse_x <= NEW_GAME_BUTTON_X + NEW_GAME_BUTTON_WIDTH and mouse_y <= NEW_GAME_BUTTON_Y + NEW_GAME_BUTTON_HEIGHT):
                    game_state = PLAYING
                    player_1_x = OFFSET_X
                    player_2_x = SCREEN_WIDTH - OFFSET_X - STICK_WIDTH
                    player_1_y = (SCREEN_HEIGHT - STICK_HEIGHT) / 2.0
                    player_2_y = (SCREEN_HEIGHT - STICK_HEIGHT) / 2.0
                    player_1_velocity = 0.0
                    player_2_velocity = 0.0
                    ball_x = SCREEN_WIDTH / 2.0
                    ball_y = SCREEN_HEIGHT / 2.0
                    ball_velocity_x = 0.0
                    ball_velocity_y = 0.0
                    player_1_score = int(0)
                    player_2_score = int(0)
                    stick_velocity = STICK_INITIAL_VELOCITY

        if(game_state == PLAYING):
            player_1_y = player_move(player_1_y, player_1_velocity)
            player_2_y = player_move(player_2_y, player_2_velocity)
            stick_velocity += 0.00001
            if(ball_velocity_x == 0 and ball_velocity_y == 0 and (player_1_velocity or player_2_velocity)):
                ball_velocity_x = (
                    0.1 + 0.01 * random.randint(0, 5)) * random.choice([-1, 1])
                ball_velocity_y = (
                    0.1 + 0.01 * random.randint(0, 5)) * random.choice([-1, 1])
            ball_x += ball_velocity_x
            ball_y += ball_velocity_y
            if(check_collision(ball_x, ball_y, player_1_x, player_1_y)):
                ball_velocity_x = -ball_velocity_x * 1.1
                ball_velocity_y = ball_velocity_y * 1.1
                ball_x = player_1_x + STICK_WIDTH + BALL_SIZE
            elif(check_collision(ball_x, ball_y, player_2_x, player_2_y)):
                ball_velocity_x = -ball_velocity_x * 1.1
                ball_velocity_y = ball_velocity_y * 1.1
                ball_x = player_2_x - STICK_WIDTH - BALL_SIZE

            if(ball_y <= 0):
                ball_velocity_y = -ball_velocity_y
            elif(ball_y >= SCREEN_HEIGHT - BALL_SIZE):
                ball_velocity_y = -ball_velocity_y

            if(ball_x <= 0):
                player_2_score += 1
                ball_x = (SCREEN_WIDTH - BALL_SIZE) // 2
                ball_y = (SCREEN_HEIGHT - BALL_SIZE) // 2
                ball_velocity_x = 0
                ball_velocity_y = 0
                player_1_y = (SCREEN_HEIGHT - STICK_HEIGHT) // 2
                player_2_y = (SCREEN_HEIGHT - STICK_HEIGHT) // 2
                stick_velocity = STICK_INITIAL_VELOCITY
            elif(ball_x >= SCREEN_WIDTH - BALL_SIZE):
                player_1_score += 1
                ball_x = (SCREEN_WIDTH - BALL_SIZE) // 2
                ball_y = (SCREEN_HEIGHT - BALL_SIZE) // 2
                ball_velocity_x = 0
                ball_velocity_y = 0
                player_1_y = (SCREEN_HEIGHT - STICK_HEIGHT) // 2
                player_2_y = (SCREEN_HEIGHT - STICK_HEIGHT) // 2
                stick_velocity = STICK_INITIAL_VELOCITY

            if(player_1_score == 10):
                render_text(surface, "Player 1 wins!",
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, RED)
                game_state = PLAYER_1_WIN
                ball_x = (SCREEN_WIDTH - BALL_SIZE) // 2
                ball_y = (SCREEN_HEIGHT - BALL_SIZE) // 2
                ball_velocity_x = 0
                ball_velocity_y = 0
                player_1_y = (SCREEN_HEIGHT - STICK_HEIGHT) // 2
                player_2_y = (SCREEN_HEIGHT - STICK_HEIGHT) // 2
                stick_velocity = 0
            elif(player_2_score == 10):
                game_state = PLAYER_2_WIN
                ball_x = (SCREEN_WIDTH - BALL_SIZE) // 2
                ball_y = (SCREEN_HEIGHT - BALL_SIZE) // 2
                ball_velocity_x = 0
                ball_velocity_y = 0
                player_1_y = (SCREEN_HEIGHT - STICK_HEIGHT) // 2
                player_2_y = (SCREEN_HEIGHT - STICK_HEIGHT) // 2
                stick_velocity = 0

        surface.fill(WHITE)
        draw_stick(surface, player_1_x, player_1_y, RED)
        draw_stick(surface, player_2_x, player_2_y, BLUE)
        render_text(surface, str(player_1_score),
                    SCREEN_WIDTH // 2 - 100, 30, RED)
        render_text(surface, str(player_2_score),
                    SCREEN_WIDTH // 2 + 100 - 26, 30, BLUE)

        if(game_state == PLAYER_1_WIN):
            render_text(surface, "Player 1 wins!", SCREEN_WIDTH //
                        2 - 180, SCREEN_HEIGHT // 2 - 36, RED)
            draw_new_game_button(surface, NEW_GAME_BUTTON_X,
                                 NEW_GAME_BUTTON_Y, RED)
        elif(game_state == PLAYER_2_WIN):
            render_text(surface, "Player 2 wins!", SCREEN_WIDTH //
                        2 - 180, SCREEN_HEIGHT // 2 - 36, BLUE)
            draw_new_game_button(surface, NEW_GAME_BUTTON_X,
                                 NEW_GAME_BUTTON_Y, BLUE)
        elif(game_state == PLAYING):
            pygame.draw.line(surface, GRAY, (SCREEN_WIDTH // 2, 0),
                             (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 1)
            draw_ball(surface, ball_x, ball_y, BLACK)

        pygame.display.update()


def draw_stick(surface: Surface, x: float, y: float, color: Color):
    pygame.draw.rect(surface, color, Rect(x, y, STICK_WIDTH, STICK_HEIGHT))


def draw_ball(surface: Surface, x: float, y: float, color: Color):
    pygame.draw.circle(surface, color, (x, y), BALL_SIZE)


def check_collision(ball_x: float, ball_y: float, player_x: float, player_y: float):
    if ball_x <= player_x + STICK_WIDTH and ball_x >= player_x and ball_y <= player_y + STICK_HEIGHT and ball_y >= player_y:
        return True
    return False


def player_move(player_y: float, player_velocity: float):
    if player_y + player_velocity > 0 and player_y + player_velocity < SCREEN_HEIGHT - STICK_HEIGHT:
        player_y += player_velocity
    return player_y


def render_text(surface: Surface, text: str, x: float, y: float, color: Color):
    font = pygame.font.SysFont("Arial", 72)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))


def draw_new_game_button(surface: Surface, x: float, y: float, color: Color) -> None:
    pygame.draw.rect(surface, color, Rect(
        x, y, NEW_GAME_BUTTON_WIDTH, NEW_GAME_BUTTON_HEIGHT))
    font = pygame.font.SysFont("Arial", 36)
    text_surface = font.render("New Game", True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (int(x) + 100, int(y) + 25)
    surface.blit(text_surface, text_rect)


if __name__ == "__main__":
    main()

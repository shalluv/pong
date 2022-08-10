from pygame import Color

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

INITIAL_VELOCITY: float = 0.3

OFFSET_X: float = 30.0

PLAYING = 0
PLAYER_1_WIN = 1
PLAYER_2_WIN = 2

NEW_GAME_BUTTON_X: float = SCREEN_WIDTH / 2.0 - 100.0
NEW_GAME_BUTTON_Y: float = SCREEN_HEIGHT / 2.0 + 36.0
NEW_GAME_BUTTON_WIDTH: float = 200.0
NEW_GAME_BUTTON_HEIGHT: float = 50.0

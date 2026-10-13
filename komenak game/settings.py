import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def asset(name):
    return os.path.join(ASSETS_DIR, name)

WIDTH, HEIGHT = 800, 600
FPS = 60

PLAYER_SIZE = 50
PLAYER_SPEED = 400

ENEMY_START_SIZE = 100
ENEMY_START_SPEED = 300
ENEMY_MAX_SPEED = 1000
ENEMY_MAX_SIZE = 400
ENEMY_GROW = 20
ENEMY_ACCEL = 50

MILK_RADIUS = 50
MILK_PER_LEVEL = 15


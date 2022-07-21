UI_HEIGHT = 150

FPS_LOCK = 60

TILE_SIZE = 64

MAGIC_NUMBER = 0.04

NEIGHBOURS = [(0, 1), (1, 0), (-1, 0), (0, -1)]  # (-1, 1), (1, -1), (1, 1), (-1, -1)

ENEMY_LIFE = 20
DEBUG = True

TIMER = 5

COINS = 50

MAP_TYPE_TO_INDEX = {
    "normal": 0,
    "fighting": 1,
    "flying": 2,
    "poison": 3,
    "ground": 4,
    "rock": 5,
    "bug": 6,
    "ghost": 7,
    "steel": 8,
    "???": 9,
    "fire": 10,
    "water": 11,
    "grass": 12,
    "electric": 13,
    "psychic": 14,
    "ice": 15,
    "dragon": 16,
    "dark": 17,
    "fairy": 18
}

MAP_TYPE_TO_INDEX_PROJECTILES = {
    "normal": 3,
    "fighting": 13,
    "flying": 11,
    "poison": 2,
    "ground": 12,
    "rock": 8,
    "bug": 9,
    "ghost": 7,
    "fire": 0,
    "water": 4,
    "grass": 14,
    "electric": 5,
    "psychic": 10,
    "ice": 1,
    "dragon": 6
}

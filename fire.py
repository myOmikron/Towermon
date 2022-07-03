import pygame as pg
from pygame import gfxdraw
from random import randint

import settings

STEPS_BETWEEN_COLORS = 9
COLORS = ['black', 'red', 'orange', 'yellow', 'white']
PIXEL_SIZE = 4

FIRE_REPS = 8
FIRE_WIDTH = settings.SCREEN_WIDTH // (PIXEL_SIZE * FIRE_REPS)
FIRE_HEIGHT = settings.SCREEN_HEIGHT // PIXEL_SIZE


class DoomFire:
    def __init__(self, screen):
        self.screen = screen
        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surf = pg.Surface([PIXEL_SIZE * FIRE_WIDTH, settings.SCREEN_WIDTH])
        self.fire_surf.set_colorkey('black')

    def do_fire(self):
        for x in range(FIRE_WIDTH):
            for y in range(1, FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    rnd = randint(0, 3)
                    self.fire_array[y - 1][(x - rnd + 1) % FIRE_WIDTH] = color_index - rnd % 2
                else:
                    self.fire_array[y - 1][x] = 0

    def draw_fire(self):
        self.fire_surf.fill('black')
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palette[color_index]
                    gfxdraw.box(self.fire_surf, (x * PIXEL_SIZE, y * PIXEL_SIZE,
                                                 PIXEL_SIZE, PIXEL_SIZE), color)

        for i in range(FIRE_REPS):
            self.screen.blit(self.fire_surf, (self.fire_surf.get_width() * i, 0))

    def get_fire_array(self):
        fire_array = [[0 for i in range(FIRE_WIDTH)] for j in range(FIRE_HEIGHT)]
        for i in range(FIRE_WIDTH):
            fire_array[FIRE_HEIGHT - 1][i] = len(self.palette) - 1
        return fire_array

    def draw_palette(self):
        size = 90
        for i, color in enumerate(self.palette):
            pg.draw.rect(self.screen, color, (i * size, settings.SCREEN_WIDTH // 2, size - 5, size - 5))

    @staticmethod
    def get_palette():
        palette = [(0, 0, 0)]
        for i, color in enumerate(COLORS[:-1]):
            c1, c2 = color, COLORS[i + 1]
            for step in range(STEPS_BETWEEN_COLORS):
                c = pg.Color(c1).lerp(c2, (step + 0.5) / STEPS_BETWEEN_COLORS)
                palette.append(c)
        return palette

    def update(self):
        self.do_fire()

    def draw(self):
        self.draw_fire()

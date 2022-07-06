import sys
import pygame
from pygame.font import Font
from pygame.surface import SurfaceType


class Menu:

    def __init__(self, app):
        self.app = app
        self.show_display = True

        """ Get mid width and mid height position of the current game-window """
        self.x, self.y = pygame.display.get_window_size()
        self.mid_w, self.mid_h = self.x / 2, self.y / 2
        """ create cursor rectangle """
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        """ offset for the cursor, that it is next to Menu Options"""
        self.offset = - 100
        self.font = pygame.font.Font("assets/Gameplay.ttf", 20)
        self.font_big = pygame.font.Font("assets/Gameplay.ttf", 40)

    def draw_text(self, font: Font, text: str, pos_x: int, pos_y: int) -> None:
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x, pos_y)
        self.app.screen.blit(text_surface, text_rect)

    def draw_cursor(self):
        self.draw_text(self.font, '■', self.cursor_rect.x, self.cursor_rect.y)

    def blit_(self):
        self.app.screen.blit(self.app.screen, (0, 0))
        pygame.display.update()
        self.app.reset_keys()

    def display_menu(self):
        ...


class MainMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Start'
        self.startx, self.starty = self.mid_w, self.mid_h + 10
        self.exitx, self.exity = self.mid_w, self.mid_h + 40
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 70
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.show_display = True
        while self.show_display:
            self.app.check_events()
            self.check_input()
            self.app.screen.fill((0, 0, 0))
            self.draw_text(self.font_big, 'Main Menu', self.mid_w, self.mid_h - 40)
            self.draw_text(self.font, 'Start Game', self.startx, self.starty)
            self.draw_text(self.font, 'Exit Game', self.exitx, self.exity)
            self.draw_text(self.font, 'Options', self.optionsx, self.optionsy)
            self.draw_text(self.font, 'Credits', self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_()

    def move_cursor(self):
        if self.app.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

        elif self.app.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.app.START_KEY:
            if self.state == 'Start':
                self.app.playing = True
            elif self.state == 'Options':
                self.app.menu = self.app.options
            elif self.state == 'Exit':
                pygame.quit()
                sys.exit()
            elif self.state == 'Credits':
                self.app.menu = self.app.credits
            self.show_display = False


class OptionsMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 10
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.show_display = True
        while self.show_display:
            self.app.check_events()
            self.check_input()
            self.app.screen.fill((0, 0, 0))
            self.draw_text(self.font_big, 'Options', self.mid_w, self.mid_h - 40)
            self.draw_text(self.font, 'Volume', self.volx, self.voly)
            self.draw_text(self.font, 'Controls', self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_()

    def check_input(self):
        if self.app.BACK_KEY:
            self.app.menu = self.app.main_menu
            self.show_display = False
        elif self.app.UP_KEY or self.app.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.app.START_KEY:
            if self.state == 'Volume':
                self.app.menu = self.app.volume
                self.show_display = False
            elif self.state == 'Controls':
                self.app.menu = self.app.controls
                self.show_display = False


class VolumeMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)

    # Todo

    def display_menu(self):
        self.show_display = True
        while self.show_display:
            self.app.check_events()
            self.check_input()
            self.app.screen.fill((0, 0, 0))
            self.draw_text(self.font_big, 'Volume', self.mid_w, self.mid_h - 40)
            # self.draw_cursor()
            self.blit_()

    def check_input(self):
        if self.app.BACK_KEY:
            self.app.menu = self.app.options
            self.show_display = False


class ControlsMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        # Todo

    def display_menu(self):
        self.show_display = True
        while self.show_display:
            self.app.check_events()
            self.check_input()
            self.app.screen.fill((0, 0, 0))
            self.draw_text(self.font_big, 'Controls', self.mid_w, self.mid_h - 40)
            # self.draw_cursor()
            self.blit_()

    def check_input(self):
        if self.app.BACK_KEY:
            self.app.menu = self.app.options
            self.show_display = False


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.show_display = True
        while self.show_display:
            self.app.check_events()
            if self.app.START_KEY or self.app.BACK_KEY:
                self.app.menu = self.app.main_menu
                self.show_display = False
            self.app.screen.fill((0, 0, 0))
            self.draw_text(self.font_big, 'Credits', self.mid_w, self.mid_h - 40)
            self.draw_text(self.font, 'Made by', self.mid_w, self.mid_h + 10)
            self.draw_text(self.font,'Lukas Mahr', self.mid_w, self.mid_h + 50)
            self.draw_text(self.font,'Niklas Pfister', self.mid_w, self.mid_h + 70)
            self.draw_text(self.font,'Veronika Landerer', self.mid_w, self.mid_h + 90)
            self.draw_text(self.font,'Julian Markovic', self.mid_w, self.mid_h + 110)
            self.blit_()

import sys

import pygame
import pygame as pg
from pygame.font import Font
from utils import image

import json_utils.json_parser
import settings


class Menu:

    def __init__(self, app):
        self.app = app
        self.show_display = True

        """ Get mid width and mid height position of the current game-window """
        self.x, self.y = pg.display.get_window_size()
        self.mid_w, self.mid_h = self.x / 2, self.y / 2
        """ create cursor rectangle """
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        """ offset for the cursor, that it is next to Menu Options"""
        self.offset = - 100
        self.font = pg.font.Font("assets/Font/power green.ttf", 25)
        self.font_big = pg.font.Font("assets/Font/Gameplay.ttf", 40)
        self.error = ""

    def draw_text(self, font: Font, text: str, pos_x: int, pos_y: int) -> None:
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x, pos_y)
        self.app.screen.blit(text_surface, text_rect)

    def draw_cursor(self):
        self.draw_text(self.font, '■', self.cursor_rect.x, self.cursor_rect.y)

    def blit_(self):
        self.app.screen.blit(self.app.screen, (0, 0))
        pg.display.update()
        self.app.reset_keys()

    def display_menu(self):
        pass

    def draw_background(self):
        # Create gradient background
        bg_picture = image.load_png('gradient.png')
        bg_picture = pygame.transform.scale(bg_picture, self.app.screen.get_size())
        self.app.screen.blit(bg_picture, (0, 0))

        #get screen_size for positions
        screen_x, screen_y = self.app.screen.get_size()

        #draw Ellipse with Border
        pos_x =  screen_x - 450
        pos_y = screen_y - 200
        prof_ellipse_outline = pygame.Rect(pos_x, pos_y,400,150)
        pygame.draw.ellipse(self.app.screen, (185,215,205), prof_ellipse_outline)
        pygame.draw.ellipse(self.app.screen, (145, 190, 166), prof_ellipse_outline, width=5)

        #draw professor
        prof_img = image.load_png('professor.png')
        prof_img = pygame.transform.scale(prof_img, (300,300))
        prof_x = pos_x + 40
        prof_y = pos_y - 200
        self.app.screen.blit(prof_img, (prof_x, prof_y))

        #draw pokemon Ellipse:
        pos_x = 100
        pos_y = 400
        poke_ellipse_outline = pygame.Rect(pos_x, pos_y,400,150)
        pygame.draw.ellipse(self.app.screen, (185,215,205), poke_ellipse_outline)
        pygame.draw.ellipse(self.app.screen, (145, 190, 166), poke_ellipse_outline, width=5)

        # draw Pokemon
        pokemon_img = image.load_png('charizard.png')
        pokemon_img = pygame.transform.scale(pokemon_img, (400,400))
        pokemon_img = pygame.transform.flip(pokemon_img, True, False)
        self.app.screen.blit(pokemon_img, (70, 100))
'''
    def create_dropdown(self) -> Dropdown:
        screen = self.app.screen
        x = self.mid_w - 50
        y = self.mid_h + 130
        width = 100
        height = 50
        choices = ["easy", "medium", "hard", "insane"]
        dropdown = Dropdown(screen,x,y,width,height,'Select Diffculty', choices, borderRadius=3, colour=pg.Color('grey'),  direction='down', textHAlign='left')
        return dropdown
'''
class MainMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Start'
        self.difficulties = ['', 'Trainer', 'Gym Leader', 'Elite Four', 'Champ' ]
        self.difficulty = 0

        self.startx, self.starty = self.mid_w, self.mid_h + 10
        self.difficultyx, self.difficultyy = self.mid_w, self.mid_h + 40
        self.exitx, self.exity = self.mid_w, self.mid_h + 70
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 100
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 130

        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        #self.dropdown = self.create_dropdown()


    def display_menu(self):
        self.show_display = True
        pos_x, pos_y = self.app.screen.get_size()
        pos_x = pos_x - 340
        pos_y = pos_y - 250
        pokeball = Pokeball(pos_x,pos_y)
        while self.show_display:
            self.app.check_events()
            self.check_input()
            self.draw_background()
            pokeball.render_ball(self.app.screen)
            pokeball.move()


            if self.error != "":
                self.draw_text(self.font, self.error, self.mid_w, self.mid_h - 150)
            self.draw_text(self.font_big, 'Main Menu', self.mid_w, self.mid_h - 40)
            self.draw_text(self.font, 'Start Game', self.startx, self.starty)
            self.draw_text(self.font, f'<Mode: {self.difficulties[self.difficulty]}>', self.difficultyx, self.difficultyy)
            self.draw_text(self.font, 'Exit Game', self.exitx, self.exity)
            self.draw_text(self.font, 'Options', self.optionsx, self.optionsy)
            self.draw_text(self.font, 'Credits', self.creditsx, self.creditsy)
            self.draw_cursor()
            #pygame_widgets.update(events)
            self.blit_()


    def move_cursor(self):
        if self.app.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.difficultyx + self.offset, self.difficultyy)
                self.state = 'Difficulty'
            elif self.state == 'Difficulty':
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
            elif self.state == 'Difficulty':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.difficultyx + self.offset, self.difficultyy)
                self.state = 'Difficulty'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

        elif self.app.RIGHT_KEY:
            if self.state == 'Difficulty':
                index = self.difficulty + 1
                if index >= len(self.difficulties):
                    self.difficulty = index - len(self.difficulties)
                else: self.difficulty = index
        elif self.app.LEFT_KEY:
            if self.state == 'Difficulty':
                index = self.difficulty - 1
                if index < 0:
                    self.difficulty = index + len(self.difficulties)
                else: self.difficulty = index

    def check_input(self):
        self.move_cursor()
        if self.app.START_KEY:
            if self.state == 'Start':
                    if self.difficulty != 0:
                        self.set_diffictuly(self.difficulty)
                        self.app.playing = True
                        self.error = ""
                    else: self.error = "Please use left and right arrow to select a difficulty mode!"
            elif self.state == 'Options':
                self.error = ""
                self.app.menu = self.app.options
            elif self.state == 'Exit':
                pg.quit()
                sys.exit()
            elif self.state == 'Credits':
                self.error = ""
                self.app.menu = self.app.credits
            self.show_display = False


    def set_diffictuly(self, difficulty: int):
        difficulty_str = self.difficulties[difficulty]
        dict = json_utils.json_parser.get_game_settings(difficulty_str)
        settings.COINS = dict["coins"]
        settings.TIMER = dict["timer"]
        settings.ENEMY_LIFE = dict["enemy_life"]

class OptionsMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 10
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.show_display = True
        pos_x, pos_y = self.app.screen.get_size()
        pos_x = pos_x - 340
        pos_y = pos_y - 250
        pokeball = Pokeball(pos_x, pos_y)
        while self.show_display:
            self.app.check_events()
            self.check_input()
            self.app.screen.fill((0, 0, 0))
            self.draw_background()
            pokeball.render_ball(self.app.screen)
            pokeball.move()
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
        self.state = 'vol_up'
        self.volume = pg.mixer.music.get_volume()
        self.message = 'Use the Up and Down keys to change the volume!'


    def display_menu(self):
        self.show_display = True
        pos_x, pos_y = self.app.screen.get_size()
        pos_x = pos_x - 340
        pos_y = pos_y - 250
        pokeball = Pokeball(pos_x, pos_y)
        while self.show_display:
            self.app.check_events()
            self.check_input()
            self.app.screen.fill((0, 0, 0))
            self.draw_background()
            pokeball.render_ball(self.app.screen)
            pokeball.move()
            self.draw_text(self.font_big, 'Volume', self.mid_w, self.mid_h-40)
            self.draw_text(self.font, self.message, self.mid_w, self.mid_h)
            self.blit_()

    def check_input(self):
        if self.app.BACK_KEY:
            self.app.menu = self.app.options
            self.show_display = False
        elif self.app.UP_KEY: self.volume += 0.1
        elif self.app.DOWN_KEY: self.volume -= 0.1
        pg.mixer.music.set_volume(self.volume)


class ControlsMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        # Todo

    def display_menu(self):
        self.show_display = True
        pos_x, pos_y = self.app.screen.get_size()
        pos_x = pos_x - 340
        pos_y = pos_y - 250
        pokeball = Pokeball(pos_x, pos_y)
        while self.show_display:
            self.app.check_events()
            self.check_input()
            self.app.screen.fill((0, 0, 0))
            self.draw_background()
            pokeball.render_ball(self.app.screen)
            pokeball.move()
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
        pos_x, pos_y = self.app.screen.get_size()
        pos_x = pos_x - 340
        pos_y = pos_y - 250
        pokeball = Pokeball(pos_x, pos_y)
        while self.show_display:
            self.app.check_events()
            if self.app.START_KEY or self.app.BACK_KEY:
                self.app.menu = self.app.main_menu
                self.show_display = False
            self.app.screen.fill((0, 0, 0))
            self.draw_background()
            pokeball.render_ball(self.app.screen)
            pokeball.move()
            self.draw_text(self.font_big, 'Credits', self.mid_w, self.mid_h - 40)
            self.draw_text(self.font, 'Made by', self.mid_w, self.mid_h + 10)
            self.draw_text(self.font,'Lukas Mahr', self.mid_w, self.mid_h + 50)
            self.draw_text(self.font,'Niklas Pfister', self.mid_w, self.mid_h + 70)
            self.draw_text(self.font,'Veronika Landerer', self.mid_w, self.mid_h + 90)
            self.draw_text(self.font,'Julian Markovic', self.mid_w, self.mid_h + 110)
            self.blit_()

class Pokeball():
    def __init__(self, x,y):
        self.x = x - 15
        self.y = y
        self.direction = 'up'
        self.velosity = 3
        self.max_y =  y - 180
        self.min_y = y - 20

    def move(self):
        if self.direction == 'up':
            if self.y >= self.max_y:
                self.y -= self.velosity
            else:
                self.direction = 'down'
        if self.direction == 'down':
            if self.y <= self.min_y:
                self.y += self.velosity
            else: self.direction = 'up'

    def render_ball(self, screen):
        ball_img = image.load_png('pokeball.png')
        ball_img = pygame.transform.scale(ball_img, (30,30))
        screen.blit(ball_img, (self.x, self.y))






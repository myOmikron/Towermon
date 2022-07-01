import sys
import pygame

class Menu():

    def __init__(self, game):
        self.game = game
        self.show_display = True

        """ Get mid width and mid height position of the current game-window """
        self.x, self.y = pygame.display.get_window_size()
        self.mid_w, self.mid_h = self.x/2, self.y/2
        """ create cursor rectangle """
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        """ offset for the cursor, that it is next to Menu Options"""
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 20, self.cursor_rect.x, self.cursor_rect.y)

    def blit_(self):
        self.game.screen.blit(self.game.screen, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

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
            self.game.check_events()
            self.check_input()
            self.game.screen.fill((0, 0, 0))
            self.game.draw_text('Main Menu', 30, self.mid_w, self.mid_h - 40)
            self.game.draw_text('Start Game', 20, self.startx, self.starty)
            self.game.draw_text('Exit Game', 20, self.exitx, self.exity)
            self.game.draw_text('Options', 20, self.optionsx, self.optionsy)
            self.game.draw_text('Credits', 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_()


    def move_cursor(self):
        if self.game.DOWN_KEY:
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

        elif self.game.UP_KEY:
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
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Exit':
                pygame.quit()
                sys.exit()
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
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
            self.game.check_events()
            self.check_input()
            self.game.screen.fill((0, 0, 0))
            self.game.draw_text('Options', 30, self.mid_w, self.mid_h - 40)
            self.game.draw_text('Volume', 20, self.volx, self.voly)
            self.game.draw_text('Controls', 20, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_()





    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.show_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            if self.state == 'Volume':
                self.game.curr_menu = self.game.volume
                self.show_display = False
            elif self.state == 'Controls':
                self.game.curr_menu = self.game.controls
                self.show_display = False

class VolumeMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
    # Todo

    def display_menu(self):
        self.show_display = True
        while self.show_display:
            self.game.check_events()
            self.check_input()
            self.game.screen.fill((0, 0, 0))
            self.game.draw_text('Volume', 30, self.mid_w, self.mid_h - 40)
            #self.draw_cursor()
            self.blit_()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.options
            self.show_display = False

class ControlsMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        #Todo

    def display_menu(self):
        self.show_display = True
        while self.show_display:
            self.game.check_events()
            self.check_input()
            self.game.screen.fill((0, 0, 0))
            self.game.draw_text('Controls', 30, self.mid_w, self.mid_h - 40)
            #self.draw_cursor()
            self.blit_()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.options
            self.show_display = False


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.show_display = True
        while self.show_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.show_display = False
            self.game.screen.fill((0,0,0))
            self.game.draw_text('Credits', 50, self.mid_w , self.mid_h - 40)
            self.game.draw_text('Made by', 25, self.mid_w, self.mid_h + 10)
            self.game.draw_text('Lukas Mahr', 15, self.mid_w, self.mid_h + 50)
            self.game.draw_text('Niklas Pfister', 15, self.mid_w, self.mid_h + 70)
            self.game.draw_text('Veronika Landerer', 15, self.mid_w, self.mid_h + 90)
            self.game.draw_text('Julian Markovic', 15, self.mid_w, self.mid_h + 110)
            self.blit_()
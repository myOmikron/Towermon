import sys

import pygame

import settings
from entities.Test import Test
from entities.level import Level
from entities.player import Player
from utils import image
from menu import*


class Game:
    def __init__(self):
        # Initialize the audio mixer
        pygame.mixer.pre_init(44100, 16, 2, 4096)

        # Game init
        pygame.init()

        # Set fullscreen && double buffering for performance improvement
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)
        x = self.screen.get_width()

        # Set allowed events for performance improvement
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        pygame.display.set_caption("Tower defense")
        pygame.display.set_icon(image.load_png("favicon.png"))

        # Set running and playing variables
        self.running, self.playing, = True, False

        # Set Keys on default for menu actions
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

        self.clock = pygame.time.Clock()

        self.font_name = "assets/Gameplay.ttf"

        # Initialize menu objects
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.volume = VolumeMenu(self)
        self.controls = ControlsMenu(self)

        # set main_menu as current menu
        self.curr_menu = self.main_menu

        self.font_name = "assets/Gameplay.ttf"

        self.click_sound = pygame.mixer.Sound('Sounds/click.wav')

        # Initialize menu objects
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.volume = VolumeMenu(self)
        self.controls = ControlsMenu(self)

        # set main_menu as current menu
        self.curr_menu = self.main_menu

        # Fill screen black
        self.screen.fill((0, 0, 0))

        self.scale = 1

        self.level = Level(self.scale)
        self.player = Player("player.png", self.scale)
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        if settings.DEBUG:
            self.test = Test(self.scale)

    def draw_text(self, text, size, pos_x, pos_y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x, pos_y)
        self.screen.blit(text_surface, text_rect)

    # check events help function for menu
    def check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # help function for menu inputs
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, pos_x, pos_y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x, pos_y)
        self.screen.blit(text_surface, text_rect)

    # check events help function for menu
    def check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                    self.click_sound.play()
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                    self.click_sound.play()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # help function for menu inputs
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def run(self):
        move_north, move_south, move_west, move_east = False, False, False, False
        while self.playing:
            # Trigger clock
            time_delta = self.clock.tick() / 1000

            for event in pygame.event.get():
                # Handle quit event
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.playing = False
                # Handle zooming
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        if self.scale > 0.4:
                            self.scale /= 1.1
                    elif event.y > 0:
                        if self.scale < 2:
                            self.scale *= 1.1
                # Handle player move events
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        move_east = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_w:
                        move_north = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_a:
                        move_west = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_s:
                        move_south = event.type == pygame.KEYDOWN
                    if settings.DEBUG:
                        if event.key == pygame.K_q:
                            if event.type == pygame.KEYDOWN:
                                self.test.set_start(*pygame.mouse.get_pos(), scale=self.scale)
                        if event.key == pygame.K_e:
                            if event.type == pygame.KEYDOWN:
                                self.test.set_end(*pygame.mouse.get_pos(), scale=self.scale)
                        if event.key == pygame.K_r:
                            if event.type == pygame.KEYDOWN:
                                self.test.search()
                        if event.key == pygame.K_t:
                            if event.type == pygame.KEYDOWN:
                                self.test.spawn()

            # Move player
            if move_east:
                # Only move if the opposite direction is not pressed
                if not move_west:
                    self.player.move_east(time_delta)
            elif move_west:
                self.player.move_west(time_delta)
            if move_north:
                # Only move if the opposite direction is not pressed
                if not move_south:
                    self.player.move_north(time_delta)
            elif move_south:
                self.player.move_south(time_delta)

            if settings.DEBUG:
                self.test.update(time_delta)

            # Render map
            self.level.render(time_delta, self.scale)

            if settings.DEBUG:
                self.test.render(self.scale)

            # Render player
            self.player.render(time_delta, self.scale)

            fps = str(int(self.clock.get_fps()))
            fps_t = self.font.render(fps, True, pygame.Color("RED"))
            pygame.display.get_surface().blit(fps_t, (0, 0))

            pygame.display.update()

    def game_loop(self):
        while game.running:
            game.curr_menu.display_menu()
            if self.playing:
                game.run()


if __name__ == '__main__':
    game = Game()
    game.game_loop()

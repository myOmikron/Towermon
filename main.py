import time
from os.path import exists

import pygame
from pygame.mixer import Sound

from menu import *
from utils import image


class Game:
    level: Level
    scale: int
    font: Font
    playing: bool
    screen: pg.SurfaceType
    playlist: [str]

    def __init__(self, screen: pg.SurfaceType):
        # Set Keys on default for menu actions
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.clock = pygame.time.Clock()
        self.screen = screen
        # Set running and playing variables
        self.playing = False
        self.paused = False
        self.playlist = []
        self.level = Level.load_level("level_0.dat")

        # Fill screen black
        self.screen.fill((0, 0, 0))

        self.scale = 1

        # self.player = Player("player.png", self.scale)
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.a = 0;

        # if settings.DEBUG:
        #    self.test = Test(self.scale, self.level.map.grid)

    @staticmethod
    def create_playlist():
        playlist = []
        if exists('assets/audio/Route 1.wav'):
            playlist.append('assets/audio/Route 1.wav')
            playlist.append('assets/audio/Route 1.wav')
        if exists('assets/audio/Route 1.wav'):
            playlist.append('assets/audio/Route 2.wav')
            playlist.append('assets/audio/Route 2.wav')
        if exists('assets/audio/Route 1.wav'):
            playlist.append('assets/audio/Route 3.wav')
            playlist.append('assets/audio/Route 3.wav')
        return playlist

    def run(self):
        move_north, move_south, move_west, move_east = False, False, False, False
        offset = (0, 0)
        counter = 0

        trigger_rerender = False

        while self.a < 1:
            self.level = Level.load_level("level_0.dat")
            self.level.start(self.screen)
            self.a += 1

        self.level.render(self.scale, offset, trigger_rerender)

        self.playlist = self.create_playlist()
        soundtrack = pygame.mixer.music.load(self.playlist[0])
        pygame.mixer.music.play(1, 0, 500)
        self.playlist.pop(0)
        pygame.mixer.music.queue(self.playlist[0])
        self.playlist.pop(0)
        MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(MUSIC_END)

        while self.playing and not self.paused:
            # Trigger clock
            time_delta = self.clock.tick() / 1000

            for event in pygame.event.get():
                # Handle quit event
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.load('assets/audio/Ingido Plateau.wav')
                    pygame.mixer.music.play(-1, 0, 0)
                    self.paused = True

                # Handle Music Playlist
                if event.type == MUSIC_END:
                    if len(self.playlist) == 0:
                        self.playlist = self.create_playlist()
                        pygame.mixer.music.load(self.playlist[0])
                        pygame.mixer.music.play(1, 0, 500)
                        self.playlist.pop(0)
                    if len(self.playlist) > 0:
                        pygame.mixer.music.queue(self.playlist[0])
                        self.playlist.pop(0)
                # Handle zooming
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        if self.scale > 0.4:
                            self.scale /= 1.1
                    elif event.y > 0:
                        if self.scale < 2:
                            self.scale *= 1.1
                # Handle selecting
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # print(event.button)
                    self.level.highlight(pygame.mouse.get_pos(), offset)
                    trigger_rerender = True
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
                    # if event.key == pygame.K_q and event.type == pygame.KEYDOWN:
                    #    self.level.level_spawn()
                    # if settings.DEBUG:
                    #    if event.key == pygame.K_q:
                    #        if event.type == pygame.KEYDOWN:
                    #            self.test.set_start(*pygame.mouse.get_pos(), scale=self.scale)
                    #    if event.key == pygame.K_e:
                    #        if event.type == pygame.KEYDOWN:
                    #            self.test.set_end(*pygame.mouse.get_pos(), scale=self.scale)
                    #    if event.key == pygame.K_r:
                    #        if event.type == pygame.KEYDOWN:
                    #            self.test.search()
                    #    if event.key == pygame.K_t:
                    #        if event.type == pygame.KEYDOWN:
                    #            self.test.spawn()

            # Move player
            if time.time_ns() >= counter:
                if move_east:
                    # Only move if the opposite direction is not pressed
                    if not move_west:
                        new_x = offset[0] + 1
                        if new_x > self.level.map.width - 2 - self.screen.get_width() // (
                                self.scale * settings.TILE_SIZE):
                            new_x = self.level.map.width - 2 - self.screen.get_width() // (
                                    self.scale * settings.TILE_SIZE)
                        if new_x < 0:
                            new_x = 0
                        offset = int(new_x), offset[1]
                        counter = time.time_ns() + 100_000_000
                elif move_west:
                    new_x = offset[0] - 1
                    if new_x < 0:
                        new_x = 0
                    offset = int(new_x), offset[1]
                    counter = time.time_ns() + 100_000_000
                if move_north:
                    # Only move if the opposite direction is not pressed
                    if not move_south:
                        new_y = offset[1] - 1
                        if new_y < 0:
                            new_y = 0
                        offset = offset[0], int(new_y)
                        counter = time.time_ns() + 100_000_000
                elif move_south:
                    new_y = offset[1] + 1
                    if new_y > self.level.map.height - 1 - self.screen.get_height() // (
                            self.scale * settings.TILE_SIZE):
                        new_y = self.level.map.height - 1 - self.screen.get_height() // (
                                self.scale * settings.TILE_SIZE)
                    if new_y < 0:
                        new_y = 0
                    offset = offset[0], int(new_y)
                    counter = time.time_ns() + 100_000_000

            if self.level.game_over:
                # Gameover Sound
                pg.mixer.music.load('assets/audio/Voltorb Flip win.ogg')
                pg.mixer.music.play(0, 0, 0)

                self.playing = False

            # if settings.DEBUG:
            #    self.test.update(time_delta)
            self.level.update(time_delta)

            # Render map
            self.level.render(self.scale, offset, trigger_rerender)

            # if settings.DEBUG:
            #    self.test.render(self.scale)

            # Render player
            # self.player.render(time_delta, self.scale)

            fps = int(self.clock.get_fps())
            fps_t = self.font.render(str(fps), True, pygame.Color("RED"))
            pygame.display.get_surface().blit(fps_t, (0, 0))

            pygame.display.flip()

            trigger_rerender = False


class App:
    screen: pg.SurfaceType
    menu: Menu
    main_menu: Menu
    options_menu: Menu
    credits: Menu
    volume: Menu
    controls: Menu
    game: Game
    font_name: str
    click_sound: Sound
    running: bool = True
    playing: bool = False
    UP_KEY: bool = False
    DOWN_KEY: bool = False
    RIGHT_KEY: bool = False
    LEFT_KEY: bool = False
    START_KEY: bool = False
    BACK_KEY: bool = False

    def __init__(self):
        # Initialize the audio mixer
        pygame.mixer.pre_init(44100, 32, 2, 4096)
        # Game init
        pygame.init()

        # Set fullscreen && double buffering for performance improvement
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)

        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.load('assets/audio/Ingido Plateau.wav')
        pygame.mixer.music.play(1, 0, 0)

        # Set allowed events for performance improvement
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        pygame.display.set_caption("Tower defense")
        pygame.display.set_icon(image.load_png("favicon.png"))

        # Initialize menu objects
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.volume = VolumeMenu(self)
        self.controls = ControlsMenu(self)

        # set main_menu as current menu
        self.menu = self.main_menu
        self.font_name = "assets/Font/Gameplay.ttf"
        self.click_sound = pygame.mixer.Sound('assets/audio/click.wav')

        self.paused = False
        self.new_game = True

    def check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.menu.run_display = False
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
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                    self.click_sound.play()
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                    self.click_sound.play()
                if event.key == pygame.K_a:
                    print(self.main_menu.current_text)
                    if self.main_menu.current_text >= len(self.main_menu.intro_text) - 2:
                        self.main_menu.current_text = 0
                    else:
                        self.main_menu.current_text += 2
                    self.click_sound.play()
                    self.main_menu.draw_textbox()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x > 70 and x < 470 and y > 100 and y < 500:
                    poke_sound = pygame.mixer.Sound('assets/audio/CHARIZARD.ogg')
                    pygame.mixer.Sound.play(poke_sound)

    # help function for menu inputs
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False

    def run(self):
        pg.mixer.music.load('assets/audio/Ingido Plateau.wav')
        pg.mixer.music.play(-1, 0, 0)
        while self.running:
            if self.new_game:
                self.game = Game(self.screen)
                self.new_game = False
            self.menu.display_menu()
            self.game.paused = self.paused
            if self.playing:
                self.game.clock = pygame.time.Clock()
                self.game.playing = self.playing
                self.game.run()
                self.paused = self.game.paused
                if self.game.level.game_over:
                    self.menu = GameOverMenu(self)
                if self.paused:
                    self.menu = ResumeMenu(self)
                    self.playing = False


if __name__ == '__main__':
    app = App()
    app.run()

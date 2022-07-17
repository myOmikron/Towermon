import pygame
from pygame.mixer import Sound

import settings
from entities.Test import Test
from entities.level import Level
from entities.player import Player
from menu import *
from utils import image
from os.path import exists


class Game:
    level: Level
    scale: int
    player: Player
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
        self.playlist = self.create_playlist()

        # Fill screen black
        self.screen.fill((0, 0, 0))

        self.scale = 1
        self.level = Level.load_level("level_0.dat")
        self.player = Player("player.png", self.scale)
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        #if settings.DEBUG:
        #    self.test = Test(self.scale, self.level.map.grid)

    @staticmethod
    def create_playlist():
        playlist = []
        if exists('assets/audio/Route 1.wav'):
            playlist.append('assets/audio/Route 1.mid')
        if exists('assets/audio/Route 1.wav'):
            playlist.append('assets/audio/Route 2.mid')
        if exists('assets/audio/Route 1.wav'):
            playlist.append('assets/audio/Route 3.mid')
        return playlist

    def run(self):
        move_north, move_south, move_west, move_east = False, False, False, False
        self.level.start(self.screen)
        self.level.render(self.scale)

        pygame.mixer.music.load(self.playlist[0])
        pygame.mixer.music.play()
        self.playlist.pop(0)
        pygame.mixer.music.queue(self.playlist[0])
        self.playlist.pop(0)
        MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(MUSIC_END)

        while self.playing:
            # Trigger clock
            time_delta = self.clock.tick() / 1000

            for event in pygame.event.get():
                # Handle quit event
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.playing = False

                # Handle Music Playlist
                if event.type == MUSIC_END:
                    if len(self.playlist) == 0:
                        self.playlist = self.create_playlist()
                        pygame.mixer.music.load(self.playlist[0])
                        pygame.mixer.music.play()
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
                    self.level.highlight(pygame.mouse.get_pos())
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
                    #if settings.DEBUG:
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

            if self.level.game_over:
                self.playing = False

            #if settings.DEBUG:
            #    self.test.update(time_delta)
            self.level.update(time_delta)

            # Render map
            self.level.render(self.scale)

            #if settings.DEBUG:
            #    self.test.render(self.scale)

            # Render player
            self.player.render(time_delta, self.scale)

            fps = str(int(self.clock.get_fps()))
            fps_t = self.font.render(fps, True, pygame.Color("RED"))
            pygame.display.get_surface().blit(fps_t, (0, 0))

            pygame.display.update()


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
        self.game = Game(self.screen)

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
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # help function for menu inputs
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def run(self):
        while self.running:
            self.menu.display_menu()
            if self.playing:
                self.game.playing = self.playing
                self.game.run()
                self.playing = self.game.playing
            pygame.mixer.music.unload()
            pygame.mixer.music.load('assets/audio/Ingido Plateau.wav')
            pygame.mixer.music.play(1, 0, 0)



if __name__ == '__main__':
    app = App()
    app.run()

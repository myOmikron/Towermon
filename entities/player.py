import math

import pygame.sprite

import settings
import utils.image
import utils.transform


class Player(pygame.sprite.Sprite):
    """The player base class.

    :param image_path: Path to the player sprite image
    :param initial_scale: Initial scaling factor
    :param player_speed: Speed of player movement. Defaults to 800.
    """
    def __init__(self, image_path: str, initial_scale: float, player_speed: int = 800):
        super(Player, self).__init__()
        self.image = utils.image.load_png(image_path)
        self.rect = self.image.get_rect()

        self.screen = pygame.display.get_surface()

        self.position = (0, 0)
        self.player_speed = player_speed
        self.scale = initial_scale

    def move_east(self, time_delta: float):
        """Move the player in east direction

        :param time_delta: Time in seconds since the last render cycle
        """
        self.position = self.position[0] + self.player_speed * time_delta, self.position[1]

    def move_west(self, time_delta: float):
        """Move the player in west direction

        :param time_delta: Time in seconds since the last render cycle
        """
        self.position = self.position[0] - self.player_speed * time_delta, self.position[1]

    def move_south(self, time_delta: float):
        """Move the player in south direction

        :param time_delta: Time in seconds since the last render cycle
        """
        self.position = self.position[0], self.position[1] + self.player_speed * time_delta

    def move_north(self, time_delta: float):
        """Move the player in north direction

        :param time_delta: Time in seconds since the last render cycle
        """
        self.position = self.position[0], self.position[1] - self.player_speed * time_delta

    def render(self, time_delta: float, scale: float):
        """Render the player.

        :param time_delta: Time in seconds since the last render cycle
        :param scale: Scale factor
        """
        if self.scale != scale:
            self.scale = scale

        scaled_tile_size = round(settings.TILE_SIZE * scale)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(
            (self.position[0] * scale) + scaled_tile_size/2 - mouse_x,
            (self.position[1] * scale) + scaled_tile_size/2 - mouse_y
        ) * (180 / math.pi)

        self.screen.blit(
            pygame.transform.scale(
                utils.transform.rot_center(self.image, angle),
                (scaled_tile_size, scaled_tile_size)
            ),
            (
                self.position[0] * scale,
                self.position[1] * scale
            )
        )

from typing import List, Tuple, Union

import pygame
from pygame.surface import SurfaceType, Surface

import settings
import utils.image
from json_utils import json_parser


def generate_button_image(background: Surface, pokemon: Surface, pokemon_type: Surface, cost: int):
    """
    Generate an Button image from the background template the pokemon, the type and the cost
    :param background:
    :param pokemon:
    :param pokemon_type:
    :param cost:
    :return:
    """
    font = pygame.font.Font("assets/Font/Gameplay.ttf", 28)
    text = font.render(f"{cost}", True, (0, 0, 0))
    background.blit(pokemon, (26, 9))
    background.blit(pokemon_type, (109, 7))
    background.blit(text, (52, 179))


def generate_all_buttons():
    types = utils.image.load_tile_map("icon_types.png", (96, 32))
    for pokemon in json_parser.get_pokemon_list():
        background = utils.image.load_png("Button-Template.png")
        highlight = utils.image.load_png("Button-Template-Highlight.png")
        _type = json_parser.get_pokemon_data(pokemon)["type"]
        pokemon_image = utils.image.load_png(f"{pokemon}.png")
        _type = types[settings.MAP_TYPE_TO_INDEX.get(_type)][0]
        generate_button_image(background, pokemon_image, _type, 100)
        generate_button_image(highlight, pokemon_image, _type, 100)
        # pygame.image.save(background, f"assets/graphics/buttons/{pokemon}_button_image.png")
        yield background, highlight


class Button:
    image: Surface
    highlight: Surface
    button_screen: Surface
    activated: bool
    position: Tuple[int, int]
    """
    A Basic Button, that has 2 states activated or not activated
    """

    def __init__(self, image: Surface, highlight: Surface) -> None:
        self.image = image
        self.button_screen = pygame.surface.Surface(image.get_size())
        self.activated = False
        self.position = (0, 0)
        self.highlight = highlight

    def render(self) -> None:
        """
        renders the button on its own surface, to switch from activated to deactivated
        :return:
        """
        if self.activated:
            self.button_screen.blit(self.image, (0, 0))
            self.button_screen.blit(self.highlight, (0, 0))
        else:
            self.button_screen.fill((255, 255, 255))
            self.button_screen.blit(self.image, (0, 0))

    def scale(self, dim: Tuple[int, int]) -> None:
        """
        scales the button images to the given dimensions
        :param dim: new (width, height)
        :return: None
        """
        self.image = pygame.transform.scale(self.image, dim)
        self.button_screen = pygame.transform.scale(self.button_screen, dim)
        self.highlight = pygame.transform.scale(self.highlight, dim)


class ButtonGrid:
    position: Tuple[int, int]
    width: int
    height: int
    buttons: List[Button]
    game_screen: SurfaceType
    ui_screen: Surface
    current_selection: Union[int, None]
    """
    A Class to handle a collection of Buttons, so that all ways only one button can be active
    """

    def __init__(self, width: int, height: int, position: Tuple[int, int], buttons: List[Button],
                 game_screen: SurfaceType) -> None:
        """
        Create a Button Grid
        :param width: grid width
        :param height: grid height
        :param position: position of the grid on screen
        :param buttons: list of buttons in the grid
        :param game_screen: surface os the game
        """
        self.ui_screen = pygame.surface.Surface((width, height))
        self.ui_screen.fill((255, 255, 250))
        self.width = width
        self.height = height
        self.position = position
        self.buttons = buttons
        self.game_screen = game_screen
        self.current_selection = None
        self._setup()

    def _setup(self) -> None:
        """
        setup the button grid, resize the buttons, so they fit the width and height of the grid
        :return:
        """
        width = self.width // len(self.buttons)
        x = 0
        for button in self.buttons:
            button.scale((width, self.height))
            button.position = (x, 0)
            x += width
            button.render()
            self.ui_screen.blit(button.button_screen, button.position)
        self.render()

    def _click(self, index) -> None:
        """
        switches the state of the button
        :param index: index of the button from the button list
        :return: None
        """
        self.buttons[index].activated = False if self.buttons[index].activated else True

    def _pixel_to_button_list_index(self, position: Tuple[int, int]) -> int:
        """
        convert pixel coordinates to index of the button list
        :param position:
        :return: index of the button list
        """
        x, y = position
        return int(x / (self.width / len(self.buttons)))

    def click(self, position) -> None:
        """
        Click on the button at the given position, deselects the previews one if a previews one exists
        :param position: mouse coordinates
        :return: None
        """
        index = self._pixel_to_button_list_index(position)
        last_index = self.current_selection
        if self.current_selection is not None:
            if self.current_selection == index:
                self._click(index)
                self.current_selection = None
            else:
                self._click(self.current_selection)
                self._click(index)
                self.current_selection = index
                self.buttons[last_index].render()
                self.ui_screen.blit(self.buttons[last_index].button_screen, self.buttons[last_index].position)
        else:
            self._click(index)
            self.current_selection = index

        self.buttons[index].render()

        self.ui_screen.blit(self.buttons[index].button_screen, self.buttons[index].position)

    def render(self) -> None:
        """
        render the button grid surface on the game surface
        :return:
        """
        self.game_screen.blit(self.ui_screen, self.position)

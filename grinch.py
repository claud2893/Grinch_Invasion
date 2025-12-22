import pygame
import random
from pygame.sprite import Sprite
from utils import resource_path

class Grinch(Sprite):
    """A class to represent a single Grinch in the fleet."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the grinch image and set its rect attribute.
        self.image = pygame.image.load(resource_path('images\grinch.png'))
        self.rect = self.image.get_rect()

        # Start each new grinch near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the grinch's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if grinch is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        self.x += self.settings.grinch_speed * self.settings.fleet_direction
        self.rect.x = self.x
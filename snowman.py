import pygame
from pygame.sprite import Sprite
from utils import resource_path

class Snowman(Sprite):
    """A class to manage the snowman."""

    def __init__(self, ai_game):
        """Initialize the snowman and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the snowman image and get its rect.
        self.image = pygame.image.load(resource_path('images/ship.bmp'))
        self.rect = self.image.get_rect()

        # Start each new snowman at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the snowman's exact horizontal position.
        self.x = float(self.rect.x)

        # Movement flag; start with a snowman that's not moving.
        self.moving_right = False
        self.moving_left = False

    def center_snowman(self):
         """Center the snowman on the screen."""
         self.rect.midbottom = self.screen_rect.midbottom
         self.x = float(self.rect.x)

    def update(self):
        """Update the snowman's position based on the movement flag."""
        # Update the snowman's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.snowman_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.snowman_speed

        # Update rect object with the modified self.x value.
        self.rect.x = self.x

    def blitime(self):
        """Draw the snowman at its current location."""
        self.screen.blit(self.image, self.rect)



import pygame
from pygame.sprite import Sprite
from utils import resource_path

class Bullet(Sprite):
    """A class to manage bullets fired from the snowman."""

    def __init__(self, ai_game):
        """Create a bullet object fired at the snowman's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color
        self.image = pygame.image.load(resource_path("images/bullet.png"))

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.snowman.rect.midtop

        # Store the bullet's position as a float.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bulle up the screen."""
        # Update the exact position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)
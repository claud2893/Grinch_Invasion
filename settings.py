class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (230, 230, 230)
        # Set the background color. 3 values between 0 and 255 in RGB space.

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 30
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 7

        # Alien settings
        self.fleet_drop_speed = 14

        # Scoring settings
        self.alien_points = 50

        # How quickly the game speeds up
        self.speedup_scale = 1.4

        # How quickly the alkien point values increase
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 8
        self.bullet_speed = 10.0
        self.alien_speed = 1.2

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
import sys
# The sys module is used to exit the game when the player quits.
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from snowman import Snowman
from bullet import Bullet
from grinch import Grinch

class GrinchInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the background settings, needed to make Pygame work properly."""
        pygame.init()
        self.clock = pygame.time.Clock()
        """
        The clock ticks once on each pass through the main loop. Anytime the loop processes faster than the rate we
        define, Pygame will calculate the correct amount of time to pause so that the game runs at a consistent rate.
        """
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        """Create the display window in Full Screen mode."""

        pygame.display.set_caption("Grinch Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.snowman = Snowman(self)
        self.bullets = pygame.sprite.Group()
        self.grinches = pygame.sprite.Group()

        self._create_fleet()

        # Start the game in an active state.
        self.game_active = False
        self.game_paused = False
        
        # Make the play button.
        self.play_button = Button(self, "Click HERE to start")

        # Make the pause button.
        self.pause_button = Button(self, "PAUSE")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Watch for keyboards and mouse events.
            self._check_events()
            
            if self.game_active and not self.game_paused:
                self.snowman.update()
                self._update_bullets()
                self._update_grinches()
            
            self._update_screen()
            self.clock.tick(60)
            """
            After initializing pygame, we create an instance of the class Clock, from the pygame.time module. 
            Then we make the clock tick at the end of the while loop in run_game().
            The tick() method takes one argument: the frame rate for the game.
            """
    def _create_grinch(self, x_position, y_position):
         """Create a new grinch and place it in the row."""
         new_grinch = Grinch(self)
         new_grinch.x = x_position
         new_grinch.rect.x = x_position
         new_grinch.rect.y = y_position
         self.grinches.add(new_grinch)

    def _create_fleet(self):
        """Create the fleet of grinches."""
        # Create a grinch and keep adding grinches until there's no room left.
        # Spacing between grinches is one grinch width.
        grinch = Grinch(self)
        grinch_width, grinch_height = grinch.rect.size

        current_x, current_y = grinch_width, grinch_height
        while current_y < (self.settings.screen_height - 9 * grinch_height):
            while current_x < (self.settings.screen_width - 2 * grinch_width):
                self._create_grinch(current_x, current_y)
                current_x += 2 * grinch_width

            # Finished a row; reset x value and increment y value.
            current_x = grinch_width
            current_y += 2 * grinch_height
    
    def _update_bullets(self):
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        self._check_bullet_grinch_collisions()

    def _check_bullet_grinch_collisions(self):
        """Respond to bullet-grinch collisions."""
        # Check for any bullets that have hit grinches.
        # If so, get rid of the bullets that have hit grinches.
        collisions = pygame.sprite.groupcollide(
             self.bullets, self.grinches, True, True)
        
        if collisions:
             for grinches in collisions.values():
                self.stats.score += self.settings.grinch_points * len(grinches)
             self.sb.prep_score()
             self.sb.check_high_score()

        if not self.grinches:
             # Destroy existing bullets and create new fleet.
             self.bullets.empty()
             self._create_fleet()
             self.settings.increase_speed()

            # Increase level.
             self.stats.level += 1
             self.sb.prep_level()
    
    def _update_grinches(self):
         """Check if the fleet is at an edge, then update positions.."""
         self._check_fleet_edges()
         self.grinches.update()

         # Look for grinches-snowman collisions.
         if pygame.sprite.spritecollideany(self.snowman, self.grinches):
              self._snowman_hit()

        # Look for grinches hitting the bottom of the screen.
         self._check_grinches_bottom()

    def _check_fleet_edges(self):
         """Respond appropriately if any grinches have reached an edge."""
         for grinch in self.grinches.sprites():
              if grinch.check_edges():
                   self._change_fleet_direction()
                   break
              
    def _check_grinches_bottom(self):
         """Check if any grinches have reached the bottom of the screen."""
         for grinch in self.grinches.sprites():
              if grinch.rect.bottom >= self.settings.screen_height:
                   # Treat this the same as if the snowman got hit.
                   self._snowman_hit()
                   break

    def _change_fleet_direction(self):
         """Drop the entire and change the fleet's direction."""
         for grinch in self.grinches.sprites():
              grinch.rect.y += self.settings.fleet_drop_speed
         self.settings.fleet_direction *= -1

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     mouse_pos = pygame.mouse.get_pos()
                     self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
         """Start a new game when the player clicks on the button to play."""
         button_clicked = self.play_button.rect.collidepoint(mouse_pos)
         if button_clicked and not self.game_active:
              
              #Hide the mouse cursor.
              pygame.mouse.set_visible(False)

              # Reset the game settings.
              self.settings.initialize_dynamic_settings()

              # Reset the game statistics.
              self.stats.reset_stats()
              self.sb.prep_score()
              self.sb.prep_level()
              self.sb.prep_snowmen()
              self.game_active = True

              # Get rid of any remainin bullets and grinches.
              self.bullets.empty()
              self.grinches.empty()

              # Create a new fleet and center the snowman.
              self._create_fleet()
              self.snowman.center_snowman()
                
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.snowman.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.snowman.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
             self._fire_bullet()
        elif event.key == pygame.K_RETURN:
            self.pause_game()

    def pause_game(self):
         """Toggle pause state and show pause button."""
         if not self.game_paused:
            self.game_paused = True
            pygame.mouse.set_visible(True)
         else:
            self.game_paused = False
            pygame.mouse.set_visible(False)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.snowman.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.snowman.moving_left = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _snowman_hit(self):
         """Respond to the snowman being hit by a grinch."""
         if self.stats.snowmen_left > 0:
            # Decrement snowman_left.
            self.stats.snowmen_left -= 1
            self.sb.prep_snowmen()

            # Get rid of any remaining bullets and grinches.
            self.bullets.empty()
            self.grinches.empty()

            # Create a new fleet and center the snowman.
            self._create_fleet()
            self.snowman.center_snowman()

            # Pause.
            sleep(0.5)

         else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        # Update images on the screen, and flip to the new screen.
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                 bullet.draw_bullet()
            self.snowman.blitime()
            self.grinches.draw(self.screen)

            # Draw the score information.
            self.sb.show_score()

            # Draw the play button if the game is inactive.
            if not self.game_active:
                self.play_button.draw_button()

            # Draw the pause button if the game is paused.
            if self.game_paused:
                self.pause_button.draw_button()

            pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = GrinchInvasion()
    ai.run_game()
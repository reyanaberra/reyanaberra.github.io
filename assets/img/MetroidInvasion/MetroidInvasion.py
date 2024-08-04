import sys
from time import sleep

import pygame

from settings import Settings
from stats import Stats
from health import Health
from scores import Scores
from button import Button
from samus import Samus
from missile import Missile
from metroid import Metroid

class MetroidInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        if self.settings.full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            pygame.display.set_caption("Metroid Invasion")
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
            pygame.display.set_caption("Metroid Invasion")

        # Create an instance to store game statistics and create a scoreboard.
        self.stats = Stats(self)
        self.scores = Scores(self)
        
        self.samus = Samus(self)
        self.missiles = pygame.sprite.Group()
        self.metroids = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.samus.update()
                self._update_missiles()
                self._update_metroids()

            self._update_screen()

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
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self._start_game()

    def _start_game(self):
        """Start the game."""
        if not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            
            # Reset the game scores.
            self.scores.prep_score()
            self.scores.prep_level()
            self.scores.prep_health()
            
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Get rid of any remaining metroids and missiles.
            self.metroids.empty()
            self.missiles.empty()

            # Create a new fleet and center Samus.
            self._create_fleet()
            self.samus.center_samus()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.samus.moving_right = True
            self.samus.look_right = True
            self.samus.look_left = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.samus.moving_left = True
            self.samus.look_right = False
            self.samus.look_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_missile()
        elif event.key == pygame.K_RETURN:
            self._start_game()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.samus.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.samus.moving_left = False

    def _fire_missile(self):
        """Create a new missile and add it to the missiles group."""
        if len(self.missiles) < self.settings.missiles_allowed:
            new_missile = Missile(self)
            self.missiles.add(new_missile)

    def _update_missiles(self):
        """Update position of missiles and get rid of old missiles."""
        # Update missile positions.
        self.missiles.update()

        # Get rid of missiles that have disappeared.
        for missile in self.missiles.copy():
            if missile.rect.bottom <= 0:
                self.missiles.remove(missile)

        self._check_collisions()

    def _check_collisions(self):
        """Respond to missile-metroid collisions."""
        # Remove any missiles and metroids that have collided.

        collisions = pygame.sprite.groupcollide(
            self.missiles, self.metroids, True, True)

        if collisions:
            for metroids in collisions.values():
                self.stats.score += self.settings.metroid_points
            self.scores.prep_score()
            self.scores.check_high_score()

        if not self.metroids:
            # Destroy existing missiles and create new fleet.
            self.missiles.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.scores.prep_level()

    def _samus_hit(self):
        """Respond to Samus being hit by a metroid."""
        if self.stats.samus_health > 1:
            # Decrement samus_health, and update scoreboard.
            self.stats.samus_health -= 1
            self.scores.prep_health()

            # Get rid of any remaning metroids and missiles.
            self.metroids.empty()
            self.missiles.empty()

            # Create a new fleet and center Samus.
            self._create_fleet()
            self.samus.center_samus()

            # Pause.
            sleep(.5)
        else:
            # Decrement samus_health, and update scoreboard.
            self.stats.samus_health -= 1
            self.scores.prep_health()

            # Reset the game
            self.stats.game_active = False

    def _update_metroids(self):
        """
        Check if the fleet is at an edge,
         then update the positions of all metroids in the fleet.
        """
        self._check_fleet_edges()
        self.metroids.update()

        # Look for metroid-samus collisions.
        if pygame.sprite.spritecollideany(self.samus, self.metroids):
            self._samus_hit()

        # Look for metroids hitting the bottom of the screen.
        self._check_metroids_bottom()

    def _create_metroid(self, metroid_number, row_number):
        """Create a metroid and place it in the row."""
        metroid = Metroid(self)
        metroid_width, metroid_height = metroid.rect.size
        metroid.x = metroid_width + 2 * metroid_width * metroid_number
        metroid.rect.x = metroid.x
        metroid.rect.y = metroid_height + 1.5 * metroid.rect.height * row_number
        self.metroids.add(metroid)

    def _create_fleet(self):
        """Create the fleet of metroids."""
        # Create a metroid and find the number of metroids in a row.
        # Spacing between each metroid is equal to one metroid width.
        metroid = Metroid(self)
        metroid_width, metroid_height = metroid.rect.size
        available_space_x = self.settings.screen_width - (1 * metroid_width)
        number_metroids_x = available_space_x // (2 * metroid_width)

        # Determine the number of rows of aliens that fit on the screen.
        samus_height = self.samus.rect.height
        available_space_y = (self.settings.screen_height - 
                            (2 * metroid_height) - samus_height)
        number_rows = available_space_y // (2 * metroid_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for metroid_number in range(number_metroids_x):
                self._create_metroid(metroid_number, row_number)

    def _check_fleet_edges(self):
        """Respond appropriately if any metroids have reached an edge."""
        for metroid in self.metroids.sprites():
            if metroid.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for metroid in self.metroids.sprites():
            metroid.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_metroids_bottom(self):
        """Check if any metroids have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for metroid in self.metroids.sprites():
            if metroid.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if Samus got hit.
                self._samus_hit()
                break

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # clock = pygame.time.Clock()
        # clock.tick(60)
        # self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.settings.bg, (0, 0))
        
        self.samus.blitme()
        for missile in self.missiles.sprites():
            missile.draw_missile()
        self.metroids.draw(self.screen)

        # Draw the score information.
        self.scores.show_score()
        
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screeen visible.
        pygame.display.flip()

if __name__ == "__main__":
    # Make a game instance, and run the game.
    mi = MetroidInvasion()
    mi.run_game()

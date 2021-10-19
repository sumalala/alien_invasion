import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard

class AlienInvasion:
# Overall class to manage game assets and behavior.
    def __init__(self):
    # Initial the game, and create game resources
        pygame.init()
        self.settings = Settings()

        # Set the background color
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Make the Play button
        self.play_button = Button(self, "Play")

        # Create instance Ship
        self.ship = Ship(self)

        # Create group live Bullet
        self.bullets = pygame.sprite.Group()

        # Create group of alien
        self.aliens = pygame.sprite.Group() 
        self.aliens_food = pygame.sprite.Group()
        self.aliens_friend = pygame.sprite.Group()
        self._create_fleet()
        
    def run_game(self):
    # Start main loop for the game
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
        
    def _check_events(self):
    # Respond to the keyboard and mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)              

    def _check_keydown_events(self, event):
    # Respond to key presses
        if event.key == pygame.K_RIGHT:
        # Move the ship to the right
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
        # Move the ship to the left
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
        # Move the ship to the up
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
        # Move the ship to the down
            self.ship.moving_down = True
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_SPACE:
            if self.stats.game_active == False:
                self._check_play_button()
            else:
                # Shot the bullet
                self._fire_bullet()

    def _check_play_button(self):
    # Start a new game when the player clicks Play
        # Reset the game statistics
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.ship.ship_left()

        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.aliens_food.empty()
        self.aliens_friend.empty()
        self.bullets.empty()
        
        # Reset the game settings
        self.stats.set_initial_number()
        self.settings.initialize_dynamic_settings()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

    def _check_keyup_events(self, event):
    # Respond to key releases
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
        # Move the ship to the left
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
        # Move the ship to the up
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
        # Move the ship to the down
            self.ship.moving_down = False

    def _fire_bullet(self):
    # Create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
    # Update images on the screen, and flip to the new screen
        self.screen.fill(self.settings.bg_color)

        # Draw the ship
        self.ship.blitme()

        # Draw bullet
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.aliens_food.draw(self.screen)
        self.aliens_friend.draw(self.screen)

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Draw the score information
        self.sb.show_score()
        
        # Make the most recently drawn screen visible
        pygame.display.flip()
    
    def _update_bullets(self):
    # Update positon of bullets and get rid of old bullets
        # Update bullet positions
        self.bullets.update()
        # Get rid of old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens
        # If so, get rid of the bullet and the alien
        shoot_the_alien = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        shoot_the_alien_food = pygame.sprite.groupcollide(self.bullets, self.aliens_food, True, True)
        shoot_the_alien_friend = pygame.sprite.groupcollide(self.bullets, self.aliens_friend, True, True)

        if shoot_the_alien:
            for aliens in shoot_the_alien.values():
                self.stats.score += self.settings.alien_points
                self.sb.prep_score()
                self.sb.check_high_score()

        if shoot_the_alien_friend or shoot_the_alien_food:
            self._shoot_wrong()

        if not self.aliens and not self.aliens_food:
        # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self.stats.score += (self.stats.alien_friend * 2)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.aliens_friend.empty()
            self.stats.set_initial_number()
            self._create_fleet()
            self.ship.center_ship()
            self.settings.increase_level()

    def _create_fleet(self):
    # Create the fleet of aliens
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (3 * alien_width)
        number_aliens_x = available_space_x // (alien_width)
        
        # Set stats alien number to zero
        if alien.stats.alien == 1 or alien.stats.alien_food == 1 or alien.stats.alien_friend == 1:
            alien.stats.set_initial_number()

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (4 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
    # Create an alien and place it in a row
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width * alien_number + 14 * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 30 + 2 * alien.rect.height * row_number
        # Seperate 3 types to 3 Sprites
        if alien.random_percent < self.settings.alien:
            self.aliens.add(alien)
        elif alien.random_percent >= self.settings.alien and alien.random_percent < (1 - self.settings.alien_friend):
            self.aliens_food.add(alien)
        else:
            self.aliens_friend.add(alien)
        
    def _update_aliens(self):
    # Update alien posistions of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()
        self.aliens_food.update()
        self.aliens_friend.update()

        # Look for alien-ship collisions and delete the alien hitted
        collisions = pygame.sprite.spritecollideany(self.ship, self.aliens)
        if collisions:
            self._ship_hit()
            self.aliens.remove(collisions)
        collisions = pygame.sprite.spritecollideany(self.ship, self.aliens_friend)
        if collisions:
            self._ship_hit()
            self.aliens_friend.remove(collisions)

        # Delete alien_food and bonus the point
        collisions = pygame.sprite.spritecollideany(self.ship, self.aliens_food)
        if collisions:
            self.aliens_food.remove(collisions)
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
    # Respond appropriately if any aliens have reached an edge
        is_change_direction = 0
        for alien in self.aliens.sprites():
            if alien.check_edges():
                is_change_direction = 1
                self._change_fleet_direction()
                break
        if is_change_direction == 0:
            for alien_food in self.aliens_food.sprites():
                if alien_food.check_edges():
                    is_change_direction = 1
                    self._change_fleet_direction()
                    break
        if is_change_direction == 0:
            for alien_friend in self.aliens_friend.sprites():
                if alien_friend.check_edges():
                    self._change_fleet_direction()
                    break
        
    def _change_fleet_direction(self):
    # Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        for alien_food in self.aliens_food.sprites():
            alien_food.rect.y += self.settings.fleet_drop_speed
        for alien_friend in self.aliens_friend.sprites():
            alien_friend.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
    # Respond to the ship being hit by an alien
        if self.stats.ship_left > 1:
            # Decrement ship_left
            self.stats.ship_left -= 1

            # Center the ship
            self.ship.center_ship()

            self.ship.ship_left()
        else:
            self.stats.ship_left -= 1
            self.ship.ship_left()
            self.stats.game_active = False

    def _shoot_wrong(self):
    # Respond when the ship shoot the food or friend
        if self.stats.ship_left > 1:
            # Decrement ship_left
            self.stats.ship_left -= 1
            self.ship.ship_left()
        else:
            self.stats.ship_left -= 1
            self.ship.ship_left()
            self.stats.game_active = False

    def _check_aliens_bottom(self):
    # Check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
                self._ship_hit()
                break
        for alien in self.aliens_food.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
                self._ship_hit()
                break
        for alien in self.aliens_friend.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
                self._ship_hit()
                break

if __name__ == '__main__':
# Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()

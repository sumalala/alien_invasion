import pygame
from random import random
from pygame.sprite import Sprite

class Alien(Sprite):
# A class to represent a single alien in the fleet
    def __init__(self, ai_game):
        # Initialize the Alien and set its position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Load the Alien image and get its rect
        self.image = self.load_random_image()
        self.rect = self.image.get_rect()
        # # Start each new Alien near the top left of the screen
        # self.rect.x = self.rect.width / 4
        # self.rect.y = self.rect.height / 4

        # Store the alient's exac horizontal position
        self.x = float(self.rect.x)

    def load_random_image(self):
    # Load random images and get its rect
        self.random_percent = random()

        if self.random_percent < self.settings.alien:
            self.stats.alien += 1
            return pygame.image.load('image/alien.bmp')
        elif self.random_percent >= self.settings.alien and self.random_percent < (1 - self.settings.alien_friend):
            self.stats.alien_food += 1
            return pygame.image.load('image/alien_food.bmp')
        else:
            self.stats.alien_friend += 1
            return pygame.image.load('image/alien_friend.bmp')

    def update(self):
    # Move alien to the right or left
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
    # Return True if alien is at edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left < screen_rect.left:
            return True
        
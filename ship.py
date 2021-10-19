import pygame

class Ship():
# A class to manage the ship
    def __init__(self, ai_game):
        # Initialize the ship and set its position
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Load the ship image and get its rect
        self.image = pygame.image.load('image\starship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Prepare the initial number of ship image
        self.ship_left()

    def update(self):
        # update ship's position based on the movement flag
        # update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
    # Center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def ship_left(self):
    # Display how many ships left
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 30)
        ship_left = str(self.stats.ship_left)
        self.ship_left_image = self.font.render(ship_left, True, self.text_color, None)

        # Display the number at the top left of the screen
        self.ship_left_rect = self.ship_left_image.get_rect()
        self.ship_left_rect.left = self.screen_rect.left + 20
        self.ship_left_rect.top = self.screen_rect.top + 8

    def blitme(self):
    # Draw the ship at its current location
        self.screen.blit(self.image, self.rect)
        # Draw the current ship left
        self.screen.blit(self.ship_left_image, self.ship_left_rect)
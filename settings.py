class Settings:
# A class to store all settings for Alien Invasion
    def __init__(self):
    # Initialize the game's settings
        # Screen setting
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230,230,230)
    
        # Ship setting
        self.ship_speed = 0.75
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 4
        self.bullet_height = 14
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 4

        # Alien settings
        self.alien_speed = 0.1
        self.fleet_drop_speed = 2
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        # Alien types percentage
        self.alien = 0.7
        self.alien_food = 0.2
        self.alien_friend = 0.1

        # How quickly the game speeds up
        self.speedup_scale = 1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.alien_speed = 0.1
        self.level = 1

        # Scoring
        self.alien_points = 1

    def increase_level(self):
    # Increase speed settings
        if self.level < 4:
            self.alien_speed *= self.speedup_scale
            self.fleet_direction *= -1
            self.fleet_drop_speed *= self.speedup_scale
            self.level += 1
            
    
class GameStats:
# Track statistics for alien invasion
    def __init__(self, ai_game):
    # Initialize statistics
        self.settings = ai_game.settings
        self.reset_stats()
        # Start alien invaion in an active state
        self.game_active = False
        # High score
        self.high_score = 0

        self.set_initial_number()

    def reset_stats(self):
    # Initialize statistics that can change during the game
        self.ship_left = self.settings.ship_limit
        self.score = 0

    def set_initial_number(self):
        # Number of each alien type
        self.alien = 0
        self.alien_food = 0
        self.alien_friend = 0
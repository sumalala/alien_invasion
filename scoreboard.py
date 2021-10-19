import pygame.font

class Scoreboard:
# A class to report scoring information
    def __init__(self, ai_game):
    # initialize scorekeeping attributes
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 30)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
    
    def prep_score(self):
    # Turn the score into a rendered image
        self.score_str = str(self.stats.score)
        self.score_image = self.font.render(self.score_str, True, self.text_color, None)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.top + 8

    def prep_high_score(self):
    # Turn the high score into a rendered image
        high_score = self.stats.high_score
        high_score_str = format(high_score)
        self.high_text_color = (255, 0, 0)
        self.high_score_image = self.font.render(high_score_str, True, self.high_text_color, None)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 8

        # Text "Highscore" settings
        self.hg_text_color = (169, 169, 169)
        self.hg_font = pygame.font.SysFont(None, 30)
        self.hg_msg = "High"

        self.hg_msg_image = self.font.render(self.hg_msg, True, self.hg_text_color, None)
        self.hg_msg_image_rect = self.hg_msg_image.get_rect()
        self.hg_msg_image_rect.centerx = self.high_score_rect.centerx - 50
        self.hg_msg_image_rect.top = self.high_score_rect.top

    def show_score(self):
    # Draw score to the screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.hg_msg_image, self.hg_msg_image_rect)

    def check_high_score(self):
    # Check to see if there's a new high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
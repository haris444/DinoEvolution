import pygame
import random
from game_config import *


class GoldenApple:
    """A collectible golden apple that gives experience when clicked"""

    def __init__(self):
        # Generate random spawn position within the gameplay area only
        x = random.randint(GAMEPLAY_LEFT + 20, GAMEPLAY_RIGHT - 50)
        y = random.randint(50, SCREEN_HEIGHT - 80)  # Y-axis is fine
        self.rect = pygame.Rect(x, y, 30, 30)  # Smaller than enemies

        # Apple properties
        self.color = (255, 215, 0)  # Golden color
        self.outline_color = (255, 165, 0)  # Orange outline
        self.exp_value = GOLDEN_APPLE_EXP_VALUE
        self.name = "Golden Apple"

    def is_clicked_by_player(self, mouse_pos, player):
        """Check if apple was clicked and is within player's attack range (now pet-boosted)"""
        if not self.rect.collidepoint(mouse_pos):
            return False

        # Check if within attack range (now uses pet-boosted range)
        from game_math import calculate_distance
        player_center = (player.rect.centerx, player.rect.centery)
        apple_center = (self.rect.centerx, self.rect.centery)
        distance = calculate_distance(player_center, apple_center)

        return distance <= player.attack_range + self.rect.width / 2

    def get_exp_value(self):
        """Return the experience value of this apple"""
        return self.exp_value
import pygame
from game_config import *
from game_math import calculate_distance


class ShieldFruit:
    """A collectible shield fruit that gives temporary damage immunity"""

    def __init__(self):
        # Generate random spawn position within the gameplay area only
        import random
        x = random.randint(GAMEPLAY_LEFT + 20, GAMEPLAY_RIGHT - 50)
        y = random.randint(50, SCREEN_HEIGHT - 80)  # Y-axis is fine
        self.rect = pygame.Rect(x, y, 30, 30)  # Same size as golden apple

        # Shield fruit properties
        self.color = (80, 180, 255)  # Light blue
        self.outline_color = (0, 100, 255)  # Darker blue outline
        self.shield_duration = 10.0  # 10 seconds of immunity
        self.name = "Shield Fruit"

    def is_clicked_by_player(self, mouse_pos, player):
        """Check if fruit was clicked and is within player's attack range"""
        if not self.rect.collidepoint(mouse_pos):
            return False

        # Check if within attack range (uses pet-boosted range)
        player_center = (player.rect.centerx, player.rect.centery)
        fruit_center = (self.rect.centerx, self.rect.centery)
        distance = calculate_distance(player_center, fruit_center)

        return distance <= player.attack_range + self.rect.width / 2

    def get_shield_duration(self):
        """Return the shield duration in seconds"""
        return self.shield_duration

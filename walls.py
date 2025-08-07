import pygame
from game_config import GRAY


class Wall:
    """A wall obstacle that blocks movement"""

    def __init__(self, x, y, width, height, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color


def create_level_walls():
    """Create the wall layout for the current level"""
    walls = []

    # Top wall with gap on the right side
    walls.append(Wall(120, 140, 280, 25))

    # Bottom wall with gap on the left side
    walls.append(Wall(380, 360, 300, 25))

    # Left wall system (uneven positioning for interesting gameplay)
    walls.append(Wall(120, 140, 25, 150))  # Top part
    walls.append(Wall(110, 320, 25, 80))  # Bottom part (offset inward)

    # Right wall system (uneven positioning)
    walls.append(Wall(680, 165, 25, 120))  # Top part (offset from corner)
    walls.append(Wall(690, 310, 25, 75))  # Bottom part (offset outward)

    # Interior obstacles for more complex navigation
    walls.append(Wall(300, 220, 80, 20))  # Horizontal obstacle
    walls.append(Wall(450, 280, 20, 60))  # Vertical obstacle

    return walls


def create_walls():
    """Main function to create walls - can be expanded for multiple levels"""
    return create_level_walls()
import pygame

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (128, 128, 128)  # GRAY

def create_walls():
    """Create the wall layout for the game"""
    return [
        # Top wall with gap on the right
        Wall(120, 140, 280, 25),  # Left part of top wall
        # Gap here for opening

        # Bottom wall with gap on the left
        Wall(380, 360, 300, 25),  # Right part of bottom wall
        # Gap here for opening

        # Left wall with uneven positioning
        Wall(120, 140, 25, 150),  # Top part of left wall
        Wall(110, 320, 25, 80),   # Bottom part of left wall (offset inward)

        # Right wall with uneven positioning
        Wall(680, 165, 25, 120),  # Top part of right wall (offset from corner)
        Wall(690, 310, 25, 75),   # Bottom part of right wall (offset outward)

        # Some interior obstacles for more interesting layout
        Wall(300, 220, 80, 20),   # Small horizontal obstacle
        Wall(450, 280, 20, 60),   # Small vertical obstacle
    ]
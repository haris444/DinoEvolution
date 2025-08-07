# pets.py - Complete Pet System
import pygame
import math
from game_config import *

# Pet Data - Each pet has stats, cost, and unlock level
PET_DATA = {
    "Damage Doggy": {
        "unlock_level": 1,
        "cost": 5,
        "boost_type": "damage",
        "boost_amount": 2,
        "color": (255, 100, 100),  # Light Red
        "description": "Boosts damage by +2"
    },
    "Health Hamster": {
        "unlock_level": 1,
        "cost": 5,
        "boost_type": "health",
        "boost_amount": 20,
        "color": (100, 255, 100),  # Light Green
        "description": "Boosts max health by +20"
    },
    "Range Owl": {
        "unlock_level": 1,
        "cost": 8,
        "boost_type": "aura",
        "boost_amount": 15,
        "color": (150, 75, 200),  # Purple
        "description": "Increases attack range by +15"
    },
    "Speed Squirrel": {
        "unlock_level": 4,
        "cost": 15,
        "boost_type": "speed",
        "boost_amount": 3,
        "color": (100, 100, 255),  # Light Blue
        "description": "Boosts speed by +3"
    },
    "Regen Rabbit": {
        "unlock_level": 7,
        "cost": 30,
        "boost_type": "regeneration",
        "boost_amount": 0.5,
        "color": (255, 255, 100),  # Light Yellow
        "description": "Boosts health regen by +0.5/sec"
    },
    "Aura Axolotl": {
        "unlock_level": 10,
        "cost": 50,
        "boost_type": "aura",
        "boost_amount": 25,
        "color": (255, 100, 255),  # Light Magenta
        "description": "Increases attack range by +25"
    },
    "Mega Damage Dragon": {
        "unlock_level": 13,
        "cost": 100,
        "boost_type": "damage",
        "boost_amount": 10,
        "color": (255, 0, 0),  # Red
        "description": "Boosts damage by +10"
    },
    "Radar Eagle": {
        "unlock_level": 16,
        "cost": 180,
        "boost_type": "aura",
        "boost_amount": 40,
        "color": (75, 200, 200),  # Cyan
        "description": "Increases attack range by +40"
    },
    "Ultra Health Unicorn": {
        "unlock_level": 16,
        "cost": 200,
        "boost_type": "health",
        "boost_amount": 100,
        "color": (0, 255, 0),  # Green
        "description": "Boosts max health by +100"
    },
    "Lightning Llama": {
        "unlock_level": 19,
        "cost": 500,
        "boost_type": "speed",
        "boost_amount": 15,
        "color": (255, 255, 0),  # Yellow
        "description": "Boosts speed by +15"
    },
    "Cosmic Chameleon": {
        "unlock_level": 19,
        "cost": 600,
        "boost_type": "aura",
        "boost_amount": 60,
        "color": (200, 50, 255),  # Deep Purple
        "description": "Increases attack range by +60"
    }
}


class Pet:
    """A pet that follows the player and provides stat boosts"""

    def __init__(self, pet_name, slot_index):
        self.name = pet_name
        self.data = PET_DATA[pet_name]
        self.slot_index = slot_index  # 0, 1, or 2 for the three slots

        # Visual properties
        self.color = self.data["color"]
        self.size = 20
        self.rect = pygame.Rect(0, 0, self.size, self.size)

        # Following behavior
        self.target_distance = 40 + (slot_index * 25)  # Different distances for each pet
        self.follow_speed = 3
        self.bob_timer = 0  # For cute bobbing animation

    def update(self, player_pos):
        """Update pet position to follow player"""
        # Calculate angle based on slot (pets form a triangle behind player)
        base_angle = math.pi + (self.slot_index - 1) * 0.5  # Spread pets out

        # Calculate target position behind player
        target_x = player_pos[0] + math.cos(base_angle) * self.target_distance
        target_y = player_pos[1] + math.sin(base_angle) * self.target_distance

        # Move towards target position
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 5:  # Only move if not too close
            move_x = (dx / distance) * self.follow_speed
            move_y = (dy / distance) * self.follow_speed
            self.rect.centerx += move_x
            self.rect.centery += move_y

        # Update bobbing animation
        self.bob_timer += 0.2

    def draw(self, screen):
        """Draw the pet with cute bobbing animation"""
        # Calculate bobbing offset
        bob_offset = math.sin(self.bob_timer) * 3
        draw_y = self.rect.centery + bob_offset

        # Draw pet body (circle)
        pygame.draw.circle(screen, self.color, (self.rect.centerx, int(draw_y)), self.size // 2)

        # Draw cute eyes
        eye_color = (0, 0, 0)
        eye_size = 3
        eye_offset = self.size // 4
        pygame.draw.circle(screen, eye_color, (self.rect.centerx - eye_offset, int(draw_y) - 3), eye_size)
        pygame.draw.circle(screen, eye_color, (self.rect.centerx + eye_offset, int(draw_y) - 3), eye_size)

    def get_boost_type(self):
        """Return what stat this pet boosts"""
        return self.data["boost_type"]

    def get_boost_amount(self):
        """Return how much this pet boosts the stat"""
        return self.data["boost_amount"]


def get_available_pets_for_level(level):
    """Return list of pet names that are unlocked at this level"""
    available = []
    for pet_name, pet_data in PET_DATA.items():
        if level >= pet_data["unlock_level"]:
            available.append(pet_name)
    return available


def get_pet_cost(pet_name):
    """Return the cost in wins to buy this pet"""
    return PET_DATA[pet_name]["cost"]


def get_pet_info(pet_name):
    """Return pet information for display"""
    return PET_DATA[pet_name]
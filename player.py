import pygame
from game_config import *
from game_math import calculate_experience_needed, clamp_value
from evolutions import get_evolution_data


class Player:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = START_EXP_TO_LEVEL

        # Set initial evolution and stats
        self._update_evolution_and_stats()

        # Position and size
        self.rect = pygame.Rect(50, 50, 50, 50)

    def _update_evolution_and_stats(self):
        """Update player appearance AND stats based on current level"""
        evolution_data = get_evolution_data(self.level)

        # Update appearance
        self.evolution = evolution_data["name"]
        self.body_color = evolution_data["body_color"]
        self.head_color = evolution_data["head_color"]
        self.specialty = evolution_data["specialty"]

        # Update stats from evolution data
        stats = evolution_data["stats"]
        old_max_health = getattr(self, 'max_health', stats["health"])

        self.max_health = stats["health"]
        self.speed = stats["speed"]
        self.damage = stats["damage"]

        # Handle health on level up
        if hasattr(self, 'health'):
            # Heal 50% of max health on level up + keep current health
            self.health = min(self.max_health, self.health + (self.max_health * 0.5))
        else:
            # First time initialization
            self.health = self.max_health

    def handle_movement(self, keys, walls):
        """Handle player movement with collision detection"""
        # Store current position in case we need to revert
        old_x, old_y = self.rect.x, self.rect.y

        # Apply movement based on key input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player within screen boundaries
        self.rect.x = clamp_value(self.rect.x, 0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = clamp_value(self.rect.y, 0, SCREEN_HEIGHT - self.rect.height)

        # Check for wall collisions and revert if necessary
        if self._check_wall_collision(walls):
            self.rect.x, self.rect.y = old_x, old_y

    def _check_wall_collision(self, walls):
        """Check if player is colliding with any wall"""
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                return True
        return False

    def gain_experience(self, amount):
        """Add experience and handle level up"""
        self.exp += amount
        print(f"Gained {amount} EXP! Total EXP: {self.exp}")

        while self.exp >= self.exp_to_next_level:
            self._level_up()

    def _level_up(self):
        """Handle leveling up with new stat system"""
        self.level += 1
        self.exp -= self.exp_to_next_level  # Keep excess EXP
        self.exp_to_next_level = calculate_experience_needed(self.level)

        # Update evolution and all stats
        self._update_evolution_and_stats()

        print(f"Leveled up to {self.level}! Evolved to {self.evolution}")
        print(f"New stats - Damage: {self.damage}, Health: {self.max_health}, Speed: {self.speed}")
        print(f"Specialty: {self.specialty}")

    def take_damage(self, amount):
        """Reduce health by damage amount"""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal_over_time(self):
        """Slowly regenerate health when not at maximum"""
        if self.health > 0 and self.health < self.max_health:
            self.health += self.max_health / 1000  # Heal 0.1% of max health per frame
            if self.health > self.max_health:
                self.health = self.max_health

    def can_buy_pet(self):
        """Check if player is high enough level to buy a pet"""
        return self.level >= PET_UNLOCK_LEVEL

    def is_alive(self):
        """Check if player is still alive"""
        return self.health > 0
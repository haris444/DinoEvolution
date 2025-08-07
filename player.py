import pygame
from game_config import *
from game_math import calculate_experience_needed, clamp_value


class Player:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = START_EXP_TO_LEVEL

        # Set initial evolution
        self._update_evolution()

        # Position and size
        self.rect = pygame.Rect(50, 50, 50, 50)

        # Health system
        self.health = PLAYER_START_HEALTH
        self.max_health = PLAYER_START_HEALTH
        self.speed = PLAYER_SPEED

    def _update_evolution(self):
        """Update player appearance based on current level"""
        if self.level in EVOLUTIONS:
            evolution_data = EVOLUTIONS[self.level]
            self.evolution = evolution_data["name"]
            self.body_color = evolution_data["body_color"]
            self.head_color = evolution_data["head_color"]
        else:
            # Use the highest available evolution if level exceeds defined evolutions
            max_level = max(EVOLUTIONS.keys())
            evolution_data = EVOLUTIONS[max_level]
            self.evolution = evolution_data["name"]
            self.body_color = evolution_data["body_color"]
            self.head_color = evolution_data["head_color"]

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
        """Handle leveling up and stat increases"""
        self.level += 1
        self.exp -= self.exp_to_next_level  # Keep excess EXP
        self.exp_to_next_level = calculate_experience_needed(self.level)

        # Double health and max health on level up
        self.max_health *= 2
        self.health = self.max_health  # Full heal on level up

        # Update appearance
        self._update_evolution()

        print(f"Leveled up to {self.level}! Evolved to {self.evolution}")

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
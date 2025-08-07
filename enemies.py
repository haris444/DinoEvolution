import pygame
import random
from game_config import *
from game_math import (
    generate_random_spawn_position,
    calculate_enemy_stats_for_level,
    calculate_distance,
    normalize_vector,
    clamp_value
)


class Enemy:
    def __init__(self, walls, player_level=1):
        # Generate spawn position outside gameplay area
        x, y = generate_random_spawn_position()
        self.rect = pygame.Rect(x, y, 40, 40)

        # Generate random appearance
        self._generate_random_appearance()

        # Set stats based on player level
        self._set_stats_for_level(player_level)

    def _generate_random_appearance(self):
        """Create random enemy appearance from available parts"""
        self.head, self.head_color = random.choice(ENEMY_HEADS)
        self.body, self.body_color = random.choice(ENEMY_BODIES)
        self.accessory, self.accessory_color = random.choice(ENEMY_ACCESSORIES)
        self.name = f"{self.head}-{self.body}-{self.accessory}"

    def _set_stats_for_level(self, player_level):
        """Set enemy stats based on player level using mathematical scaling"""
        enemy_stats = calculate_enemy_stats_for_level(player_level)
        self.health = enemy_stats["health"]
        self.max_health = enemy_stats["health"]
        self.speed = random.randint(enemy_stats["min_speed"], enemy_stats["max_speed"])
        self.attack_damage = random.randint(enemy_stats["min_damage"], enemy_stats["max_damage"])
        self.last_attack = 0

    def update_movement(self, player, walls):
        """Move towards player while avoiding walls"""
        # Calculate direction to player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        # Normalize direction and apply speed
        norm_dx, norm_dy = normalize_vector(dx, dy)
        move_x = norm_dx * self.speed
        move_y = norm_dy * self.speed

        # Try to move towards player
        self._attempt_movement(move_x, move_y, walls)

        # Keep enemies near gameplay area (allow slight off-screen movement)
        self.rect.x = clamp_value(self.rect.x, GAMEPLAY_LEFT - 12, GAMEPLAY_RIGHT + 12)
        self.rect.y = clamp_value(self.rect.y, GAMEPLAY_TOP - 12, GAMEPLAY_BOTTOM + 12)

    def _attempt_movement(self, move_x, move_y, walls):
        """Try to move, handling wall collisions intelligently"""
        # Store original position
        old_x, old_y = self.rect.x, self.rect.y

        # Try full movement
        self.rect.x += int(move_x)
        self.rect.y += int(move_y)

        # If we hit a wall, try alternative movements
        if self._check_wall_collision(walls):
            self.rect.x, self.rect.y = old_x, old_y  # Reset position

            # Try moving only horizontally
            self.rect.x += int(move_x)
            if self._check_wall_collision(walls):
                self.rect.x = old_x  # Reset horizontal movement

                # Try moving only vertically
                self.rect.y += int(move_y)
                if self._check_wall_collision(walls):
                    self.rect.y = old_y  # Reset if that also fails

    def _check_wall_collision(self, walls):
        """Check if enemy is colliding with any wall"""
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                return True
        return False

    def can_attack_player(self, player):
        """Check if player is within attack range"""
        distance = calculate_distance(
            (player.rect.centerx, player.rect.centery),
            (self.rect.centerx, self.rect.centery)
        )
        return distance < ENEMY_ATTACK_RANGE

    def attempt_attack(self, player):
        """Attack player if cooldown has passed"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack > ENEMY_ATTACK_COOLDOWN:
            self.last_attack = current_time
            player.take_damage(self.attack_damage)
            print(f"{self.name} attacked for {self.attack_damage} damage!")
            return True
        return False

    def take_damage(self, amount):
        """Reduce health and return True if enemy dies"""
        self.health -= amount
        return self.health <= 0

    def get_health_percentage(self):
        """Get health as a percentage for health bar display"""
        if self.max_health == 0:
            return 0
        return self.health / self.max_health
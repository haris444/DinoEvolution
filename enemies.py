import pygame
import random
from game_config import *
from game_math import (
    generate_random_spawn_position,
    calculate_enemy_stats_for_level,
    calculate_boss_stats_for_level,
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
        self.is_boss = False

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
            # No need to check shield here - the player.take_damage method handles that
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


class Boss(Enemy):
    """A much stronger boss enemy with 10-30x health."""

    def __init__(self, walls, player_level=1):
        super().__init__(walls, player_level)
        self.rect.width = 80  # Boss is twice as wide
        self.rect.height = 80 # Boss is twice as tall

    def _generate_random_appearance(self):
        """Bosses have a unique, royal appearance."""
        self.head, self.head_color = ("Crown", (255, 215, 0))  # Gold
        self.body, self.body_color = ("Royal Robe", (75, 0, 130))  # Indigo
        self.accessory, self.accessory_color = ("Scepter", (192, 192, 192))  # Silver
        self.name = "The Meme King"

    def _set_stats_for_level(self, player_level):
        """Set boss stats to be much higher than normal enemies."""
        # Get the stats of a normal enemy for the current level
        normal_enemy_stats = calculate_enemy_stats_for_level(player_level)
        normal_enemy_health = normal_enemy_stats["health"]

        # --- Health Boost! ---
        # Boss health is 10-30x a normal enemy's health
        health_multiplier = random.uniform(10, 30)
        self.health = int(normal_enemy_health * health_multiplier)
        self.max_health = self.health

        # Boss speed is slightly slower to make it a bigger target
        self.speed = random.randint(
            normal_enemy_stats["min_speed"],
            normal_enemy_stats["max_speed"]
        )
        self.speed = max(1, self.speed -1) # Ensure speed is at least 1 but slower

        # Boss damage is also higher
        damage_multiplier = random.uniform(2, 4)
        self.attack_damage = random.randint(
            int(normal_enemy_stats["min_damage"] * damage_multiplier),
            int(normal_enemy_stats["max_damage"] * damage_multiplier)
        )
        self.last_attack = 0
import pygame
import random
from game_rules import *

class Enemy:
    def __init__(self, walls, player_level=1):
        # Spawn enemies slightly off-screen so they can move in
        side = random.randint(0, 3)
        if side == 0:  # Top
            x, y = random.randint(0, SCREEN_WIDTH - 40), -40  # Spawn above screen
        elif side == 1:  # Right
            x, y = SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - 40)  # Spawn right of screen
        elif side == 2:  # Bottom
            x, y = random.randint(0, SCREEN_WIDTH - 40), SCREEN_HEIGHT  # Spawn below screen
        else:  # Left
            x, y = -40, random.randint(0, SCREEN_HEIGHT - 40)  # Spawn left of screen

        self.rect = pygame.Rect(x, y, 40, 40)

        # Generate random enemy parts
        self.head, self.head_color = random.choice(ENEMY_HEADS)
        self.body, self.body_color = random.choice(ENEMY_BODIES)
        self.accessory, self.accessory_color = random.choice(ENEMY_ACCESSORIES)
        self.name = f"{self.head}-{self.body}-{self.accessory}"

        # Get stats based on player level
        enemy_stats = get_enemy_stats_for_level(player_level)
        self.health = enemy_stats["health"]
        self.max_health = enemy_stats["health"]
        self.speed = random.randint(enemy_stats["min_speed"], enemy_stats["max_speed"])
        self.attack_damage = random.randint(enemy_stats["min_damage"], enemy_stats["max_damage"])
        self.last_attack = 0

    def move_towards_player(self, player, walls):
        # Store original position for collision rollback
        old_x, old_y = self.rect.x, self.rect.y

        # Calculate direction vector to player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # Move towards player if distance is greater than zero
        if distance > 0:
            # Normalize direction and apply speed
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            self.rect.x += int(move_x)
            self.rect.y += int(move_y)

        # Keep enemies on screen - allow slight off-screen but not too far
        self.rect.x = max(-12, min(SCREEN_WIDTH + 12, self.rect.x))
        self.rect.y = max(-12, min(SCREEN_HEIGHT + 12, self.rect.y))

        # Check collision with walls
        hit_wall = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                hit_wall = True
                break

        # If we hit a wall, try alternative movement
        if hit_wall:
            self.rect.x, self.rect.y = old_x, old_y  # Revert position

            # Try moving only horizontally
            self.rect.x += int(move_x) if distance > 0 else 0
            wall_hit_again = any(self.rect.colliderect(wall.rect) for wall in walls)

            if wall_hit_again:
                self.rect.x = old_x  # Revert horizontal movement
                # Try moving only vertically
                self.rect.y += int(move_y) if distance > 0 else 0
                if any(self.rect.colliderect(wall.rect) for wall in walls):
                    self.rect.y = old_y  # Revert if that also hits a wall

    def can_attack_player(self, player):
        distance = ((player.rect.centerx - self.rect.centerx) ** 2 +
                    (player.rect.centery - self.rect.centery) ** 2) ** 0.5
        return distance < ENEMY_ATTACK_RANGE

    def attack_player(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack > ENEMY_ATTACK_COOLDOWN:
            self.last_attack = current_time
            player.take_damage(self.attack_damage)
            print(f"{self.name} attacked for {self.attack_damage} damage!")

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
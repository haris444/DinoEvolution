import pygame
import random
from game_rules import *

# Colors for drawing
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
SILVER = (192, 192, 192)


class Particle:
    """Particle class for explosion effect (red and orange only)"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)  # Random velocity
        self.vy = random.uniform(-2, 2)
        self.color = random.choice([RED, ORANGE])  # Only red or orange
        self.lifetime = PARTICLE_LIFETIME

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)


class Pet:
    """Pet class for generating passive EXP"""

    def __init__(self):
        self.exp_per_second = PET_EXP_PER_SECOND
        self.last_update = pygame.time.get_ticks()
        self.rect = pygame.Rect(700, 450, 30, 30)
        self.color = YELLOW

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= 1000:
            self.last_update = now
            return self.exp_per_second
        return 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.circle(screen, CYAN, (self.rect.centerx, self.rect.top + 10), 10)


def draw_background(screen):
    """Draw gradient background"""
    for y in range(SCREEN_HEIGHT):
        color_intensity = max(0, min(255, int(135 - y * 0.2)))
        color = (color_intensity, min(255, int(206 - y * 0.1)), min(255, int(235 - y * 0.15)))
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))


def draw_player(screen, player):
    """Draw the player character with attack range aura"""
    # Draw green aura (attack range)
    aura_surface = pygame.Surface((PLAYER_ATTACK_RANGE * 2, PLAYER_ATTACK_RANGE * 2), pygame.SRCALPHA)
    pygame.draw.circle(aura_surface, (255, 192, 203, 50), (PLAYER_ATTACK_RANGE, PLAYER_ATTACK_RANGE), PLAYER_ATTACK_RANGE)
    aura_rect = aura_surface.get_rect()
    aura_rect.center = player.rect.center
    screen.blit(aura_surface, aura_rect)

    # Draw player body and head
    pygame.draw.rect(screen, player.body_color, player.rect)
    head_pos = (player.rect.centerx, player.rect.top + 10)
    pygame.draw.circle(screen, player.head_color, head_pos, 15)


def draw_enemy(screen, enemy, font):
    """Draw an enemy with all its parts"""
    pygame.draw.rect(screen, enemy.body_color, enemy.rect)
    head_pos = (enemy.rect.centerx, enemy.rect.top + 10)
    pygame.draw.circle(screen, enemy.head_color, head_pos, 12)

    # Draw accessory
    if enemy.accessory == "Hat":
        points = [(enemy.rect.centerx - 15, enemy.rect.top),
                  (enemy.rect.centerx + 15, enemy.rect.top),
                  (enemy.rect.centerx, enemy.rect.top - 15)]
        pygame.draw.polygon(screen, enemy.accessory_color, points)
    elif enemy.accessory == "Sword":
        pygame.draw.line(screen, enemy.accessory_color,
                         (enemy.rect.right, enemy.rect.centery),
                         (enemy.rect.right + 20, enemy.rect.centery + 10), 3)
    elif enemy.accessory == "Cape":
        points = [(enemy.rect.left, enemy.rect.bottom),
                  (enemy.rect.right, enemy.rect.bottom),
                  (enemy.rect.centerx, enemy.rect.bottom + 20)]
        pygame.draw.polygon(screen, enemy.accessory_color, points)
    elif enemy.accessory == "Glasses":
        pygame.draw.circle(screen, enemy.accessory_color,
                           (enemy.rect.centerx - 5, enemy.rect.top + 10), 3)
        pygame.draw.circle(screen, enemy.accessory_color,
                           (enemy.rect.centerx + 5, enemy.rect.top + 10), 3)

    # Draw enemy name
    name_text = font.render(enemy.name, True, BLACK)
    screen.blit(name_text, (enemy.rect.x - 10, enemy.rect.y - 20))

    # Draw enemy health bar
    health_width = int((enemy.health / enemy.max_health) * 40)
    pygame.draw.rect(screen, RED, (enemy.rect.x, enemy.rect.y + 45, 40, 5))
    pygame.draw.rect(screen, GREEN, (enemy.rect.x, enemy.rect.y + 45, health_width, 5))


def draw_wall(screen, wall):
    """Draw a wall"""
    pygame.draw.rect(screen, wall.color, wall.rect)


def draw_ui(screen, player, font):
    """Draw all UI elements"""
    # Stats
    stats_text = font.render(f"Level: {player.level} EXP: {player.exp}/{player.exp_to_next_level}", True, BLACK)
    screen.blit(stats_text, (10, 10))
    evolution_text = font.render(f"Evolution: {player.evolution}", True, BLACK)
    screen.blit(evolution_text, (10, 35))
    health_text = font.render(f"Health: {player.health}/{player.max_health}", True, BLACK)
    screen.blit(health_text, (10, 60))

    # Player health bar
    pygame.draw.rect(screen, RED, (10, 85, 200, 20))
    health_width = int((player.health / player.max_health) * 200)
    pygame.draw.rect(screen, GREEN, (10, 85, health_width, 20))

    # Instructions
    instructions = font.render("Use WASD or Arrow Keys to move. Click enemies to attack!", True, BLACK)
    screen.blit(instructions, (10, SCREEN_HEIGHT - 30))

def draw_game_over_screen(screen, font, player, pet):
    """Draws the game over screen with all final stats."""
    screen.fill(BLACK)

    # Game Over title
    title_text = font.render("Game Over", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
    screen.blit(title_text, title_rect)

    # Final stats
    y_offset = SCREEN_HEIGHT // 2 - 60
    stats_to_show = [
        f"Final Level: {player.level}",
        f"Final Evolution: {player.evolution}",
        f"EXP: {int(player.exp)}/{int(player.exp_to_next_level)}",
        f"Pet Acquired: {'Yes' if pet else 'No'}"
    ]

    for text_line in stats_to_show:
        stats_text = font.render(text_line, True, WHITE)
        stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(stats_text, stats_rect)
        y_offset += 35

    # Play Again button
    play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, y_offset + 10, 150, 50)
    play_again_text = font.render("Play Again", True, BLACK)
    pygame.draw.rect(screen, WHITE, play_again_button)
    screen.blit(play_again_text, play_again_text.get_rect(center=play_again_button.center))

    return play_again_button

def draw_pet_button(screen, font):
    """Draw the pet purchase button"""
    pygame.draw.rect(screen, CYAN, (700, 500, 100, 50))
    text = font.render("Buy Pet", True, BLACK)
    screen.blit(text, (710, 515))
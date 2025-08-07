import pygame
import random
from game_config import *
from game_math import calculate_health_percentage


class Particle:
    """Explosion particle effect"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Random velocity for scatter effect
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.color = random.choice([RED, ORANGE])
        self.lifetime = PARTICLE_LIFETIME

    def update(self):
        """Move particle and decrease lifetime"""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, screen):
        """Draw particle if still alive"""
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

    def is_alive(self):
        """Check if particle should still be displayed"""
        return self.lifetime > 0


class Pet:
    """Pet that generates passive experience"""

    def __init__(self):
        self.exp_per_second = PET_EXP_PER_SECOND
        self.last_update = pygame.time.get_ticks()
        self.rect = pygame.Rect(700, 450, 30, 30)
        self.color = YELLOW

    def update(self):
        """Update pet and return EXP if a second has passed"""
        now = pygame.time.get_ticks()
        if now - self.last_update >= 1000:  # One second passed
            self.last_update = now
            return self.exp_per_second
        return 0

    def draw(self, screen):
        """Draw the pet character"""
        # Pet body
        pygame.draw.rect(screen, self.color, self.rect)
        # Pet head
        pygame.draw.circle(screen, CYAN, (self.rect.centerx, self.rect.top + 10), 10)


class GameRenderer:
    """Handles all game drawing operations"""

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_background(self):
        """Draw gradient background"""
        for y in range(SCREEN_HEIGHT):
            # Create gradient effect with mathematical color interpolation
            color_intensity = max(0, min(255, int(135 - y * 0.2)))
            color = (
                color_intensity,
                min(255, int(206 - y * 0.1)),
                min(255, int(235 - y * 0.15))
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

    def draw_player(self, player):
        """Draw player with attack range visualization"""
        # Draw attack range aura
        aura_surface = pygame.Surface(
            (PLAYER_ATTACK_RANGE * 2, PLAYER_ATTACK_RANGE * 2),
            pygame.SRCALPHA
        )
        pygame.draw.circle(
            aura_surface,
            (255, 192, 203, 50),  # Semi-transparent pink
            (PLAYER_ATTACK_RANGE, PLAYER_ATTACK_RANGE),
            PLAYER_ATTACK_RANGE
        )
        aura_rect = aura_surface.get_rect(center=player.rect.center)
        self.screen.blit(aura_surface, aura_rect)

        # Draw player body and head
        pygame.draw.rect(self.screen, player.body_color, player.rect)
        head_pos = (player.rect.centerx, player.rect.top + 10)
        pygame.draw.circle(self.screen, player.head_color, head_pos, 15)

    def draw_enemy(self, enemy):
        """Draw enemy with all its parts and health bar"""
        # Draw enemy body
        pygame.draw.rect(self.screen, enemy.body_color, enemy.rect)

        # Draw enemy head
        head_pos = (enemy.rect.centerx, enemy.rect.top + 10)
        pygame.draw.circle(self.screen, enemy.head_color, head_pos, 12)

        # Draw enemy accessory
        self._draw_enemy_accessory(enemy)

        # Draw enemy name
        name_text = self.font.render(enemy.name, True, BLACK)
        self.screen.blit(name_text, (enemy.rect.x - 10, enemy.rect.y - 20))

        # Draw health bar
        self._draw_health_bar(enemy)

    def _draw_enemy_accessory(self, enemy):
        """Draw the enemy's accessory based on type"""
        if enemy.accessory == "Hat":
            points = [
                (enemy.rect.centerx - 15, enemy.rect.top),
                (enemy.rect.centerx + 15, enemy.rect.top),
                (enemy.rect.centerx, enemy.rect.top - 15)
            ]
            pygame.draw.polygon(self.screen, enemy.accessory_color, points)

        elif enemy.accessory == "Sword":
            pygame.draw.line(
                self.screen,
                enemy.accessory_color,
                (enemy.rect.right, enemy.rect.centery),
                (enemy.rect.right + 20, enemy.rect.centery + 10),
                3
            )

        elif enemy.accessory == "Cape":
            points = [
                (enemy.rect.left, enemy.rect.bottom),
                (enemy.rect.right, enemy.rect.bottom),
                (enemy.rect.centerx, enemy.rect.bottom + 20)
            ]
            pygame.draw.polygon(self.screen, enemy.accessory_color, points)

        elif enemy.accessory == "Glasses":
            pygame.draw.circle(
                self.screen,
                enemy.accessory_color,
                (enemy.rect.centerx - 5, enemy.rect.top + 10),
                3
            )
            pygame.draw.circle(
                self.screen,
                enemy.accessory_color,
                (enemy.rect.centerx + 5, enemy.rect.top + 10),
                3
            )

    def _draw_health_bar(self, enemy):
        """Draw enemy health bar"""
        health_percentage = enemy.get_health_percentage()
        health_width = int(health_percentage * 40)

        # Background (red)
        pygame.draw.rect(self.screen, RED, (enemy.rect.x, enemy.rect.y + 45, 40, 5))
        # Foreground (green)
        pygame.draw.rect(self.screen, GREEN, (enemy.rect.x, enemy.rect.y + 45, health_width, 5))

    def draw_wall(self, wall):
        """Draw a wall"""
        pygame.draw.rect(self.screen, wall.color, wall.rect)

    def draw_ui(self, player):
        """Draw all user interface elements"""
        # Player stats
        stats_text = self.font.render(
            f"Level: {player.level} EXP: {player.exp:.1f}/{player.exp_to_next_level:.1f}",
            True, BLACK
        )
        self.screen.blit(stats_text, (10, 10))

        evolution_text = self.font.render(f"Evolution: {player.evolution}", True, BLACK)
        self.screen.blit(evolution_text, (10, 35))

        health_text = self.font.render(
            f"Health: {player.health:.1f}/{player.max_health}",
            True, BLACK
        )
        self.screen.blit(health_text, (10, 60))

        # Player health bar
        self._draw_player_health_bar(player)

        # Instructions
        instructions = self.font.render(
            "Use WASD or Arrow Keys to move. Click enemies to attack!",
            True, BLACK
        )
        self.screen.blit(instructions, (10, SCREEN_HEIGHT - 30))

    def _draw_player_health_bar(self, player):
        """Draw the player's health bar"""
        health_percentage = calculate_health_percentage(player.health, player.max_health)
        health_width = int(health_percentage * 200)

        # Background (red)
        pygame.draw.rect(self.screen, RED, (10, 85, 200, 20))
        # Foreground (green)
        pygame.draw.rect(self.screen, GREEN, (10, 85, health_width, 20))

    def draw_pet_button(self):
        """Draw the pet purchase button"""
        pygame.draw.rect(self.screen, CYAN, (700, 500, 100, 50))
        text = self.font.render("Buy Pet", True, BLACK)
        self.screen.blit(text, (710, 515))

    def draw_game_over_screen(self, player, pet):
        """Draw the game over screen with final stats"""
        self.screen.fill(BLACK)

        # Game Over title
        title_text = self.font.render("Game Over", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title_text, title_rect)

        # Final stats
        y_offset = SCREEN_HEIGHT // 2 - 60
        stats_to_show = [
            f"Final Level: {player.level}",
            f"Final Evolution: {player.evolution}",
            f"EXP: {int(player.exp)}/{int(player.exp_to_next_level)}",
            f"Pet Acquired: {'Yes' if pet else 'No'}"
        ]

        for text_line in stats_to_show:
            stats_text = self.font.render(text_line, True, WHITE)
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(stats_text, stats_rect)
            y_offset += 35

        # Play Again button
        play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, y_offset + 10, 150, 50)
        play_again_text = self.font.render("Play Again", True, BLACK)
        pygame.draw.rect(self.screen, WHITE, play_again_button)
        self.screen.blit(play_again_text, play_again_text.get_rect(center=play_again_button.center))

        return play_again_button
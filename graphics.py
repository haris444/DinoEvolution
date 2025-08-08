import pygame
import random
from game_config import *
from game_math import calculate_health_percentage
from pets import get_pet_info, get_pet_cost


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


class GameRenderer:
    """Handles all game drawing operations"""

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_background(self):
        """Draw gradient background with UI panel"""
        # Draw UI panel background (dark gray)
        ui_panel_rect = pygame.Rect(0, 0, UI_PANEL_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, DARK_GRAY, ui_panel_rect)

        # Draw separator line
        pygame.draw.line(self.screen, WHITE, (UI_PANEL_WIDTH, 0), (UI_PANEL_WIDTH, SCREEN_HEIGHT), 2)

        # Draw gradient background for gameplay area
        for y in range(SCREEN_HEIGHT):
            # Create gradient effect with mathematical color interpolation
            color_intensity = max(0, min(255, int(135 - y * 0.2)))
            color = (
                color_intensity,
                min(255, int(206 - y * 0.1)),
                min(255, int(235 - y * 0.15))
            )
            pygame.draw.line(self.screen, color, (UI_PANEL_WIDTH, y), (SCREEN_WIDTH, y))

    def draw_player(self, player):
        """Draw player with attack range visualization (now pet-boosted)"""
        # Draw attack range aura (using pet-boosted range)
        aura_surface = pygame.Surface(
            (player.attack_range * 2, player.attack_range * 2),
            pygame.SRCALPHA
        )
        pygame.draw.circle(
            aura_surface,
            (255, 192, 203, 50),  # Semi-transparent pink
            (player.attack_range, player.attack_range),
            player.attack_range
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
        head_radius = 20 if enemy.is_boss else 12
        pygame.draw.circle(self.screen, enemy.head_color, head_pos, head_radius)

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

    def draw_golden_apple(self, apple):
        """Draw a golden apple collectible"""
        # Draw apple body (golden circle)
        pygame.draw.circle(self.screen, apple.color, apple.rect.center, apple.rect.width // 2)

        # Draw apple outline for better visibility
        pygame.draw.circle(self.screen, apple.outline_color, apple.rect.center, apple.rect.width // 2, 2)

        # Draw apple stem (small brown line on top)
        stem_start = (apple.rect.centerx, apple.rect.top + 5)
        stem_end = (apple.rect.centerx, apple.rect.top)
        pygame.draw.line(self.screen, BROWN, stem_start, stem_end, 2)

        # Draw apple leaf (small green triangle)
        leaf_points = [
            (apple.rect.centerx + 3, apple.rect.top + 2),
            (apple.rect.centerx + 8, apple.rect.top - 2),
            (apple.rect.centerx + 5, apple.rect.top + 5)
        ]
        pygame.draw.polygon(self.screen, GREEN, leaf_points)

        # Draw EXP value text above apple
        exp_text = self.font.render(f"+{apple.exp_value} EXP", True, BLACK)
        text_rect = exp_text.get_rect(center=(apple.rect.centerx, apple.rect.top - 15))
        self.screen.blit(exp_text, text_rect)

    def _draw_health_bar(self, enemy):
        """Draw enemy health bar"""
        health_percentage = enemy.get_health_percentage()
        health_width = int(health_percentage * enemy.rect.width)

        # Background (red)
        pygame.draw.rect(self.screen, RED, (enemy.rect.x, enemy.rect.y + enemy.rect.height + 5, enemy.rect.width, 5))
        # Foreground (green)
        pygame.draw.rect(self.screen, GREEN, (enemy.rect.x, enemy.rect.y + enemy.rect.height + 5, health_width, 5))

    def draw_wall(self, wall):
        """Draw a wall"""
        pygame.draw.rect(self.screen, wall.color, wall.rect)

    def draw_ui(self, player):
        """Draw all user interface elements in the left UI panel"""
        # UI Panel title
        title_text = self.font.render("PLAYER STATS", True, WHITE)
        self.screen.blit(title_text, (10, 10))

        # Player basic stats
        level_exp_text = self.font.render(
            f"Level: {player.level}", True, WHITE
        )
        self.screen.blit(level_exp_text, (10, 40))

        exp_text = self.font.render(
            f"EXP: {player.exp:.1f}/{player.exp_to_next_level:.1f}", True, WHITE
        )
        self.screen.blit(exp_text, (10, 60))

        wins_text = self.font.render(f"Wins: {player.wins}", True, WHITE)
        self.screen.blit(wins_text, (10, 80))

        evolution_text = self.font.render(f"Evolution:", True, WHITE)
        self.screen.blit(evolution_text, (10, 110))

        evo_name_text = self.font.render(f"{player.evolution}", True, YELLOW)
        self.screen.blit(evo_name_text, (10, 130))

        # Show specialty
        specialty_text = self.font.render(f"Specialty:", True, WHITE)
        self.screen.blit(specialty_text, (10, 160))

        # Split specialty text if too long
        specialty_words = player.specialty.split()
        if len(player.specialty) > 25:  # If too long, split into two lines
            line1 = " ".join(specialty_words[:3])
            line2 = " ".join(specialty_words[3:])
            spec1_text = self.font.render(line1, True, CYAN)
            spec2_text = self.font.render(line2, True, CYAN)
            self.screen.blit(spec1_text, (10, 180))
            self.screen.blit(spec2_text, (10, 200))
            y_offset = 220
        else:
            spec_text = self.font.render(player.specialty, True, CYAN)
            self.screen.blit(spec_text, (10, 180))
            y_offset = 210

        # Combat stats
        damage_text = self.font.render(f"Damage: {player.damage}", True, WHITE)
        self.screen.blit(damage_text, (10, y_offset))

        speed_text = self.font.render(f"Speed: {player.speed}", True, WHITE)
        self.screen.blit(speed_text, (10, y_offset + 20))

        range_text = self.font.render(f"Range: {player.attack_range}", True, WHITE)
        self.screen.blit(range_text, (10, y_offset + 40))

        # Health stats
        health_text = self.font.render(f"Health: {player.health:.0f}/{player.max_health}", True, WHITE)
        self.screen.blit(health_text, (10, y_offset + 70))

        regen_text = self.font.render(f"Regen: {player.regen_rate:.2f}/sec", True, WHITE)
        self.screen.blit(regen_text, (10, y_offset + 90))

        # Player health bar
        self._draw_player_health_bar(player, y_offset + 110)

        # Show active pets
        pets_title = self.font.render("Active Pets:", True, WHITE)
        self.screen.blit(pets_title, (10, y_offset + 140))

        for i in range(3):
            pet_y = y_offset + 160 + (i * 20)
            if (i < len(player.pet_objects) and
                    player.pet_objects[i] is not None):
                pet_name = player.pet_objects[i].name
                # Truncate pet name if too long
                if len(pet_name) > 18:
                    pet_name = pet_name[:15] + "..."
                pet_text = f"[{i + 1}]: {pet_name}"
                color = GREEN
            else:
                pet_text = f"[{i + 1}]: Empty"
                color = GRAY

            pets_display = self.font.render(pet_text, True, color)
            self.screen.blit(pets_display, (10, pet_y))

        # Instructions at bottom of UI panel
        instructions1 = self.font.render("CONTROLS:", True, WHITE)
        self.screen.blit(instructions1, (10, SCREEN_HEIGHT - 120))

        instructions2 = self.font.render("WASD/Arrows: Move", True, WHITE)
        self.screen.blit(instructions2, (10, SCREEN_HEIGHT - 100))

        instructions3 = self.font.render("Click: Attack", True, WHITE)
        self.screen.blit(instructions3, (10, SCREEN_HEIGHT - 80))

        instructions4 = self.font.render("P: Pet Shop", True, WHITE)
        self.screen.blit(instructions4, (10, SCREEN_HEIGHT - 60))

        instructions5 = self.font.render("T: Pet Team", True, WHITE)
        self.screen.blit(instructions5, (10, SCREEN_HEIGHT - 40))

        instructions6 = self.font.render("Kill enemies for wins!", True, YELLOW)
        self.screen.blit(instructions6, (10, SCREEN_HEIGHT - 20))

    def _draw_player_health_bar(self, player, y_pos):
        """Draw the player's health bar in the UI panel"""
        health_percentage = calculate_health_percentage(player.health, player.max_health)
        health_width = int(health_percentage * 280)  # Scale to fit UI panel (280px wide)

        # Background (red)
        pygame.draw.rect(self.screen, RED, (10, y_pos, 280, 20))
        # Foreground (green)
        pygame.draw.rect(self.screen, GREEN, (10, y_pos, health_width, 20))
        # Border
        pygame.draw.rect(self.screen, WHITE, (10, y_pos, 280, 20), 2)

    def draw_pet_shop(self, player, selected_pet_info, confirm_purchase):
        """Draw the pet shop interface"""
        self.screen.fill(BLACK)

        # Title
        title = self.font.render("PET SHOP", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Show wins
        wins_text = self.font.render(f"Wins: {player.wins}", True, WHITE)
        self.screen.blit(wins_text, (50, 70))

        # Show available pets
        available_pets = player.get_available_pets()
        y_start = 100

        for i, pet_name in enumerate(available_pets):
            y = y_start + i * 60
            pet_info = get_pet_info(pet_name)
            cost = get_pet_cost(pet_name)

            # Pet background
            pet_rect = pygame.Rect(50, y, 500, 50)
            if pet_name in player.owned_pets:
                pygame.draw.rect(self.screen, (0, 100, 0), pet_rect)  # Green for owned
                status = "OWNED"
            elif player.can_buy_pet(pet_name):
                pygame.draw.rect(self.screen, (0, 0, 100), pet_rect)  # Blue for buyable
                status = f"Cost: {cost} wins"
            else:
                pygame.draw.rect(self.screen, (100, 0, 0), pet_rect)  # Red for can't buy
                status = f"Need {cost} wins"

            pygame.draw.rect(self.screen, WHITE, pet_rect, 2)  # White border

            # Pet info text
            name_text = self.font.render(pet_name, True, WHITE)
            desc_text = self.font.render(pet_info["description"], True, WHITE)
            status_text = self.font.render(status, True, WHITE)

            self.screen.blit(name_text, (60, y + 5))
            self.screen.blit(desc_text, (60, y + 20))
            self.screen.blit(status_text, (60, y + 35))

            # Pet color indicator
            color_rect = pygame.Rect(520, y + 10, 20, 30)
            pygame.draw.rect(self.screen, pet_info["color"], color_rect)

        # Purchase confirmation dialog
        if confirm_purchase and selected_pet_info:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            # Confirmation box
            dialog_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 180)
            pygame.draw.rect(self.screen, GRAY, dialog_rect)
            pygame.draw.rect(self.screen, WHITE, dialog_rect, 3)

            # Confirmation text
            pet_info = get_pet_info(selected_pet_info)
            cost = get_pet_cost(selected_pet_info)

            confirm_text = [
                f"Buy {selected_pet_info}?",
                pet_info["description"],
                f"Cost: {cost} wins",
                f"You have: {player.wins} wins"
            ]

            for i, text in enumerate(confirm_text):
                rendered = self.font.render(text, True, BLACK)
                text_rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, 330 + i * 25))
                self.screen.blit(rendered, text_rect)

            # Buttons - positioned below the text
            confirm_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 430, 80, 40)
            cancel_rect = pygame.Rect(SCREEN_WIDTH // 2 + 20, 430, 80, 40)

            pygame.draw.rect(self.screen, GREEN, confirm_rect)
            pygame.draw.rect(self.screen, RED, cancel_rect)

            confirm_btn_text = self.font.render("BUY", True, WHITE)
            cancel_btn_text = self.font.render("CANCEL", True, WHITE)

            self.screen.blit(confirm_btn_text, confirm_btn_text.get_rect(center=confirm_rect.center))
            self.screen.blit(cancel_btn_text, cancel_btn_text.get_rect(center=cancel_rect.center))

        # Instructions
        instructions = self.font.render("Click on pets to buy them! Press ESC to close.", True, WHITE)
        self.screen.blit(instructions, (50, SCREEN_HEIGHT - 50))

    def draw_pet_selection(self, player):
        """Draw the pet selection interface"""
        self.screen.fill(BLACK)

        # Title
        title = self.font.render("PET TEAM SELECTION", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Show owned pets
        owned_text = self.font.render("Your Pets:", True, WHITE)
        self.screen.blit(owned_text, (50, 80))

        y_start = 100
        for i, pet_name in enumerate(player.owned_pets):
            y = y_start + i * 40
            pet_info = get_pet_info(pet_name)

            # Pet background
            pet_rect = pygame.Rect(50, y, 400, 35)
            pygame.draw.rect(self.screen, (50, 50, 50), pet_rect)
            pygame.draw.rect(self.screen, WHITE, pet_rect, 2)

            # Pet info
            name_text = self.font.render(f"{pet_name}: {pet_info['description']}", True, WHITE)
            self.screen.blit(name_text, (60, y + 8))

            # Color indicator
            color_rect = pygame.Rect(420, y + 5, 25, 25)
            pygame.draw.rect(self.screen, pet_info["color"], color_rect)

        # Show active slots
        slots_text = self.font.render("Active Pet Slots (click to remove):", True, WHITE)
        self.screen.blit(slots_text, (50, 280))

        for slot in range(3):
            x = 50 + slot * 180
            y = 300
            slot_rect = pygame.Rect(x, y, 160, 200)

            # Slot background
            pygame.draw.rect(self.screen, (30, 30, 30), slot_rect)
            pygame.draw.rect(self.screen, WHITE, slot_rect, 2)

            # Slot title
            slot_title = self.font.render(f"Slot {slot + 1}", True, WHITE)
            self.screen.blit(slot_title, (x + 10, y + 10))

            # Pet in slot
            if (slot < len(player.pet_objects) and
                    player.pet_objects[slot] is not None):
                pet = player.pet_objects[slot]
                pet_info = get_pet_info(pet.name)

                # Pet visual representation
                pet_visual_rect = pygame.Rect(x + 30, y + 40, 100, 100)
                pygame.draw.rect(self.screen, pet_info["color"], pet_visual_rect)

                # Pet name and description
                name = self.font.render(pet.name, True, WHITE)
                desc_lines = pet_info["description"].split()

                # Wrap text to fit in slot
                line1 = " ".join(desc_lines[:2]) if len(desc_lines) >= 2 else pet_info["description"]
                line2 = " ".join(desc_lines[2:]) if len(desc_lines) > 2 else ""

                name_rect = name.get_rect(center=(x + 80, y + 155))
                self.screen.blit(name, name_rect)

                desc1 = self.font.render(line1, True, WHITE)
                desc1_rect = desc1.get_rect(center=(x + 80, y + 170))
                self.screen.blit(desc1, desc1_rect)

                if line2:
                    desc2 = self.font.render(line2, True, WHITE)
                    desc2_rect = desc2.get_rect(center=(x + 80, y + 185))
                    self.screen.blit(desc2, desc2_rect)
            else:
                # Empty slot
                empty_text = self.font.render("EMPTY", True, GRAY)
                empty_rect = empty_text.get_rect(center=(x + 80, y + 100))
                self.screen.blit(empty_text, empty_rect)

        # Instructions
        instructions1 = self.font.render("Click your pets above to add them to slots.", True, WHITE)
        instructions2 = self.font.render("Click active slots to remove pets. Press ESC to close.", True, WHITE)
        self.screen.blit(instructions1, (50, SCREEN_HEIGHT - 70))
        self.screen.blit(instructions2, (50, SCREEN_HEIGHT - 50))

    def draw_game_over_screen(self, player):
        """Draw the game over screen with final stats"""
        self.screen.fill(BLACK)

        # Game Over title
        title_text = self.font.render("Game Over", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title_text, title_rect)

        # Final stats - updated to show wins and pets
        y_offset = SCREEN_HEIGHT // 2 - 60
        stats_to_show = [
            f"Final Level: {player.level}",
            f"Final Evolution: {player.evolution}",
            f"Total Wins: {player.wins}",
            f"Final Damage: {player.damage}",
            f"Final Health: {player.max_health}",
            f"EXP: {int(player.exp)}/{int(player.exp_to_next_level)}",
            f"Pets Owned: {len(player.owned_pets)}"
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
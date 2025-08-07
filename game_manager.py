import pygame
from game_config import *
from game_math import calculate_spawn_time_for_level, calculate_distance
from player import Player
from enemies import Enemy
from walls import create_walls
from graphics import Particle, Pet, GameRenderer


class GameManager:
    """Manages the overall game state and coordinates all game systems"""

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.renderer = GameRenderer(screen, font)
        self.game_state = "playing"

        # Initialize game objects
        self.reset_game()

    def reset_game(self):
        """Reset all game objects to starting state"""
        self.player = Player()
        self.enemies = []
        self.particles = []
        self.pet = None
        self.walls = create_walls()
        self.enemy_spawn_timer = 0
        self.game_state = "playing"

    def handle_input(self, event):
        """Handle mouse clicks and other input events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.game_state == "playing":
                self._handle_playing_input(mouse_pos)
            elif self.game_state == "game_over":
                return self._handle_game_over_input(mouse_pos)

        return False

    def _handle_playing_input(self, mouse_pos):
        """Handle input during gameplay"""
        # Check if clicked on enemy
        self._handle_enemy_attacks(mouse_pos)

        # Check if clicked on pet button
        self._handle_pet_purchase(mouse_pos)

    def _handle_enemy_attacks(self, mouse_pos):
        """Check if player clicked on an enemy within attack range"""
        for enemy in self.enemies[:]:
            if enemy.rect.collidepoint(mouse_pos):
                # Calculate distance to enemy
                player_center = (self.player.rect.centerx, self.player.rect.centery)
                enemy_center = (enemy.rect.centerx, enemy.rect.centery)
                distance = calculate_distance(player_center, enemy_center)

                # Check if enemy is within attack range
                if distance <= PLAYER_ATTACK_RANGE + enemy.rect.width / 2:
                    # Deal damage using player's current damage stat
                    damage_dealt = self.player.damage
                    if enemy.take_damage(damage_dealt):
                        # Enemy died - give EXP and create explosion
                        self.player.gain_experience(EXP_PER_ENEMY_KILL)
                        self.enemies.remove(enemy)
                        self._create_explosion_particles(enemy.rect.centerx, enemy.rect.centery)
                        print(f"Defeated {enemy.name} with {damage_dealt} damage!")
                    else:
                        print(f"Hit {enemy.name} for {damage_dealt} damage! Enemy health: {enemy.health}")
                else:
                    print("Enemy too far away!")
                break

    def _handle_pet_purchase(self, mouse_pos):
        """Handle pet purchase button clicks"""
        pet_button_rect = pygame.Rect(700, 500, 100, 50)
        if (self.player.can_buy_pet() and
                self.pet is None and
                pet_button_rect.collidepoint(mouse_pos)):
            self.pet = Pet()
            print("Bought a pet!")

    def _handle_game_over_input(self, mouse_pos):
        """Handle input on game over screen"""
        # Use the same button position as in the draw function
        y_offset = SCREEN_HEIGHT // 2 - 60 + (5 * 35)  # After 5 stats lines
        play_again_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 75,
            y_offset + 10,
            150, 50
        )
        if play_again_button.collidepoint(mouse_pos):
            self.reset_game()
            return True
        return False

    def _create_explosion_particles(self, x, y):
        """Create particle explosion effect at given position"""
        for _ in range(PARTICLES_PER_EXPLOSION):
            self.particles.append(Particle(x, y))

    def update_game(self, keys):
        """Update all game objects for one frame"""
        if self.game_state == "playing":
            self._update_playing_state(keys)
        # Game over state doesn't need updates

    def _update_playing_state(self, keys):
        """Update game during playing state"""
        # Check for game over
        if not self.player.is_alive():
            self.game_state = "game_over"
            return

        # Update player
        self.player.handle_movement(keys, self.walls)
        self.player.heal_over_time()

        # Spawn new enemies
        self._update_enemy_spawning()

        # Update all enemies
        self._update_enemies()

        # Update pet
        self._update_pet()

        # Update visual effects
        self._update_particles()

    def _update_enemy_spawning(self):
        """Handle enemy spawning based on level"""
        self.enemy_spawn_timer += 1
        spawn_time = calculate_spawn_time_for_level(self.player.level)

        if self.enemy_spawn_timer >= spawn_time:
            self.enemies.append(Enemy(self.walls, self.player.level))
            self.enemy_spawn_timer = 0

    def _update_enemies(self):
        """Update all enemies"""
        for enemy in self.enemies:
            # Move enemy towards player
            enemy.update_movement(self.player, self.walls)

            # Check if enemy can attack player
            if enemy.can_attack_player(self.player):
                enemy.attempt_attack(self.player)

    def _update_pet(self):
        """Update pet and handle EXP generation"""
        if self.pet:
            exp_from_pet = self.pet.update()
            if exp_from_pet > 0:
                self.player.gain_experience(exp_from_pet)

    def _update_particles(self):
        """Update visual effect particles"""
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw_game(self):
        """Draw the entire game"""
        if self.game_state == "playing":
            self._draw_playing_state()
        elif self.game_state == "game_over":
            return self._draw_game_over_state()
        return None

    def _draw_playing_state(self):
        """Draw everything during gameplay"""
        # Draw background
        self.renderer.draw_background()

        # Draw walls
        for wall in self.walls:
            self.renderer.draw_wall(wall)

        # Draw player
        self.renderer.draw_player(self.player)

        # Draw enemies
        for enemy in self.enemies:
            self.renderer.draw_enemy(enemy)

        # Draw pet purchase button if available
        if self.player.can_buy_pet() and self.pet is None:
            self.renderer.draw_pet_button()

        # Draw pet if owned
        if self.pet:
            self.pet.draw(self.screen)

        # Draw visual effects
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw UI
        self.renderer.draw_ui(self.player)

    def _draw_game_over_state(self):
        """Draw game over screen"""
        return self.renderer.draw_game_over_screen(self.player, self.pet)
import pygame
from game_config import *
from game_math import calculate_spawn_time_for_level, calculate_distance
from player import Player
from golden_apple import GoldenApple
from walls import create_walls
from graphics import Particle, GameRenderer


class GameManager:
    """Manages the overall game state and coordinates all game systems"""

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.renderer = GameRenderer(screen, font)
        self.game_state = "playing"  # "playing", "game_over", "pet_shop", "pet_selection"

        # Pet shop state variables
        self.selected_pet_info = None  # Currently viewing pet info
        self.confirm_purchase = False  # Whether showing purchase confirmation

        # Initialize game objects
        self.reset_game()

    def reset_game(self):
        """Reset all game objects to starting state"""
        self.player = Player()
        self.enemies = []
        self.golden_apples = []
        self.particles = []
        self.walls = create_walls()
        self.enemy_spawn_timer = 0
        self.enemies_spawned_since_last_boss = 0
        self.apple_spawn_timer = 0
        self.game_state = "playing"
        self.selected_pet_info = None
        self.confirm_purchase = False

    def handle_input(self, event):
        """Handle mouse clicks and other input events"""
        if event.type == pygame.KEYDOWN:
            # Pet shop hotkey
            if event.key == pygame.K_p and self.game_state == "playing":
                self.game_state = "pet_shop"
                return False
            # Pet selection hotkey
            elif event.key == pygame.K_t and self.game_state == "playing":
                self.game_state = "pet_selection"
                return False
            # Close menus with ESC
            elif event.key == pygame.K_ESCAPE:
                if self.game_state in ["pet_shop", "pet_selection"]:
                    self.game_state = "playing"
                    self.selected_pet_info = None
                    self.confirm_purchase = False
                return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.game_state == "playing":
                self._handle_playing_input(mouse_pos)
            elif self.game_state == "game_over":
                return self._handle_game_over_input(mouse_pos)
            elif self.game_state == "pet_shop":
                self._handle_pet_shop_input(mouse_pos)
            elif self.game_state == "pet_selection":
                self._handle_pet_selection_input(mouse_pos)

        return False

    def _handle_playing_input(self, mouse_pos):
        """Handle input during gameplay"""
        # Check if clicked on enemy
        self._handle_enemy_attacks(mouse_pos)

        # Check if clicked on golden apple
        self._handle_apple_collection(mouse_pos)

    def _handle_pet_shop_input(self, mouse_pos):
        """Handle input in the pet shop"""
        from pets import get_pet_info, get_pet_cost

        if self.confirm_purchase and self.selected_pet_info:
            # Handle purchase confirmation - fixed button positions
            confirm_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 430, 80, 40)
            cancel_rect = pygame.Rect(SCREEN_WIDTH // 2 + 20, 430, 80, 40)

            if confirm_rect.collidepoint(mouse_pos):
                # Buy the pet
                if self.player.buy_pet(self.selected_pet_info):
                    print(f"Successfully bought {self.selected_pet_info}!")
                self.confirm_purchase = False
                self.selected_pet_info = None
            elif cancel_rect.collidepoint(mouse_pos):
                # Cancel purchase
                self.confirm_purchase = False
                self.selected_pet_info = None
        else:
            # Handle pet clicking
            available_pets = self.player.get_available_pets()
            y_start = 100

            for i, pet_name in enumerate(available_pets):
                pet_rect = pygame.Rect(50, y_start + i * 60, 500, 50)
                if pet_rect.collidepoint(mouse_pos):
                    if pet_name in self.player.owned_pets:
                        print(f"{pet_name} already owned!")
                    elif self.player.can_buy_pet(pet_name):
                        # Show purchase confirmation
                        self.selected_pet_info = pet_name
                        self.confirm_purchase = True
                    else:
                        cost = get_pet_cost(pet_name)
                        print(f"Need {cost} wins to buy {pet_name} (you have {self.player.wins})")
                    break

    def _handle_pet_selection_input(self, mouse_pos):
        """Handle input in the pet selection menu"""
        # Handle slot clicks (where to put pets)
        for slot in range(3):
            slot_rect = pygame.Rect(50 + slot * 180, 300, 160, 200)
            if slot_rect.collidepoint(mouse_pos):
                # Show owned pets for this slot selection
                self._show_pets_for_slot(slot, mouse_pos)
                break

        # Handle owned pet clicks
        y_start = 100
        for i, pet_name in enumerate(self.player.owned_pets):
            pet_rect = pygame.Rect(50, y_start + i * 40, 400, 35)
            if pet_rect.collidepoint(mouse_pos):
                # Find an empty slot or ask which slot to replace
                for slot in range(3):
                    if (slot < len(self.player.pet_objects) and
                            self.player.pet_objects[slot] is None):
                        self.player.set_active_pet(slot, pet_name)
                        print(f"Added {pet_name} to slot {slot + 1}")
                        return
                print(f"All slots full! Click on a slot to replace a pet.")
                break

    def _show_pets_for_slot(self, slot, mouse_pos):
        """Handle clicking on a specific pet slot"""
        # Safety check for valid slot index
        if 0 <= slot < len(self.player.pet_objects):
            # Remove pet from slot
            self.player.set_active_pet(slot, None)
            print(f"Removed pet from slot {slot + 1}")

    def _handle_enemy_attacks(self, mouse_pos):
        """Check if player clicked on an enemy within attack range"""
        for enemy in self.enemies[:]:
            if enemy.rect.collidepoint(mouse_pos):
                # Calculate distance to enemy
                player_center = (self.player.rect.centerx, self.player.rect.centery)
                enemy_center = (enemy.rect.centerx, enemy.rect.centery)
                distance = calculate_distance(player_center, enemy_center)

                # Check if enemy is within attack range (now pet-boosted)
                if distance <= self.player.attack_range + enemy.rect.width / 2:
                    # Deal damage using player's current damage stat (now pet-boosted)
                    damage_dealt = self.player.damage
                    if enemy.take_damage(damage_dealt):
                        # Enemy died - give EXP, WINS, and create explosion
                        self.player.gain_experience(EXP_PER_ENEMY_KILL)
                        self.player.add_win()  # Add win for pet purchasing!
                        self.enemies.remove(enemy)
                        self._create_explosion_particles(enemy.rect.centerx, enemy.rect.centery)
                        print(f"Defeated {enemy.name} with {damage_dealt} damage!")
                    else:
                        print(f"Hit {enemy.name} for {damage_dealt} damage! Enemy health: {enemy.health}")
                else:
                    print("Enemy too far away!")
                break

    def _handle_apple_collection(self, mouse_pos):
        """Check if player clicked on a golden apple within attack range"""
        for apple in self.golden_apples[:]:
            if apple.is_clicked_by_player(mouse_pos, self.player):
                # Use pet-boosted attack range
                exp_gained = apple.get_exp_value()
                self.player.gain_experience(exp_gained)
                self.golden_apples.remove(apple)
                self._create_explosion_particles(apple.rect.centerx, apple.rect.centery)
                print(f"Collected {apple.name} for {exp_gained} EXP!")
                break

    def _handle_game_over_input(self, mouse_pos):
        """Handle input on game over screen"""
        # Use the same button position as in the draw function
        y_offset = SCREEN_HEIGHT // 2 - 60 + (7 * 35)  # After 7 stats lines (added wins)
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
        # Other states don't need updates (they're paused)

    def _update_playing_state(self, keys):
        """Update game during playing state"""
        # Check for game over
        if not self.player.is_alive():
            self.game_state = "game_over"
            return

        # Update player
        self.player.handle_movement(keys, self.walls)
        self.player.heal_over_time()  # Now uses pet-boosted regen
        self.player.update_pets()  # Update pet positions

        # Spawn new enemies
        self._update_enemy_spawning()

        # Spawn new golden apples
        self._update_apple_spawning()

        # Update all enemies
        self._update_enemies()

        # Update visual effects
        self._update_particles()

    def _update_enemy_spawning(self):
        """Handle enemy spawning based on level"""
        self.enemy_spawn_timer += 1
        spawn_time = calculate_spawn_time_for_level(self.player.level)

        if self.enemy_spawn_timer >= spawn_time:
            if self.enemies_spawned_since_last_boss >= BOSS_SPAWN_INTERVAL:
                self.enemies.append(Boss(self.walls, self.player.level))
                self.enemies_spawned_since_last_boss = 0
            else:
                self.enemies.append(Enemy(self.walls, self.player.level))
                self.enemies_spawned_since_last_boss += 1
            self.enemy_spawn_timer = 0

    def _update_apple_spawning(self):
        """Handle golden apple spawning"""
        self.apple_spawn_timer += 1

        if self.apple_spawn_timer >= GOLDEN_APPLE_SPAWN_TIME:
            self.golden_apples.append(GoldenApple())
            self.apple_spawn_timer = 0

    def _update_enemies(self):
        """Update all enemies"""
        for enemy in self.enemies:
            # Move enemy towards player
            enemy.update_movement(self.player, self.walls)

            # Check if enemy can attack player
            if enemy.can_attack_player(self.player):
                enemy.attempt_attack(self.player)

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
        elif self.game_state == "pet_shop":
            self._draw_pet_shop()
        elif self.game_state == "pet_selection":
            self._draw_pet_selection()
        return None

    def _draw_playing_state(self):
        """Draw everything during gameplay"""
        # Draw background
        self.renderer.draw_background()

        # Draw walls
        for wall in self.walls:
            self.renderer.draw_wall(wall)

        # Draw player (with pet-boosted attack range)
        self.renderer.draw_player(self.player)

        # Draw enemies
        for enemy in self.enemies:
            self.renderer.draw_enemy(enemy)

        # Draw golden apples
        for apple in self.golden_apples:
            self.renderer.draw_golden_apple(apple)

        # Draw pets
        for i in range(3):
            if (i < len(self.player.pet_objects) and
                    self.player.pet_objects[i] is not None):
                self.player.pet_objects[i].draw(self.screen)

        # Draw visual effects
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw UI (now includes wins and pet info)
        self.renderer.draw_ui(self.player)

    def _draw_pet_shop(self):
        """Draw the pet shop interface"""
        self.renderer.draw_pet_shop(self.player, self.selected_pet_info, self.confirm_purchase)

    def _draw_pet_selection(self):
        """Draw the pet selection interface"""
        self.renderer.draw_pet_selection(self.player)

    def _draw_game_over_state(self):
        """Draw game over screen"""
        return self.renderer.draw_game_over_screen(self.player)
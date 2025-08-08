import pygame
import time
from game_config import *
from game_math import calculate_experience_needed, clamp_value
from evolutions import get_evolution_data
from pets import Pet, get_available_pets_for_level


class Player:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = START_EXP_TO_LEVEL
        self.wins = 0  # Track enemy kills for buying pets

        # Shield system
        self._shield_end_time = 0.0  # time.monotonic() when shield ends

        # Pet system
        self.owned_pets = []  # List of pet names the player owns
        self.active_pets = [None, None, None]  # 3 slots for active pets (Pet objects)
        self.pet_objects = [None, None, None]  # Currently active Pet objects (3 slots)

        # Set initial evolution and stats
        self._update_evolution_and_stats()

        # Position and size - 40x40 collision box (head is visual only)
        self.rect = pygame.Rect(40, 40, 40, 40)

    def _update_evolution_and_stats(self):
        """Update player appearance AND stats based on current level"""
        evolution_data = get_evolution_data(self.level)

        # Update appearance
        self.evolution = evolution_data["name"]
        self.body_color = evolution_data["body_color"]
        self.head_color = evolution_data["head_color"]
        self.specialty = evolution_data["specialty"]

        # Update base stats from evolution data
        stats = evolution_data["stats"]

        self.base_max_health = stats["health"]
        self.base_speed = stats["speed"]
        self.base_damage = stats["damage"]

        # Apply pet boosts to get final stats
        self._calculate_final_stats()

        # Handle health on level up
        if hasattr(self, 'health'):
            # Heal 50% of max health on level up + keep current health
            self.health = min(self.max_health, self.health + (self.max_health * 0.5))
        else:
            # First time initialization
            self.health = self.max_health

    def _calculate_final_stats(self):
        """Calculate final stats by applying pet boosts to base stats"""
        # Tally up percentage boosts from all active pets
        health_boost = 0
        speed_boost = 0
        damage_boost = 0
        aura_boost = 0
        regen_boost = 0

        for pet in self.pet_objects:
            if pet is None:
                continue

            boost_type = pet.get_boost_type()
            boost_amount = pet.get_boost_amount()

            if boost_type == "health":
                health_boost += boost_amount
            elif boost_type == "speed":
                speed_boost += boost_amount
            elif boost_type == "damage":
                damage_boost += boost_amount
            elif boost_type == "aura":
                aura_boost += boost_amount
            elif boost_type == "regeneration":
                regen_boost += boost_amount

        # Apply tallied boosts to base stats
        self.max_health = self.base_max_health * (1 + health_boost)
        self.speed = self.base_speed * (1 + speed_boost)
        self.damage = self.base_damage * (1 + damage_boost)
        self.attack_range = PLAYER_ATTACK_RANGE * (1 + aura_boost)
        self.regen_rate = (self.base_max_health / 1000) * (1 + regen_boost)

    def add_win(self):
        """Increase win counter when player kills an enemy"""
        self.wins += 1
        print(f"Win! Total wins: {self.wins}")

    def buy_pet(self, pet_name):
        """Buy a pet if player has enough wins"""
        from pets import get_pet_cost
        cost = get_pet_cost(pet_name)

        if self.wins >= cost and pet_name not in self.owned_pets:
            self.wins -= cost
            self.owned_pets.append(pet_name)
            print(f"Bought {pet_name} for {cost} wins!")
            return True
        return False

    def set_active_pet(self, slot_index, pet_name):
        """Set a pet to be active in the given slot (0, 1, or 2)"""
        if not (0 <= slot_index < 3):
            print(f"Invalid slot index: {slot_index}")
            return

        if pet_name in self.owned_pets or pet_name is None:
            # Remove old pet from that slot
            if slot_index < len(self.pet_objects) and self.pet_objects[slot_index] is not None:
                self.pet_objects[slot_index] = None

            # Add new pet if not None
            if pet_name is not None:
                new_pet = Pet(pet_name, slot_index)
                self.pet_objects[slot_index] = new_pet
            else:
                self.pet_objects[slot_index] = None

            # Recalculate stats with new pets
            self._calculate_final_stats()

            # Ensure health doesn't exceed new max
            if hasattr(self, 'health') and self.health > self.max_health:
                self.health = self.max_health

    def update_pets(self):
        """Update all active pets"""
        player_center = (self.rect.centerx, self.rect.centery)
        for i in range(3):
            if (i < len(self.pet_objects) and
                    self.pet_objects[i] is not None):
                self.pet_objects[i].update(player_center)

    def get_available_pets(self):
        """Get list of pets available for purchase at current level"""
        return get_available_pets_for_level(self.level)

    def can_buy_pet(self, pet_name):
        """Check if player can buy a specific pet"""
        from pets import get_pet_cost
        cost = get_pet_cost(pet_name)
        return (self.wins >= cost and
                pet_name not in self.owned_pets and
                pet_name in self.get_available_pets())

    def handle_movement(self, keys, walls):
        """Handle player movement with precise collision detection"""
        # Calculate proposed movement
        move_x = 0
        move_y = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y += self.speed

        # Move horizontally and check for collisions
        self.rect.x += move_x
        collided_walls = self._get_colliding_walls(walls)
        for wall in collided_walls:
            if move_x > 0:  # Moving right; Hit the left side of the wall
                self.rect.right = wall.rect.left
            elif move_x < 0:  # Moving left; Hit the right side of the wall
                self.rect.left = wall.rect.right

        # Move vertically and check for collisions
        self.rect.y += move_y
        collided_walls = self._get_colliding_walls(walls)
        for wall in collided_walls:
            if move_y > 0:  # Moving down; Hit the top side of the wall
                self.rect.bottom = wall.rect.top
            elif move_y < 0:  # Moving up; Hit the bottom side of the wall
                self.rect.top = wall.rect.bottom

        # Keeps player in gameplay area only
        self.rect.x = clamp_value(self.rect.x, GAMEPLAY_LEFT, GAMEPLAY_RIGHT - self.rect.width)
        self.rect.y = clamp_value(self.rect.y, 0, SCREEN_HEIGHT - self.rect.height)

    def _get_colliding_walls(self, walls):
        """Return a list of walls the player is colliding with"""
        colliding_walls = []
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                colliding_walls.append(wall)
        return colliding_walls

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
        """Reduce health by damage amount (unless shielded)"""
        if self.has_shield():
            print(f"Shield blocked {amount} damage! {self.shield_time_remaining():.1f}s remaining")
            return

        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal_over_time(self):
        """Slowly regenerate health when not at maximum (boosted by pets)"""
        if self.health > 0 and self.health < self.max_health:
            self.health += self.regen_rate  # Now uses pet-boosted regen rate
            if self.health > self.max_health:
                self.health = self.max_health

    def is_alive(self):
        """Check if player is still alive"""
        return self.health > 0

    def activate_shield(self, duration_seconds: float) -> None:
        """Grant/extend a temporary shield that blocks all damage."""
        now = time.monotonic()
        # Stack the shield duration (extend current shield)
        self._shield_end_time = max(self._shield_end_time, now + duration_seconds)
        print(f"Shield activated for {duration_seconds}s! Total shield time: {self.shield_time_remaining():.1f}s")

    def has_shield(self) -> bool:
        """True while shield is active."""
        return time.monotonic() < self._shield_end_time

    def shield_time_remaining(self) -> float:
        """Seconds left on the shield timer."""
        return max(0.0, self._shield_end_time - time.monotonic())
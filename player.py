import pygame
from game_rules import *


class Player:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = START_EXP_TO_LEVEL
        self.evolution = EVOLUTIONS[1]["name"]
        self.body_color = EVOLUTIONS[1]["body_color"]
        self.head_color = EVOLUTIONS[1]["head_color"]
        self.rect = pygame.Rect(50, 50, 50, 50)  # Start in top-left corner
        self.health = PLAYER_START_HEALTH
        self.max_health = PLAYER_START_HEALTH
        self.speed = PLAYER_SPEED

    def move(self, keys, walls):
        # Store original position
        old_x, old_y = self.rect.x, self.rect.y

        # Check keys and move
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player on screen
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

        # Collision with walls
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x, self.rect.y = old_x, old_y  # Revert to old position
                break

    def gain_exp(self, amount):
        self.exp += amount
        print(f"Gained {amount} EXP! Total EXP: {self.exp}")
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.exp_to_next_level *= EXP_MULTIPLIER
        self.health = self.max_health * 2
        self.max_health = self.max_health * 2

        # Check if we have an evolution for this level
        if self.level in EVOLUTIONS:
            evolution_data = EVOLUTIONS[self.level]
            self.evolution = evolution_data["name"]
            self.body_color = evolution_data["body_color"]
            self.head_color = evolution_data["head_color"]

        print(f"Leveled up to {self.level}! Evolved to {self.evolution}")

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def can_buy_pet(self):
        return self.level >= PET_UNLOCK_LEVEL
import pygame
import asyncio
import platform

import game_rules
from game_rules import *
from player import Player
from enemies import Enemy
from walls import create_walls
from graphics import *

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brainrot Evolution 2D")

# Initialize game objects
player = Player()
enemies = []
particles = []
walls = create_walls()
pet = None
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()
enemy_spawn_timer = 0


async def main():
    global pet, enemy_spawn_timer
    running = True

    while running:
        keys = pygame.key.get_pressed()
        if player.health <= 0:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check if clicking on enemies
                for enemy in enemies[:]:
                    if enemy.rect.collidepoint(mouse_pos):
                        # Check if enemy is within attack range
                        distance = ((player.rect.centerx - enemy.rect.centerx) ** 2 +
                                    (player.rect.centery - enemy.rect.centery) ** 2) ** 0.5
                        if distance <= PLAYER_ATTACK_RANGE + enemy.rect.width/2:
                            if enemy.take_damage(PLAYER_CLICK_DAMAGE):
                                player.gain_exp(EXP_PER_ENEMY_KILL)
                                enemies.remove(enemy)
                                # Create explosion particles
                                for _ in range(PARTICLES_PER_EXPLOSION):
                                    particles.append(Particle(enemy.rect.centerx, enemy.rect.centery))
                        else:
                            print("Enemy too far away!")

                # Check if clicking pet button
                if (player.can_buy_pet() and pet is None and
                        pygame.Rect(700, 500, 100, 50).collidepoint(mouse_pos)):
                    pet = Pet()
                    print("Bought a pet!")

        # Update player movement
        player.move(keys, walls)

        # Spawn enemies based on level
        enemy_spawn_timer += 1
        spawn_time = get_spawn_time_for_level(player.level)
        if enemy_spawn_timer > spawn_time:
            enemies.append(Enemy(walls, player.level))
            enemy_spawn_timer = 0

        # Update all enemies
        for enemy in enemies:
            enemy.move_towards_player(player, walls)
            if enemy.can_attack_player(player):
                enemy.attack_player(player)

        # Update pet
        if pet:
            exp_from_pet = pet.update()
            if exp_from_pet > 0:
                player.gain_exp(exp_from_pet)

        # Update particles
        for particle in particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                particles.remove(particle)

        # Draw everything
        draw_background(screen)

        # Draw walls
        for wall in walls:
            draw_wall(screen, wall)

        # Draw player
        draw_player(screen, player)

        # Draw enemies
        for enemy in enemies:
            draw_enemy(screen, enemy, font)

        # Draw pet purchase button
        if player.can_buy_pet() and pet is None:
            draw_pet_button(screen, font)

        # Draw pet
        if pet:
            pet.draw(screen)

        # Draw particles
        for particle in particles:
            particle.draw(screen)

        # Draw UI
        draw_ui(screen, player, font)

        pygame.display.flip()
        clock.tick(FPS)


        if player.health < player.max_health:
            player.health += player.max_health/1000
            if player.health > player.max_health:
                player.health = player.max_health

        await asyncio.sleep(1.0 / FPS)


if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
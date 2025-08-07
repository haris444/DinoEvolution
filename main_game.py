
import asyncio
import platform

import game_rules
from game_rules import *
from player import Player
from enemies import Enemy
from walls import create_walls
from graphics import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brainrot Evolution 2D")

def reset_game():
    global player, enemies, particles, pet, enemy_spawn_timer, game_state
    player = Player()
    enemies = []
    particles = []
    pet = None
    enemy_spawn_timer = 0
    game_state = "playing"

reset_game()
walls = create_walls()
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

async def main():
    global game_state, pet, enemy_spawn_timer, walls
    running = True

    while running:
        if game_state == "playing":
            if player.health <= 0:
                game_state = "game_over"

            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    for enemy in enemies[:]:
                        if enemy.rect.collidepoint(mouse_pos):
                            distance = ((player.rect.centerx - enemy.rect.centerx) ** 2 +
                                        (player.rect.centery - enemy.rect.centery) ** 2) ** 0.5
                            if distance <= PLAYER_ATTACK_RANGE + enemy.rect.width/2:
                                if enemy.take_damage(PLAYER_CLICK_DAMAGE):
                                    player.gain_exp(EXP_PER_ENEMY_KILL)
                                    enemies.remove(enemy)
                                    for _ in range(PARTICLES_PER_EXPLOSION):
                                        particles.append(Particle(enemy.rect.centerx, enemy.rect.centery))
                            else:
                                print("Enemy too far away!")

                    if (player.can_buy_pet() and pet is None and
                            pygame.Rect(700, 500, 100, 50).collidepoint(mouse_pos)):
                        pet = Pet()
                        print("Bought a pet!")

            player.move(keys, walls)

            enemy_spawn_timer += 1
            spawn_time = get_spawn_time_for_level(player.level)
            if enemy_spawn_timer > spawn_time:
                enemies.append(Enemy(walls, player.level))
                enemy_spawn_timer = 0

            for enemy in enemies:
                enemy.move_towards_player(player, walls)
                if enemy.can_attack_player(player):
                    enemy.attack_player(player)

            if pet:
                exp_from_pet = pet.update()
                if exp_from_pet > 0:
                    player.gain_exp(exp_from_pet)

            for particle in particles[:]:
                particle.update()
                if particle.lifetime <= 0:
                    particles.remove(particle)

            draw_background(screen)

            for wall in walls:
                draw_wall(screen, wall)

            draw_player(screen, player)

            for enemy in enemies:
                draw_enemy(screen, enemy, font)

            if player.can_buy_pet() and pet is None:
                draw_pet_button(screen, font)

            if pet:
                pet.draw(screen)

            for particle in particles:
                particle.draw(screen)

            draw_ui(screen, player, font)

            if player.health > 0 and player.health < player.max_health:
                player.health += player.max_health / 1000
                if player.health > player.max_health:
                    player.health = player.max_health

        elif game_state == "game_over":
            play_again_button = draw_game_over_screen(screen, font, player, pet)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.collidepoint(event.pos):
                        reset_game()

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

if __name__ == "__main__":
    if platform.system() == "Emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())
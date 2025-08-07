import asyncio
import platform
import pygame
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game_manager import GameManager


def initialize_pygame():
    """Set up pygame and create the game window"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Brainrot Evolution 2D")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    return screen, font, clock


async def main():
    """Main game loop"""
    # Initialize pygame
    screen, font, clock = initialize_pygame()

    # Create game manager
    game_manager = GameManager(screen, font)

    running = True

    while running:
        # Get current key states
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Let game manager handle other events
                game_manager.handle_input(event)

        # Update game state
        game_manager.update_game(keys)

        # Draw everything
        play_again_button = game_manager.draw_game()

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

        # Async sleep for web compatibility
        await asyncio.sleep(1.0 / FPS)


if __name__ == "__main__":
    # Handle different platforms
    if platform.system() == "Emscripten":
        # For web deployment
        asyncio.ensure_future(main())
    else:
        # For desktop
        asyncio.run(main())
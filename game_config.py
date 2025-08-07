# Game Configuration - All game settings in one place

# Screen Settings - Expanded for UI panel
UI_PANEL_WIDTH = 300  # Left panel for stats
GAMEPLAY_WIDTH = 800   # Main game area width
SCREEN_WIDTH = UI_PANEL_WIDTH + GAMEPLAY_WIDTH  # Total: 1100
SCREEN_HEIGHT = 600
FPS = 60

# Gameplay area boundaries (where player can move and enemies spawn)
GAMEPLAY_LEFT = UI_PANEL_WIDTH  # Start gameplay area after UI panel
GAMEPLAY_RIGHT = SCREEN_WIDTH
GAMEPLAY_TOP = 0
GAMEPLAY_BOTTOM = SCREEN_HEIGHT

# Player Settings - Base values (evolution system now handles stats)
PLAYER_START_HEALTH = 10
PLAYER_BASE_MAX_HEALTH = 10
PLAYER_SPEED = 5
PLAYER_ATTACK_RANGE = 80

# Leveling System
START_EXP_TO_LEVEL = 5
EXP_MULTIPLIER = 2  # Each level requires double the EXP
EXP_PER_ENEMY_KILL = 2.2

# Enemy Base Stats
ENEMY_HEALTH = 5
ENEMY_MIN_SPEED = 1
ENEMY_MAX_SPEED = 3
ENEMY_MIN_DAMAGE = 3
ENEMY_MAX_DAMAGE = 3
ENEMY_ATTACK_RANGE = 60
ENEMY_ATTACK_COOLDOWN = 1000  # milliseconds

# Golden Apple Settings
GOLDEN_APPLE_EXP_VALUE = 5
GOLDEN_APPLE_SPAWN_TIME = 420  # frames (7 seconds at 60 FPS) - spawn less frequently than enemies

# Enemy Appearance Parts
ENEMY_HEADS = [
    ("Frog", (0, 255, 0)),
    ("Cat", (255, 255, 0)),
    ("Rhino", (128, 128, 128)),
    ("Duck", (0, 0, 255)),
    ("Robot", (0, 255, 255))
]

ENEMY_BODIES = [
    ("Tire", (255, 0, 0)),
    ("Box", (139, 69, 19)),
    ("Ball", (128, 0, 128)),
    ("Shoe", (0, 0, 0)),
    ("Pizza", (255, 165, 0))
]

ENEMY_ACCESSORIES = [
    ("Hat", (255, 0, 255)),
    ("Sword", (192, 192, 192)),
    ("Cape", (0, 0, 255)),
    ("Glasses", (0, 0, 0))
]

# Spawning Settings
ENEMY_SPAWN_TIME = 180  # frames (3 seconds at 60 FPS)

# Pet Settings
PET_UNLOCK_LEVEL = 2
PET_EXP_PER_SECOND = 0

# Visual Effects
PARTICLES_PER_EXPLOSION = 10
PARTICLE_LIFETIME = 30  # frames

# Color Constants
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
DARK_GRAY = (64, 64, 64)  # For UI panel background
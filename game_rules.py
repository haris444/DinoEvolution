# Game Rules - This is where you change how the game works!

# Player Settings
PLAYER_START_HEALTH = 10
PLAYER_SPEED = 5

# Leveling Settings
START_EXP_TO_LEVEL = 5
EXP_MULTIPLIER = 2  # How much harder each level gets

# Evolution Settings - Add new evolutions here!
EVOLUTIONS = {
    1: {"name": "Tung Tung", "body_color": (0, 255, 0), "head_color": (255, 255, 0)},  # GREEN, YELLOW
    2: {"name": "Bombardino", "body_color": (255, 0, 0), "head_color": (0, 255, 255)},  # RED, CYAN
    3: {"name": "Tralalero Tralala", "body_color": (0, 0, 255), "head_color": (128, 0, 128)},  # BLUE, PURPLE
}

# Enemy Settings
ENEMY_HEALTH = 5
ENEMY_MIN_SPEED = 1
ENEMY_MAX_SPEED = 3
ENEMY_MIN_DAMAGE = 3
ENEMY_MAX_DAMAGE = 3
ENEMY_ATTACK_RANGE = 60
ENEMY_ATTACK_COOLDOWN = 1000  # milliseconds

# Enemy Parts - Add new parts here!
ENEMY_HEADS = [
    ("Frog", (0, 255, 0)),  # GREEN
    ("Cat", (255, 255, 0)),  # YELLOW
    ("Rhino", (128, 128, 128)),  # GRAY
    ("Duck", (0, 0, 255)),  # BLUE
    ("Robot", (0, 255, 255))  # CYAN
]

ENEMY_BODIES = [
    ("Tire", (255, 0, 0)),  # RED
    ("Box", (139, 69, 19)),  # BROWN
    ("Ball", (128, 0, 128)),  # PURPLE
    ("Shoe", (0, 0, 0)),  # BLACK
    ("Pizza", (255, 165, 0))  # ORANGE
]

ENEMY_ACCESSORIES = [
    ("Hat", (255, 0, 255)),  # MAGENTA
    ("Sword", (192, 192, 192)),  # SILVER
    ("Cape", (0, 0, 255)),  # BLUE
    ("Glasses", (0, 0, 0))  # BLACK
]

# Combat Settings
PLAYER_CLICK_DAMAGE = 1
PLAYER_ATTACK_RANGE = 80  # How far the player can attack
EXP_PER_ENEMY_KILL = 2.2

# Spawning Settings
ENEMY_SPAWN_TIME = 180  # frames (3 seconds at 60 FPS)

# Pet Settings
PET_UNLOCK_LEVEL = 2
PET_EXP_PER_SECOND = 0

# Particle Settings
PARTICLES_PER_EXPLOSION = 10
PARTICLE_LIFETIME = 30  # frames

# Game Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


def get_spawn_time_for_level(level):
    """Make enemies spawn faster at higher levels!"""
    if level >= 5:
        return 60  # Very fast spawning
    elif level >= 3:
        return 120  # Faster spawning
    else:
        return ENEMY_SPAWN_TIME  # Normal spawning


def get_enemy_stats_for_level(level):
    """Make enemies stronger at higher levels!"""
    health_bonus = (level - 1) * 10
    speed_bonus = min(2, level // 2)  # Max +2 speed
    damage_bonus = (level - 1) * 5

    return {
        "health": ENEMY_HEALTH + health_bonus,
        "min_speed": ENEMY_MIN_SPEED + speed_bonus,
        "max_speed": ENEMY_MAX_SPEED + speed_bonus,
        "min_damage": ENEMY_MIN_DAMAGE + damage_bonus,
        "max_damage": ENEMY_MAX_DAMAGE + damage_bonus
    }
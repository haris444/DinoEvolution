import random
from game_config import *


def calculate_distance(pos1, pos2):
    """Calculate distance between two points using Pythagorean theorem"""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return (dx ** 2 + dy ** 2) ** 0.5


def normalize_vector(dx, dy):
    """Convert a direction vector to unit length (magnitude = 1)"""
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance == 0:
        return 0, 0
    return dx / distance, dy / distance


def calculate_spawn_time_for_level(level):
    """Calculate enemy spawn rate based on level using exponential decrease"""
    if level >= 5:
        return 60  # Very fast spawning
    elif level >= 3:
        return 120  # Faster spawning
    else:
        return ENEMY_SPAWN_TIME  # Normal spawning


def calculate_enemy_stats_for_level(level):
    """Calculate enemy strength using linear scaling formulas"""
    # Linear growth: base_value + (level - 1) * multiplier
    health_bonus = (level - 1) * 10
    damage_bonus = (level - 1) * 5

    # Speed has a maximum cap to prevent impossible gameplay
    speed_bonus = min(2, level // 2)  # Integer division, max +2 speed

    return {
        "health": ENEMY_HEALTH + health_bonus,
        "min_speed": ENEMY_MIN_SPEED + speed_bonus,
        "max_speed": ENEMY_MAX_SPEED + speed_bonus,
        "min_damage": ENEMY_MIN_DAMAGE + damage_bonus,
        "max_damage": ENEMY_MAX_DAMAGE + damage_bonus
    }


def calculate_boss_stats_for_level(level):
    """Calculate boss enemy strength using linear scaling formulas and multipliers"""
    base_stats = calculate_enemy_stats_for_level(level)

    health_multiplier = random.uniform(BOSS_HEALTH_MULTIPLIER_MIN, BOSS_HEALTH_MULTIPLIER_MAX)
    damage_multiplier = random.uniform(BOSS_DAMAGE_MULTIPLIER_MIN, BOSS_DAMAGE_MULTIPLIER_MAX)

    return {
        "health": base_stats["health"] * health_multiplier,
        "min_speed": base_stats["min_speed"],  # Speed remains the same
        "max_speed": base_stats["max_speed"],
        "min_damage": base_stats["min_damage"] * damage_multiplier,
        "max_damage": base_stats["max_damage"] * damage_multiplier,
    }


def calculate_experience_needed(level):
    """Calculate EXP needed for next level using exponential growth"""
    return START_EXP_TO_LEVEL * (EXP_MULTIPLIER ** (level - 1))


def generate_random_spawn_position():
    """Generate a random position just outside the gameplay area boundaries"""
    side = random.randint(0, 3)

    if side == 0:  # Top of gameplay area
        x = random.randint(GAMEPLAY_LEFT, GAMEPLAY_RIGHT - 40)
        y = GAMEPLAY_TOP - 40
    elif side == 1:  # Right of gameplay area
        x = GAMEPLAY_RIGHT
        y = random.randint(GAMEPLAY_TOP, GAMEPLAY_BOTTOM - 40)
    elif side == 2:  # Bottom of gameplay area
        x = random.randint(GAMEPLAY_LEFT, GAMEPLAY_RIGHT - 40)
        y = GAMEPLAY_BOTTOM
    else:  # Left of gameplay area (but not in UI panel)
        x = GAMEPLAY_LEFT - 40
        y = random.randint(GAMEPLAY_TOP, GAMEPLAY_BOTTOM - 40)

    return x, y


def clamp_value(value, min_val, max_val):
    """Keep a value within specified bounds"""
    return max(min_val, min(max_val, value))


def calculate_health_percentage(current_health, max_health):
    """Calculate health as a percentage (0.0 to 1.0)"""
    if max_health == 0:
        return 0
    return current_health / max_health
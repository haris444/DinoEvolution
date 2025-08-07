# Evolution System - Player Stats and Appearance by Level
# Each evolution roughly doubles the previous stats with some variation

EVOLUTIONS = {
    1: {
        "name": "Tung Tung Sahur",
        "body_color": (0, 255, 0),  # Green
        "head_color": (255, 255, 0),  # Yellow
        "stats": {
            "damage": 1,
            "health": 10,
            "speed": 5
        },
        "specialty": "Balanced starter form"
    },

    2: {
        "name": "Skibidi Bopbop",
        "body_color": (255, 100, 100),  # Light Red
        "head_color": (100, 255, 255),  # Light Cyan
        "stats": {
            "damage": 2,
            "health": 20,
            "speed": 6
        },
        "specialty": "Balanced growth"
    },

    3: {
        "name": "Rizzleroni Pizzini",
        "body_color": (255, 150, 0),  # Orange
        "head_color": (255, 0, 255),  # Magenta
        "stats": {
            "damage": 5,
            "health": 35,
            "speed": 7
        },
        "specialty": "High damage focus"
    },

    4: {
        "name": "Gigachadino Chadello",
        "body_color": (128, 0, 128),  # Purple
        "head_color": (255, 215, 0),  # Gold
        "stats": {
            "damage": 8,
            "health": 80,
            "speed": 9
        },
        "specialty": "Tank build - massive health"
    },

    5: {
        "name": "Bombardino Crocodilo",
        "body_color": (0, 128, 0),  # Dark Green
        "head_color": (255, 0, 0),  # Red
        "stats": {
            "damage": 18,
            "health": 120,
            "speed": 10
        },
        "specialty": "Explosive damage dealer"
    },

    6: {
        "name": "Ohio Skibadilo",
        "body_color": (75, 0, 130),  # Indigo
        "head_color": (255, 165, 0),  # Orange
        "stats": {
            "damage": 30,
            "health": 200,
            "speed": 12
        },
        "specialty": "Speed demon - ultra fast"
    },

    7: {
        "name": "Memeo Ladzini",
        "body_color": (255, 20, 147),  # Deep Pink
        "head_color": (0, 255, 127),  # Spring Green
        "stats": {
            "damage": 55,
            "health": 350,
            "speed": 13
        },
        "specialty": "Meme power activation"
    },

    8: {
        "name": "TikToki Trappini",
        "body_color": (64, 224, 208),  # Turquoise
        "head_color": (139, 0, 139),  # Dark Magenta
        "stats": {
            "damage": 120,
            "health": 500,
            "speed": 15
        },
        "specialty": "Viral damage multiplier"
    },

    9: {
        "name": "Yeetini Bananello",
        "body_color": (255, 255, 0),  # Yellow
        "head_color": (255, 69, 0),  # Red Orange
        "stats": {
            "damage": 200,
            "health": 800,
            "speed": 16
        },
        "specialty": "Potassium-powered chaos"
    },

    10: {
        "name": "Tralalelo Tralala",
        "body_color": (138, 43, 226),  # Blue Violet
        "head_color": (50, 205, 50),  # Lime Green
        "stats": {
            "damage": 350,
            "health": 1500,
            "speed": 17
        },
        "specialty": "Musical destruction"
    },

    11: {
        "name": "Skibombini Boomala",
        "body_color": (220, 20, 60),  # Crimson
        "head_color": (255, 215, 0),  # Gold
        "stats": {
            "damage": 750,
            "health": 2200,
            "speed": 18
        },
        "specialty": "Explosive specialist"
    },

    12: {
        "name": "Chimpanzini Bananini",
        "body_color": (139, 69, 19),  # Saddle Brown
        "head_color": (255, 255, 0),  # Yellow
        "stats": {
            "damage": 1200,
            "health": 4000,
            "speed": 20
        },
        "specialty": "Primal banana fury"
    },

    13: {
        "name": "Bombombini Gusini",
        "body_color": (25, 25, 112),  # Midnight Blue
        "head_color": (255, 0, 255),  # Magenta
        "stats": {
            "damage": 2500,
            "health": 6500,
            "speed": 21
        },
        "specialty": "Gusto overload"
    },

    14: {
        "name": "Burbaloni Luliloli",
        "body_color": (255, 182, 193),  # Light Pink
        "head_color": (72, 61, 139),  # Dark Slate Blue
        "stats": {
            "damage": 4000,
            "health": 12000,
            "speed": 22
        },
        "specialty": "Cuteness with deadly power"
    },

    15: {
        "name": "Brr Brr Patapim",
        "body_color": (173, 216, 230),  # Light Blue
        "head_color": (255, 255, 255),  # White
        "stats": {
            "damage": 8000,
            "health": 20000,
            "speed": 23
        },
        "specialty": "Ice cold elimination"
    },

    16: {
        "name": "Zoomeroni Glitchilo",
        "body_color": (0, 255, 255),  # Cyan
        "head_color": (255, 0, 128),  # Hot Pink
        "stats": {
            "damage": 15000,
            "health": 35000,
            "speed": 25
        },
        "specialty": "Digital reality breaker"
    },

    17: {
        "name": "Lollololo Memezzini",
        "body_color": (255, 105, 180),  # Hot Pink
        "head_color": (127, 255, 0),  # Chart Green
        "stats": {
            "damage": 30000,
            "health": 60000,
            "speed": 26
        },
        "specialty": "Ultimate meme lord"
    },

    18: {
        "name": "Bruhbruh Bananado",
        "body_color": (255, 215, 0),  # Gold
        "head_color": (128, 0, 128),  # Purple
        "stats": {
            "damage": 55000,
            "health": 120000,
            "speed": 28
        },
        "specialty": "Tornado of bruh energy"
    },

    19: {
        "name": "Skibadilo Ultrapim",
        "body_color": (186, 85, 211),  # Medium Orchid
        "head_color": (255, 20, 147),  # Deep Pink
        "stats": {
            "damage": 100000,
            "health": 200000,
            "speed": 30
        },
        "specialty": "Ultra instinct activated"
    },

    20: {
        "name": "Gigaloni Memeotrono",
        "body_color": (255, 255, 255),  # White
        "head_color": (0, 0, 0),  # Black
        "stats": {
            "damage": 200000,
            "health": 500000,
            "speed": 35
        },
        "specialty": "FINAL FORM - Transcendent being"
    }
}


def get_evolution_data(level):
    """Get evolution data for a specific level"""
    if level in EVOLUTIONS:
        return EVOLUTIONS[level]
    else:
        # Return the highest evolution if level exceeds available evolutions
        max_level = max(EVOLUTIONS.keys())
        return EVOLUTIONS[max_level]


def get_player_stats_for_level(level):
    """Get just the stats for a specific level"""
    evolution_data = get_evolution_data(level)
    return evolution_data["stats"]


def get_evolution_name(level):
    """Get just the evolution name for a specific level"""
    evolution_data = get_evolution_data(level)
    return evolution_data["name"]


def get_evolution_colors(level):
    """Get just the colors for a specific level"""
    evolution_data = get_evolution_data(level)
    return evolution_data["body_color"], evolution_data["head_color"]
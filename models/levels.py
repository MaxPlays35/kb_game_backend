from math import floor


levels = {
    1: [1.0, 800, 3.0, 6500],
    2: [1.5, 650, 2.5, 6000],
    3: [2.0, 500, 2.0, 5500],
    4: [2.5, 400, 1.5, 5000],
    5: [3.0, 300, 1.0, 4500],
}


def level(alive_players: int, level: int):
    return {
        "level": level,
        "volume": floor(levels[level][0] * alive_players),
        "minPriceRow": levels[level][1],
        "maxDestroyers": floor(levels[level][2] * alive_players),
        "maxPriceDestroyer": levels[level][3],
    }

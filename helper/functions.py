from helper.move import *

MOVES_PER_POKEMON = 4


def findPokemon(name, pokemons):
    return max(pokemons, key=lambda x: int(name in x[1]) + int(x[1] in name))


def findPokemonId(id, pokemons):
    for p in pokemons:
        if id == p[0]:
            return p
    return False


def moveStats(name, moves):
    return min(moves, key=lambda x: sum(1 for a, b in zip(name, x.name) if a != b) + abs(len(name) - len(x.name)))


def moveStatsId(id, moves):
    for p in moves:
        if id == p.id:
            return p
    return False

def calcEffictiveness(defender, move):
    multiplier = 1
    if move.type == "Normal":
        for x in defender.types:
            if x == "Steel" or x == "Rock":
                multiplier *= .5
            if x == "Ghost":
                multiplier = 0
    elif move.type == "Fighting":
        for x in defender.types:
            if x == "Steel" or x == "Normal" or x == "Ice" or x == "Rock":
                multiplier *= 2
            if x == "Fairy" or x == "Poison" or x == "Bug" or x == "Flying" or x == "Psychic":
                multiplier *= .5
            if x == "Ghost":
                multiplier = 0
    elif move.type == "Flying":
        for x in defender.types:
            if x == "Fighting" or x == "Bug" or x == "Grass" or x == "Rock":
                multiplier *= 2
            if x == "Steel" or x == "Rock" or x == "Electric":
                multiplier *= .5
    elif move.type == "Poison":
        for x in defender.types:
            if x == "Grass" or x == "Fairy":
                multiplier *= 2
            if x == "Poison" or x == "Ground" or x == "Rock" or x == "Ghost":
                multiplier *= .5
            if x == "Steel":
                multiplier *= 0
    elif move.type == "Ground":
        for x in defender.types:
            if x == "Poison" or x == "Rock" or x == "Steel" or x == "Fire" or x == "Electric":
                multiplier *= 2
            if x == "Bug" or x == "Grass":
                multiplier *= .5
            if x == "Flying":
                multiplier *= 0
    elif move.type == "Rock":
        for x in defender.types:
            if x == "Flying" or x == "Bug" or x == "Fire" or x == "Ice":
                multiplier *= 2
            if x == "Fighting" or x == "Ground" or x == "Steel":
                multiplier *= .5
    elif move.type == "Bug":
        for x in defender.types:
            if x == "Grass" or x == "Psychic" or x == "Dark":
                multiplier *= 2
            if x == "Fighting" or x == "Flying" or x == "Poison" or x == "Ghost" or x == "Fire" or x == "Fairy" or x == "Steel":
                multiplier *= .5
    elif move.type == "Ghost":
        for x in defender.types:
            if x == "Ghost" or x == "Psychic":
                multiplier *= 2
            if x == "Dark":
                multiplier *= .5
            if x == "Normal":
                multiplier *= 0
    elif move.type == "Steel":
        for x in defender.types:
            if x == "Rock" or x == "Ice" or x == "Fairy":
                multiplier *= 2
            if x == "Water" or x == "Fire" or x == "Steel" or x == "Electric":
                multiplier *= .5
    elif move.type == "Fire":
        for x in defender.types:
            if x == "Grass" or x == "Bug" or x == "Ice" or x == "Steel":
                multiplier *= 2
            if x == "Water" or x == "Rock" or x == "Fire" or x == "Dragon":
                multiplier *= .5
    elif move.type == "Water":
        for x in defender.types:
            if x == "Ground" or x == "Rock" or x == "Fire":
                multiplier *= 2
            if x == "Grass" or x == "Water" or x == "Dragon":
                multiplier *= .5
    elif move.type == "Grass":
        for x in defender.types:
            if x == "Water" or x == "Ground" or x == "Rock":
                multiplier *= 2
            if x == "Grass" or x == "Bug" or x == "Fire" or x == "Dragon" or x == "Flying" or x == "Poison" or x == "Steel":
                multiplier *= .5
    elif move.type == "Electric":
        for x in defender.types:
            if x == "Flying" or x == "Water":
                multiplier *= 2
            if x == "Grass" or x == "Electric" or x == "Dragon":
                multiplier *= .5
            if x == "Ground":
                multiplier *= 0
    elif move.type == "Psychic":
        for x in defender.types:
            if x == "Fighting" or x == "Poison":
                multiplier *= 2
            if x == "Steel" or x == "Psychic":
                multiplier *= .5
            if x == "Dark":
                multiplier *= 0
    elif move.type == "Ice":
        for x in defender.types:
            if x == "Flying" or x == "Ground" or x == "Dragon":
                multiplier *= 2
            if x == "Fire" or x == "Ice" or x == "Water" or x == "Steel":
                multiplier *= .5
    elif move.type == "Dragon":
        for x in defender.types:
            if x == "Dragon":
                multiplier *= 2
            if x == "Steel":
                multiplier *= .5
            if x == "Fairy":
                multiplier *= 0
    elif move.type == "Dark":
        for x in defender.types:
            if x == "Psychic" or x == "Ghost":
                multiplier *= 2
            if x == "Fairy" or x == "Dark" or x == "Fighting":
                multiplier *= .5
    elif move.type == "Fairy":
        for x in defender.types:
            if x == "Dragon" or x == "Dark" or x == "Fighting":
                multiplier *= 2
            if x == "Fire" or x == "Steel" or x == "Poison":
                multiplier *= .5
    return multiplier


def calcDamage(defender, attacker, move, game):
    typeMultiplier = calcEffictiveness(defender, move)
    stab = 1
    for x in attacker.types:
        if move.type == x:
            stab *= 1.5
    try:
        a = attacker.atk
        d = defender.dfn
        if move.sort == 1:
            a = attacker.spa
            d = defender.spd
        damage = ((2 * attacker.level / 5 + 2) * int(move.damage) * a / d) / 50 + 2
        weather = 1
        if game.weather == 'sun':
            if move.type == 'Water':
                weather *= .5
            elif move.type == 'Fire':
                weather *= 1.5
        elif game.weather == 'rain':
            if move.type == 'Fire':
                weather *= .5
            elif move.type == 'Water':
                weather *= 1.5
        modifier = stab * typeMultiplier * weather
        damage *= modifier
        return damage
    except Exception as e:
        print(e)
        return 0


def calcKo(defender, attacker, move, game):
    damage = calcDamage(defender, attacker, move, game)
    if move.name == "Freeze-Dry":
        return SPECIAL_DAMAGE_MOVES[move.name](move.type, damage * 0.85)
    if move.name == "Seismic Toss" or move.name == "Night Shade":
        return SPECIAL_DAMAGE_MOVES[move.name](attacker.level)
    return damage * 0.85

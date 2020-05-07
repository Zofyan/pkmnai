STATUS_EFFECTS = {
    'bad_poison': 1,
    'poison': 2,
    'burn': 3,
    'paralysis': 4,
    'freeze': 5,
    'sleep': 6
}

TYPE_CHART = {
    'Typeless': 0,
    'Normal': 1,
    'Fighting': 2,
    'Flying': 3,
    'Fire': 4,
    'Water': 5,
    'Grass': 6,
    'Electric': 7,
    'Rock': 8,
    'Ground': 9,
    'Steel': 10,
    'Ice': 11,
    'Psychic': 12,
    'Dark': 13,
    'Ghost': 14,
    'Bug': 15,
    'Poison': 16,
    'Dragon': 17,
    'Fairy': 18
}
STATUS_EFFECT_MOVES = {
    'toxic': [STATUS_EFFECTS['bad_poison'], 1],
    'Beak Blast': [STATUS_EFFECTS['burn'], 1],
    'Blaze Kick': [STATUS_EFFECTS['burn'], 0.1],
    'Blue Flare': [STATUS_EFFECTS['burn'], 0.2],
    'Ember': [STATUS_EFFECTS['burn'], 0.1],
    'Fire Blast': [STATUS_EFFECTS['burn'], 0.1],
    'Fire Fang': [STATUS_EFFECTS['burn'], 0.1],
    'Fire Punch': [STATUS_EFFECTS['burn'], 0.1],
    'Flamethrower': [STATUS_EFFECTS['burn'], 0.1],
    'Flame Wheel': [STATUS_EFFECTS['burn'], 0.1],
    'Heat Wave': [STATUS_EFFECTS['burn'], 0.1],
    'Ice Burn': [STATUS_EFFECTS['burn'], 0.3],
    'Inferno': [STATUS_EFFECTS['burn'], 1.0],
    'Lava Plume': [STATUS_EFFECTS['burn'], 0.3],
    'Sacred Fire': [STATUS_EFFECTS['burn'], 0.5],
    'Scald': [STATUS_EFFECTS['burn'], 0.3],
    'Searing Shot': [STATUS_EFFECTS['burn'], 0.3],
    'Steam Eruption': [STATUS_EFFECTS['burn'], 0.3],
    'Will-O-Wisp': [STATUS_EFFECTS['burn'], 1.0],
    'Body Slam': [STATUS_EFFECTS['paralysis'], 0.3],
    'Bolt Strike': [STATUS_EFFECTS['paralysis'], 0.2],
    'Bounce': [STATUS_EFFECTS['paralysis'], 0.3],
    'Discharge': [STATUS_EFFECTS['paralysis'], 0.3],
    'Dragon Breath': [STATUS_EFFECTS['paralysis'], 0.3],
    'Force Palm': [STATUS_EFFECTS['paralysis'], 0.3],
    'Freeze Shock': [STATUS_EFFECTS['paralysis'], 0.3],
    'Glare': [STATUS_EFFECTS['paralysis'], 1.0],
    'Lick': [STATUS_EFFECTS['paralysis'], 0.3],
    'Nuzzle': [STATUS_EFFECTS['paralysis'], 1.0],
    'Spark': [STATUS_EFFECTS['paralysis'], 0.3],
    'Stoked Sparksurfer': [STATUS_EFFECTS['paralysis'], 1.0],
    'Stun Spore': [STATUS_EFFECTS['paralysis'], 1.0],
    'Thunder': [STATUS_EFFECTS['paralysis'], 0.3],
    'Thunder Fang': [STATUS_EFFECTS['paralysis'], 0.1],
    'Thunder Punch': [STATUS_EFFECTS['paralysis'], 0.1],
    'Thunder Shock': [STATUS_EFFECTS['paralysis'], 0.1],
    'Thunder Wave': [STATUS_EFFECTS['paralysis'], 1.0],
    'Thunderbolt': [STATUS_EFFECTS['paralysis'], 0.1],
    'Volt Tackle': [STATUS_EFFECTS['paralysis'], 0.1],
    'Zap Cannon': [STATUS_EFFECTS['paralysis'], 1.0],
    'Dark Void': [STATUS_EFFECTS['sleep'], 1.0],
    'Hypnosis': [STATUS_EFFECTS['sleep'], 1.0],
    'Lovely Kiss': [STATUS_EFFECTS['sleep'], 1.0],
    'Relic Song': [STATUS_EFFECTS['sleep'], 0.1],
    'Rest': [STATUS_EFFECTS['sleep'], 1.0],
    'Sing': [STATUS_EFFECTS['sleep'], 1.0],
    'Sleep Powder': [STATUS_EFFECTS['sleep'], 1.0],
    'Spore': [STATUS_EFFECTS['sleep'], 1.0],
    'Yawn': [STATUS_EFFECTS['sleep'], 1.0],
    'Cross Poison': [STATUS_EFFECTS['poison'], 0.1],
    'Gunk Shot': [STATUS_EFFECTS['poison'], 0.3],
    'Poison Gas': [STATUS_EFFECTS['poison'], 1.0],
    'Poison Jab': [STATUS_EFFECTS['poison'], 0.3],
    'Poison Powder': [STATUS_EFFECTS['poison'], 1.0],
    'Poison Sting': [STATUS_EFFECTS['poison'], 0.3],
    'Poison Tail': [STATUS_EFFECTS['poison'], 0.1],
    'Sludge': [STATUS_EFFECTS['poison'], 0.3],
    'Sludge Bomb': [STATUS_EFFECTS['poison'], 0.3],
    'Sludge Wave': [STATUS_EFFECTS['poison'], 0.1],
    'Smog': [STATUS_EFFECTS['poison'], 0.4],
    'Toxic Thread': [STATUS_EFFECTS['poison'], 1.0],
    'Twineedle': [STATUS_EFFECTS['poison'], 0.2],
    'Toxic': [STATUS_EFFECTS['bad_poison'], 1.0],
    'Poison Fang': [STATUS_EFFECTS['bad_poison'], 0.5]
}

SPECIAL_DAMAGE_MOVES = {
    'Freeze-Dry': (lambda types, dmg: dmg * (1 + int("Water" in types))),
    'Seismic Toss': (lambda a, b: a.level),
    'Night Shade': (lambda a, b: a.level),
    'Gyroball': (lambda a, b: min),
    'Dragon Rage': (lambda a, b: 40),
    'Sonic Boom': (lambda a, b: 20)
}

STAT_MOVES = {
    'Acid Armor': [0, 2, 0, 0, 0, 0, 0],
    'Agility': [0, 0, 0, 0, 2, 0, 0],
    'Amnesia': [0, 0, 0, 2, 0, 0, 0],
    'Aromatic Mist': [0, 1, 0, 1, 0, 0, 0],
    'Autotomize': [0, 0, 0, 0, 2, 0, 0],
    'Baby-Doll Eyes': [-1, 0, 0, 0, 0, 0, 0],
    'Barrier': [0, 2, 0, 0, 0, 0, 0],
    'Belly Drum': [12, 0, 0, 0, 0, 0, 0],
    'Bulk Up': [1, 1, 0, 0, 0, 0, 0],
    'Calm Mind': [0, 0, 1, 1, 0, 0, 0],
    'Charm': [-2, 0, 0, 0, 0, 0, 0],
    'Coil': [1, 1, 0, 0, 0, 1, 0],
    'Confide': [0, 0, -1, 0, 0, 0, 0],
    'Cosmic Power': [0, 1, 0, 1, 0, 0, 0],
    'Cotton Guard': [0, 0, 0, 3, 0, 0, 0],
    'Cotton Spore': [0, 0, 0, 0, -2, 0, 0],
    'Defend Order': [0, 1, 0, 1, 0, 0, 0],
    'Curse': [1, 0, 1, 0, -1, 0, 0],
    'Dragon Dance': [0, 0, 0, 0, 0, 0, 0],
    'Gear Up': [1, 0, 1, 0, 0, 0, 0],
    'Geomancy': [0, 2, 0, 2, 2, 0, 0],
    'Harden': [0, 1, 0, 0, 0, 0, 0],
    'Hone Claws': [1, 0, 0, 0, 0, 1, 0],
    'Iron Defense': [0, 2, 0, 0, 0, 0, 0],
    'Meditate': [1, 0, 0, 0, 0, 0, 0],
    'Memento': [-2, 0, -2, 0, 0, 0, 0],
    'Metal Sound': [0, 0, 0, -2, 0, 0, 0],
    'Nasty Plot': [0, 0, 2, 0, 0, 0, 0],
    'Noble Roar': [-1, -1, 0, 0, 0, 0, 0],
    'Parting Shot': [-1, 0, -1, 0, 0, 0, 0],
    'Quiver Dance': [0, 0, 1, 1, 1, 0, 0],
    'Rock Polish': [0, 0, 0, 0, 2, 0, 0],
    'Shell Smash': [2, -1, 2, -1, 2, 0, 0],
    'Shift Gear': [1, 0, 0, 0, 2, 0, 0],
    'Strength Sap': [0, 0, 0, 0, 0, 0, 0],
    'Swords Dance': [2, 0, 0, 0, 0, 0, 0],
    'Tail Glow': [0, 0, 3, 0, 0, 0, 0],
    'Work Up': [1, 0, 1, 0, 0, 0, 0]
}


class Move:
    def __init__(self, move):
        self.id = move[0]
        self.name = move[1]
        self.type = move[2]
        self.sort = move[3]
        self.damage = move[4]
        self.accuracy = move[5]
        self.calculatedDamage = 0
        self.statChange = [0, 0, 0, 0, 0, 0, 0]
        self.statusEffect = 0
        try:
            self.statChange = STAT_MOVES[self.name]
        except KeyError:
            self.statChange = [0, 0, 0, 0, 0, 0, 0]
        try:
            self.statusEffect = STATUS_EFFECT_MOVES[self.name]
        except KeyError:
            self.statusEffect = [0, 0]


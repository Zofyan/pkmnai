import math
from helper.move import *
import numpy
from keras.engine.saving import load_model

statChangesEffects = {
    6: 8 / 2,
    5: 7 / 2,
    4: 6 / 2,
    3: 6 / 2,
    2: 4 / 2,
    1: 3 / 2,
    0: 2 / 2,
    -1: 2 / 3,
    -2: 2 / 4,
    -3: 2 / 5,
    -4: 2 / 6,
    -5: 2 / 7,
    -6: 2 / 8
}

statChangesEffectsAlt = {
    6: 9 / 3,
    5: 8 / 3,
    4: 7 / 3,
    3: 6 / 3,
    2: 5 / 3,
    1: 4 / 3,
    0: 3 / 3,
    -1: 3 / 4,
    -2: 3 / 5,
    -3: 3 / 6,
    -4: 3 / 7,
    -5: 3 / 8,
    -6: 3 / 9
}


class Pokemon:

    def __init__(self, pokemonData, level=100):
        # print(pokemonData)

        self.level = 100
        self.nature = "Hardy"
        self.moves = []
        self.statChanges = [0, 0, 0, 0, 0, 0, 0]
        self.evs = [0, 0, 0, 0, 0, 0]
        self.ivs = [31, 31, 31, 31, 31, 31]
        self.currentHp = 0
        self.ability = ""
        self.item = ""
        self.moves = []
        self.status = 0

        self.id = pokemonData[0]
        self.name = pokemonData[1]
        self.atk = pokemonData[4][1]
        self.dfn = pokemonData[4][2]
        self.spa = pokemonData[4][3]
        self.spd = pokemonData[4][4]
        self.spe = pokemonData[4][5]
        self.acc = 1
        self.eva = 1
        self.hp = pokemonData[4][0]
        self.types = pokemonData[2]

        self.currentHp = self.hp

    def getStat(self, stat):
        modifier = 1
        if stat == "spe" and self.status == STATUS_EFFECTS['paralysis']:
            modifier *= .5
        if stat == "atk" and self.status == STATUS_EFFECTS['burn']:
            modifier *= 0.5
        if stat == "hp":
            return (math.floor((int(self.hp) * 2 + int(self.ivs[0]) + math.floor(int(self.evs[0]) / 4)) * self.level / 100) + self.level + 10) * statChangesEffects[self.statChanges[0]] * modifier
        if stat == "atk":
            return (math.floor((int(self.atk) * 2 + int(self.ivs[1]) + math.floor(int(self.evs[1]) / 4)) * self.level / 100) + 5) * statChangesEffects[self.statChanges[1]] * modifier
        if stat == "dfn":
            return (math.floor((int(self.dfn) * 2 + int(self.ivs[2]) + math.floor(int(self.evs[2]) / 4)) * self.level / 100) + 5) * statChangesEffects[self.statChanges[2]] * modifier
        if stat == "spa":
            return (math.floor((int(self.spa) * 2 + int(self.ivs[3]) + math.floor(int(self.evs[3]) / 4)) * self.level / 100) + 5) * statChangesEffects[self.statChanges[3]] * modifier
        if stat == "spd":
            return (math.floor((int(self.spd) * 2 + int(self.ivs[4]) + math.floor(int(self.evs[4]) / 4)) * self.level / 100) + 5) * statChangesEffects[self.statChanges[4]] * modifier
        if stat == "spe":
            return (math.floor((int(self.spe) * 2 + int(self.ivs[5]) + math.floor(int(self.evs[5]) / 4)) * self.level / 100) + 5) * statChangesEffects[self.statChanges[5]] * modifier


    def updateStats(self):
        self.atk *= statChangesEffects[self.statChanges[0]]
        self.dfn *= statChangesEffects[self.statChanges[1]]
        self.spa *= statChangesEffects[self.statChanges[2]]
        self.spd *= statChangesEffects[self.statChanges[3]]
        self.spe *= statChangesEffects[self.statChanges[4]]
        self.acc *= statChangesEffectsAlt[self.statChanges[5]]
        self.eva *= statChangesEffectsAlt[self.statChanges[6]]

    def takeDamage(self, fraction):
        self.currentHp -= self.hp * fraction

    def setMove(self, move):

        try:
            self.moves.index(move)
        except ValueError:
            self.moves.append(move)

    def predictMoves(self):
        inputMoves = numpy.zeros((1, 11))
        inputMoves[0][0] = self.id
        inputMoves[0][1] = self.evs[0]
        inputMoves[0][2] = self.evs[1]
        inputMoves[0][3] = self.evs[2]
        inputMoves[0][4] = self.evs[3]
        inputMoves[0][5] = self.evs[4]
        inputMoves[0][6] = self.evs[5]
        for i in range(1, len(self.moves) + 1):
            inputMoves[0][6 + i] = self.moves[i - 1]
        prediction = movesAi.predict(inputMoves)
        return prediction

    def calcStat(self, base, iv, ev, hp=False):
        if not hp:
            return math.floor((int(base) * 2 + int(iv) + math.floor(int(ev) / 4)) * self.level / 100) + 5
        return math.floor((int(base) * 2 + int(iv) + math.floor(int(ev) / 4)) * self.level / 100) + self.level + 10

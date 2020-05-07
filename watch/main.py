import sys

from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import sgd

sys.path.append("..")
from interact import Game
from helper.functions import findPokemon, moveStats, calcKo, moveStatsId
import random
import time
import pickle
from helper.move import *
from helper.pokemon import *


with open('../moves.txt', 'rb') as file:
    moves = pickle.load(file)
with open('../pokemon.txt', 'rb') as file:
    pokemons = pickle.load(file)
game = Game("")
training = []
answer = []
import os, os.path
DIR = "replays/"
start = int(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) / 2)
for i in range(0, start):
    replay = open("replays/replay" + str(i) + ".html")
    info = open("replays/info" + str(i) + ".html")
    myPokemon = []
    enemyPokemon = []
    for line in info:
        if "@" in line and len(myPokemon) < 6:
            myPokemon.append(Pokemon(findPokemon(line.split("@")[0].strip(), pokemons)))
        elif "@" in line:
            enemyPokemon.append(Pokemon(findPokemon(line.split("@")[0].strip(), pokemons)))
        if len(myPokemon) > 0 and len(enemyPokemon) == 0:
            if line[0] == "-" and line[1] != "-":
                myPokemon[-1].setMove(moveStats(line[2:], moves).id)
        elif len(enemyPokemon) > 0:
            if line[0] == "-" and line[1] != "-":
                enemyPokemon[-1].setMove(moveStats(line[2:], moves).id)
    for line in replay:
        data = line.split("|")
        if len(data) < 2:
            continue
        if data[1] == "turn":
            training.append([])
            answer.append([])
        if data[1] == "switch" and "p1a" in line:
            for p in myPokemon:
                if p.name == data[2][5:]:
                    myCurrentPokemon = p
                    myCurrentPokemon.statChanges = [0, 0, 0, 0, 0, 0, 0]
        elif data[1] == "switch":
            for p in enemyPokemon:
                if p.name == data[2][5:]:
                    enemyCurrentPokemon = p
                    enemyCurrentPokemon.statChanges = [0, 0, 0, 0, 0, 0, 0]

        if data[1] == "-boost":
            if "p1a" in line:
                if data[3] == "atk":
                    myCurrentPokemon.statChanges[0] += int(data[4])
                if data[3] == "def":
                    myCurrentPokemon.statChanges[1] += int(data[4])
                if data[3] == "spa":
                    myCurrentPokemon.statChanges[2] += int(data[4])
                if data[3] == "spd":
                    myCurrentPokemon.statChanges[3] += int(data[4])
                if data[3] == "spe":
                    myCurrentPokemon.statChanges[4] += int(data[4])
                myCurrentPokemon.updateStats()
            else:
                if data[3] == "atk":
                    enemyCurrentPokemon.statChanges[0] += int(data[4])
                if data[3] == "def":
                    enemyCurrentPokemon.statChanges[1] += int(data[4])
                if data[3] == "spa":
                    enemyCurrentPokemon.statChanges[2] += int(data[4])
                if data[3] == "spd":
                    enemyCurrentPokemon.statChanges[3] += int(data[4])
                if data[3] == "spe":
                    enemyCurrentPokemon.statChanges[4] += int(data[4])
                enemyCurrentPokemon.updateStats()

        if data[1] == "-damage":
            if "p1a" in line:
                myCurrentPokemon.currentHp = float(data[3].split("\\")[0].split()[0]) * myCurrentPokemon.hp / 100
            else:
                enemyCurrentPokemon.currentHp = float(data[3].split("\\")[0].split()[0]) * enemyCurrentPokemon.hp / 100
        try:
            if myCurrentPokemon and enemyCurrentPokemon:
                training[-1] = [
                    myCurrentPokemon.id,
                    myCurrentPokemon.currentHp / myCurrentPokemon.hp,
                    TYPE_CHART[myCurrentPokemon.types[0]]
                ]
                try:
                    training[-1].append(TYPE_CHART.get(myCurrentPokemon.types[1]))
                except:
                    training[-1].append(TYPE_CHART.get("Typeless"))

                for p in myPokemon:
                    if p.id != myCurrentPokemon.id:
                        training[-1].extend([
                            p.id,
                            p.currentHp / p.hp,
                            TYPE_CHART.get(p.types[0])
                        ])
                        try:
                            training[-1].append(TYPE_CHART.get(p.types[1]))
                        except:
                            training[-1].append(TYPE_CHART.get("Typeless"))
                training[-1].extend([
                    enemyCurrentPokemon.id,
                    enemyCurrentPokemon.currentHp / enemyCurrentPokemon.hp,
                    TYPE_CHART.get(enemyCurrentPokemon.types[0])
                ])
                for p in enemyPokemon:
                    if p.id != enemyCurrentPokemon.id:
                        training[-1].extend([
                            p.id,
                            p.currentHp / p.hp,
                            TYPE_CHART.get(p.types[0])
                        ])
                        try:
                            training[-1].append(TYPE_CHART.get(p.types[1]))
                        except:
                            training[-1].append(TYPE_CHART.get("Typeless"))
                for m in myCurrentPokemon.moves:
                    m = moveStatsId(m, moves)
                    training[-1].extend([
                        m.id,
                        TYPE_CHART[m.type],
                        calcKo(enemyCurrentPokemon, myCurrentPokemon, m, game)
                    ])
                    training[-1].extend(m.statusEffect)
                    training[-1].extend(m.statChange)
                for m in range(0, 4 - len(myCurrentPokemon.moves)):
                    training[-1].extend([
                        0,
                        0,
                        0
                    ])
                    training[-1].extend([0, 0])
                    training[-1].extend([0, 0, 0, 0, 0, 0, 0])
                if data[1] == "move" and "p1a" in line:
                    answer[-1] = [
                        0,
                        moveStats(data[3], moves).id
                    ]
                if data[1] == "move" and "p1a" in line:
                    answer[-1] = [
                        0,
                        moveStats(data[3], moves).id
                    ]

                if len(answer[-1]) == 0 and data[1] == "switch" and "p1a" in line:
                    answer[-1] = [
                        1,
                        findPokemon(data[3], pokemons)[0]
                    ]
        except NameError as e:
            pass
        except IndexError as e:
            pass
j = 0
print(len(training[-1]))
print(len(answer))
for i in range(0, len(training)):
    if len(training[i - j]) == 0 or len(answer[i - j]) != 2:
        training.pop(i - j)
        answer.pop(i - j)
        j += 1
    else:
        training[i - j] = numpy.reshape(numpy.array(training[i - j][:95]), (95))
        answer[i - j] = numpy.reshape(numpy.array(answer[i - j][:2]), (2))
training = numpy.array(training)
answer = numpy.array(answer)

model = Sequential()
model.add(Dense(1000, input_dim=(95), activation="relu"))
model.add(Dense(500, activation="relu"))
model.add(Dense(1500, activation="sigmoid"))
model.add(Dense(200, activation="relu"))
model.add(Dense(2, activation="relu"))
model.compile(loss='mean_absolute_error', optimizer="adam", metrics=['accuracy'])

model.fit(training, answer, epochs=50, batch_size=15)


model.save("play.krs")
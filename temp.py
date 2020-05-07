import pickle
import time

import joblib
import numpy
import difflib
from helper.functions import *
from helper.move import *
from helper.pokemon import Pokemon

with open('moves.txt', 'rb') as file:
    moves = pickle.load(file)

file.close()

with open('training/answerData.txt', 'rb') as file:
    training = pickle.load(file)
file.close()
with open('training/answerData2.txt', 'wb') as file:
    joblib.dump(training, file, compress=True)
exit()
with open('t/pokemon2.txt', 'rb') as file:
    pokemon_old = pickle.load(file)
with open('pokemon.txt', 'rb') as file:
    pokemon = pickle.load(file)

pokeMoveLookup = []
i = 0
for p in pokemon_old:
    if len(p) >= 6 and p[1] != None and "ability" not in p[1]:
        pokeMoveLookup.append(p[1])
        i += 1
print(len(pokemon_old))
print(len(pokeMoveLookup))
print(training.shape)
training = list(training)
i = 0
start = time.time()
prev = 0
b = []
b = []
for i in range(0, 2*900):
    b.append(0)
for m in moves:
    b[m.id * 2] = 0
    b[m.id * 2 + 1] = TYPE_CHART[m.type]
i = 0
for t in training:
    if int(t[0]) == 955:
        del training[i:]
        break
    if prev == int(t[0]):
        b[int(t[9]) * 2] = 2
        b[int(t[12]) * 2] = 2
        b[int(t[15]) * 2] = 2
        b[int(t[18]) * 2] = 2
        training[i] = list(t[:9]) + b
        i += 1
        continue
    prev = int(t[0])
    try:
        for m in pokemon_old[pokeMoveLookup.index(pokemon[int(t[0])][1])][5]:
            temp = moveStats(m, moves)
            b[temp.id * 2] = 1
            b[temp.id * 2 + 1] = TYPE_CHART[temp.type]
    except ValueError:
        try:
            for m in pokemon_old[pokeMoveLookup.index(pokemon[int(t[0])][1].split("-")[0])][5]:
                temp = moveStats(m, moves)
                b[temp.id * 2] = 1
                b[temp.id * 2 + 1] = TYPE_CHART[temp.type]
        except ValueError:
            d = difflib.get_close_matches(pokemon[int(t[0])][1].split("-")[0], pokeMoveLookup)[0]
            for m in pokemon_old[pokeMoveLookup.index(d)][5]:
                temp = moveStats(m, moves)
                b[temp.id * 2] = 1
                b[temp.id * 2 + 1] = TYPE_CHART[temp.type]
    b[int(t[9]) * 2] = 2
    b[int(t[12]) * 2] = 2
    b[int(t[15]) * 2] = 2
    b[int(t[18]) * 2] = 2
    training[i] = list(t[:9]) + b
    i += 1
    print(i)
training = numpy.array(training)
print(str(time.time() - start) + "sec")
with open('training/trainingData.txt', 'wb') as file:
    pickle.dump(training, file)
exit()
i = 0
for t in training:
    s = []
    poke = Pokemon(findPokemonId(t[0], pokemon))
    s.append(poke.id)
    s.append(TYPE_CHART[poke.types[0]])
    try:
        s.append(TYPE_CHART[poke.types[1]])
    except IndexError:
        s.append(0)
    s.extend(t[5:])
    for m in t[1:5]:
        move = moveStatsId(m, moves)
        s.append(move.id)
        s.append(TYPE_CHART[move.type])
        try:
            s.append(int(move.damage))
        except ValueError:
            s.append(0)
    training[i] = s
    i += 1

file.close()
with open('training/moves.txt', 'wb') as file:
    pickle.dump(training, file)

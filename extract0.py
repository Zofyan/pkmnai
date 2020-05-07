import requests
from pyquery import PyQuery
import pickle
from helper.move import *

moves = []

for x in range(1, 8):
    data = requests.get("https://pokemondb.net/move/generation/" + str(x))
    src = PyQuery(data.text)

    trs = src.find('.ent-name')
    length = len(moves)
    i = length
    for tr in trs:
        moves.append([])
        moves[i].append(tr.text)
        i += 1

    trs = src.find('.type-icon')
    i = length
    for tr in trs:
        moves[i].append(tr.text)
        i += 1

    trs = src.find('td:nth-child(3)')
    i = length
    for tr in trs:
        if tr.attrib["data-sort-value"] == "special":
            moves[i].append(1)
        elif tr.attrib["data-sort-value"] == "physical":
            moves[i].append(0)
        else:
            moves[i].append(2)
        i += 1

    trs = src.find('td:nth-child(4)')
    i = length
    for tr in trs:
        moves[i].append(tr.text)
        i += 1

    trs = src.find('td:nth-child(5)')
    i = length
    for tr in trs:
        moves[i].append(tr.text)
        i += 1
i = 0
for m in moves:
    moves[i] = Move([i + 1] + moves[i])
    i += 1

with open('moves.txt', 'wb') as file:
    pickle.dump(moves, file)

for move in moves:
    print(move)
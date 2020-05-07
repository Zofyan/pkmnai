from selenium import webdriver
import time
import pickle
from helper.functions import *
from helper.pokemon import Pokemon

with open('pokemon.txt', 'rb') as file:
    pokemons = pickle.load(file)
with open('training/moves.txt', 'rb') as file:
    training = pickle.load(file)
with open('moves.txt', 'rb') as file:
    moves = pickle.load(file)
page = webdriver.Firefox()
page.get('https://www.smogon.com/dex/sm/pokemon/')
time.sleep(5)
entries = []
j = 0
stop = False
fastList = []
for t in training:
    fastList.append(t[0])
print(fastList)
for i in range(0, 24):
    if i < 0:
        page.execute_script("window.scrollBy(0,1500)")
        time.sleep(1)
        continue
    lst = page.find_elements_by_css_selector('.PokemonAltRow-name a')
    for entry in lst:
        if findPokemon(entry.text, pokemons)[0] in fastList:
            continue
        print(entry.text)
        fastList.append(findPokemon(entry.text, pokemons))
        entries.append([entry.text, entry.get_attribute('href')])
    page.execute_script("window.scrollBy(0,1500)")
    time.sleep(1)
    if i == 0:
        break

for entry in entries:
    x = findPokemon(entry[0], pokemons)[0]
    print(entry[0])
    page.get(entry[1])
    for block in page.find_elements_by_css_selector('.BlockMovesetInfo'):
        poke = Pokemon(findPokemon(entry[0], pokemons))
        temp = [[[]]]
        for move in block.find_elements_by_css_selector('.MovesetInfo-moves .MoveList'):
            cnt = 0
            for move2 in move.find_elements_by_css_selector('a'):
                added = False
                if cnt >= 1:
                    added = True
                    mark = len(temp)-1
                    length = len(temp)
                    for t in range(0, length):
                        temp.append([temp[t][0][0:-1]])
                for t in range(0, len(temp)):
                    if added and (t <= mark):
                        continue
                    temp[t][0].append(moveStats(move2.text, moves).id)
                cnt += 1
        hp = poke.hp
        atk = poke.atk
        dfn = poke.dfn
        spa = poke.spa
        spd = poke.spd
        ape = poke.spe
        for ev in block.find_elements_by_css_selector('.evconfig li'):
            if ev.text.split()[1] == "SpA":
                poke.evs[3] = int(ev.text.split()[0])
            elif ev.text.split()[1] == "SpD":
                poke.evs[4] = int(ev.text.split()[0])
            elif ev.text.split()[1] == "Atk":
                poke.evs[1] = int(ev.text.split()[0])
            elif ev.text.split()[1] == "Def":
                poke.evs[2] = int(ev.text.split()[0])
            elif ev.text.split()[1] == "HP":
                poke.evs[0] = int(ev.text.split()[0])
            elif ev.text.split()[1] == "Spe":
                poke.evs[5] = int(ev.text.split()[0])
        for t in temp:
            t.append(poke.getStat("hp"))
            t.append(poke.getStat("atk"))
            t.append(poke.getStat("dfn"))
            t.append(poke.getStat("spa"))
            t.append(poke.getStat("spd"))
            t.append(poke.getStat("spe"))
        for t in temp:
            t = [x] + t
            training.append([t[0]])
            training[-1].extend(t[1])
            training[-1].extend(t[2:])
for p in training:
    print(p)
with open('training/moves.txt', 'wb') as file:
    pickle.dump(training, file)

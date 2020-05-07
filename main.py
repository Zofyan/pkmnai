import difflib
import random
from selenium import webdriver
import time
import pickle
from interact import Game
from helper.functions import *
from helper.pokemon import *

movesAi = load_model("models/moves.krs")
playAi = load_model("watch/play.krs")
with open('moves.txt', 'rb') as file:
    moves = pickle.load(file)
with open('pokemon.txt', 'rb') as file:
    pokemons = pickle.load(file)

with open('t/pokemon2.txt', 'rb') as file:
    pokemon_old = pickle.load(file)

pokeMoveLookup = []
for p in pokemon_old:
    if len(p) >= 6 and p[1] != None and "ability" not in p[1]:
        pokeMoveLookup.append(p[1])
url = 'https://play.pokemonshowdown.com'
game = Game(webdriver.Firefox())
game.document.implicitly_wait(3)
game.document.get(url)
time.sleep(2)

game.document.find_element_by_css_selector('button[name=login]').click()
game.document.find_element_by_css_selector('input[name=username]').send_keys('PigeonBot')
game.document.find_element_by_css_selector('.buttonbar button').click()
game.document.find_element_by_css_selector('button[name=openSounds]').click()
game.document.find_element_by_css_selector('input[name=muted]').click()
'''
page.find_element_by_css_selector('.formatselect').click()
time.sleep(1)
page.find_element_by_css_selector('button[value=gen7bssfactory]').click()
page.find_element_by_css_selector('.formatselect').click()
time.sleep(1)
page.find_element_by_css_selector('button[value=gen7battlefactory]').click()
'''
while 1:
    try:
        game.document.find_element_by_css_selector('button[name=acceptChallenge]').click()
        break
    except:
        pass

myPokemon = []
enemyPokemon = []
time.sleep(1)
i = 0
for start in game.document.find_elements_by_css_selector('.battle-history'):
    if i == 0:
        j = 0
        for mon in start.find_element_by_css_selector('em').text.split(" / "):
            #print(findPokemon(mon, pokemons))
            for t in game.document.find_elements_by_css_selector('button[name=chooseTeamPreview]'):
                if t.text in mon or mon in t.text:
                    print("Found")
                    target = t
                    break
            myPokemon.append(Pokemon(findPokemon(mon, pokemons)))
            for y in range(0, 5):
                try:
                    game.document.execute_script("$('button[name=chooseTeamPreview]:nth(" + str(j) + ")').mouseenter()")
                    print(game.document.find_element_by_css_selector('.tooltipinner p:nth-child(2)').text)
                    hp = game.document.find_element_by_css_selector('.tooltipinner p:nth-child(2)').text.split()[2].split("/")[0][1:]
                    data = game.document.find_element_by_css_selector('.tooltipinner p:nth-child(4)').text
                    stats = data.split(" / ")
                    break
                except:
                    pass
            myPokemon[-1].hp = int(hp)
            myPokemon[-1].currentHp = int(hp)
            myPokemon[-1].atk = int(stats[0].split()[1])
            myPokemon[-1].dfn = int(stats[1].split()[1])
            myPokemon[-1].spa = int(stats[2].split()[1])
            myPokemon[-1].spd = int(stats[3].split()[1])
            myPokemon[-1].spe = int(stats[4].split()[1])
            j += 1
    else:
        for mon in start.find_element_by_css_selector('em').text.split(" / "):
            enemyPokemon.append(Pokemon(findPokemon(mon, pokemons)))
    i += 1

first = random.randint(0, 5)

game.document.find_element_by_css_selector("button[name=chooseTeamPreview][value='" + str(first) + "']").click()
for i in range(0, 4):
    print("Starting in " + str(4-i))
    time.sleep(1)
quit = False
dead = False
fastList = []
while not quit:
    try:
        while game.waiting():
            pass
        quit = game.checkGameEnd()
        game.parseTurn(moves, myPokemon, enemyPokemon)
        print("My pokemon " + str(game.myCurrentPokemon.name))
        print("Enemy pokemon " + str(game.enemyCurrentPokemon.name))

        print("My stats:")
        print("Hp: " + str(game.myCurrentPokemon.currentHp))

        check = [
            game.enemyCurrentPokemon.id,
            TYPE_CHART[game.enemyCurrentPokemon.types[0]]
        ]
        try:
            check.append(TYPE_CHART[game.enemyCurrentPokemon.types[1]])
        except IndexError:
            check.append(0)
        check.extend([
            game.enemyCurrentPokemon.getStat("hp"),
            game.enemyCurrentPokemon.getStat("atk"),
            game.enemyCurrentPokemon.getStat("dfn"),
            game.enemyCurrentPokemon.getStat("spa"),
            game.enemyCurrentPokemon.getStat("spd"),
            game.enemyCurrentPokemon.getStat("spe")
        ])

        b = []
        for i in range(0, 2 * 900):
            b.append(0)
        for m in moves:
            b[m.id * 2] = 0
            b[m.id * 2 + 1] = TYPE_CHART[m.type]

        try:
            for m in pokemon_old[pokeMoveLookup.index(game.enemyCurrentPokemon.name)][5]:
                temp = moveStats(m, moves)
                b[temp.id * 2] = 1
                b[temp.id * 2 + 1] = TYPE_CHART[temp.type]
        except ValueError:
            try:
                for m in pokemon_old[pokeMoveLookup.index(game.enemyCurrentPokemon.name)][5]:
                    temp = moveStats(m, moves)
                    b[temp.id * 2] = 1
                    b[temp.id * 2 + 1] = TYPE_CHART[temp.type]
            except ValueError:
                d = difflib.get_close_matches(game.enemyCurrentPokemon.name, pokeMoveLookup, n=1, cutoff=0.0)[0]
                for m in pokemon_old[pokeMoveLookup.index(d)][5]:
                    temp = moveStats(m, moves)
                    b[temp.id * 2] = 1
                    b[temp.id * 2 + 1] = TYPE_CHART[temp.type]
        for m in game.enemyCurrentPokemon.moves:
            b[m.id * 2] = 2
        check = numpy.reshape(numpy.array([check + b]), (1, 9 + 2*900))
        pred = list(movesAi.predict(check)[0])
        print("Prediction: ")
        try:
            for x in range(0, 4):
                print(moveStatsId(pred.index(max(pred)), moves).name)
                del pred[pred.index(max(pred))]
                del pred[pred.index(max(pred))]
        except AttributeError as e:
            print(e)
        if not game.dead():
            print('Choosing move')
            if not game.chooseMove(moves, 0.10):
                try:
                    print('Choosing switch')
                    game.chooseSwitch(myPokemon)
                except ValueError:
                    game.chooseMove(moves, -1)
        else:
            print('Choosing switch')
            game.chooseSwitch(myPokemon)
        """
        data = [
            game.myCurrentPokemon.id,
            game.myCurrentPokemon.currentHp / game.myCurrentPokemon.hp,
            TYPE_CHART[game.myCurrentPokemon.types[0]]
        ]
        try:
            data.append(TYPE_CHART.get(game.myCurrentPokemon.types[1]))
        except:
            data.append(TYPE_CHART.get("Typeless"))

        for p in myPokemon:
            if p.id != game.myCurrentPokemon.id:
                data.extend([
                    p.id,
                    p.currentHp / p.hp,
                    TYPE_CHART.get(p.types[0])
                ])
                try:
                    data.append(TYPE_CHART.get(p.types[1]))
                except:
                    data.append(TYPE_CHART.get("Typeless"))
        data.extend([
            game.enemyCurrentPokemon.id,
            game.enemyCurrentPokemon.currentHp / game.enemyCurrentPokemon.hp,
            TYPE_CHART.get(game.enemyCurrentPokemon.types[0])
        ])
        for p in enemyPokemon:
            if p.id != game.enemyCurrentPokemon.id:
                data.extend([
                    p.id,
                    p.currentHp / p.hp,
                    TYPE_CHART.get(p.types[0])
                ])
                try:
                    data.append(TYPE_CHART.get(p.types[1]))
                except:
                    data.append(TYPE_CHART.get("Typeless"))
        for m in game.myCurrentPokemon.moves:
            m = moveStatsId(m, moves)
            data.extend([
                m.id,
                TYPE_CHART[m.type],
                calcKo(game.enemyCurrentPokemon, game.myCurrentPokemon, m, game)
            ])
            data.extend(m.statusEffect)
            data.extend(m.statChange)
        for m in range(0, 4 - len(game.myCurrentPokemon.moves)):
            data.extend([
                0,
                0,
                0
            ])
            data.extend([0, 0])
            data.extend([0, 0, 0, 0, 0, 0, 0])
        data = numpy.reshape(numpy.array(data), (1, 95))
        prediction = playAi.predict(data)
        print(prediction)
        if prediction[0][0] == 0:
            for move2 in game.document.find_elements_by_css_selector("button[name=chooseMove]"):
                try:
                    if " ".join(move2.text.split()[0:-2]) == moveStatsId(int(prediction[0][1]), moves).name:
                        move2.click()
                        game.parseDone = False
                except:
                    pass
        else:
            for move2 in game.document.find_elements_by_css_selector("button[name=chooseSwitch]"):
                try:
                    if " ".join(move2.text) == findPokemonId(int(prediction[0][1]), moves).name:
                        move2.click()
                        game.parseDone = False
                except:
                    pass
                    
        ### END OF TURN, ANALYSIS TIME
        if game.myCurrentPokemon.id not in fastList and len(game.getAvailableMoves()) > 0:
            fastList.append(game.myCurrentPokemon.id)
            train = [
                game.myCurrentPokemon.id,
                moveStats(game.getAvailableMoves()[0], moves).id,
                moveStats(game.getAvailableMoves()[1], moves).id,
                moveStats(game.getAvailableMoves()[2], moves).id,
                moveStats(game.getAvailableMoves()[3], moves).id,
                game.myCurrentPokemon.getStat("hp"),
                game.myCurrentPokemon.getStat("atk"),
                game.myCurrentPokemon.getStat("dfn"),
                game.myCurrentPokemon.getStat("spa"),
                game.myCurrentPokemon.getStat("spd"),
                game.myCurrentPokemon.getStat("spe")
            ]
            print(train)
            with open('training/moves.txt', 'rb') as file:
                training = pickle.load(file)
            training.append(train)
            with open('training/moves.txt', 'wb') as file:
                pickle.dump(training, file)
                """
    except TypeError as e:
        print(e)
    except NameError as e:
        print(e)

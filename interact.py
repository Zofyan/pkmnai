from helper.functions import calcEffictiveness, moveStats, calcKo
import time
from selenium.common.exceptions import StaleElementReferenceException

from helper.move import Move, STATUS_EFFECTS


class Game:
    class FatalError(Exception):
        pass

    def __init__(self, document):
        self.document = document
        self.myCurrentPokemon = 0
        self.enemyCurrentPokemon = 0
        self.weather = ''
        self.terrain = ''
        self.turn = 0
        self.parseDone = False

    def dead(self):
        for c in self.document.find_elements_by_css_selector('.whatdo'):
            if "Switch" in c.text:
                return True
        return False

    def getAvailableMoves(self):
        availableMoves = []
        for move in self.document.find_elements_by_css_selector("button[name=chooseMove]"):
            for i in range(0, 5):
                try:
                    availableMoves.append(" ".join(move.text.split()[0:-2]))
                    break
                except:
                    continue
        return availableMoves

    def getAvailableSwitches(self):
        availableSwitches = []
        for switch in self.document.find_elements_by_css_selector("button[name=chooseSwitch]"):
            for i in range(0, 5):
                try:
                    availableSwitches.append(switch.text)
                    break
                except:
                    continue
        return availableSwitches

    def getCurrentPokemon(self, pokemons, player):
        answer = 0
        if player == 'r':
            for history in reversed(self.document.find_elements_by_css_selector('.battle-history strong')):
                temp = history.find_element_by_xpath('..')
                for p in pokemons:
                    if len(temp.text.split()) > 0 and temp.text.split()[0] == "Go!" and p.name == history.text:
                        return p

        else:
            for history in reversed(self.document.find_elements_by_css_selector('.battle-history strong')):
                temp = history.find_element_by_xpath('..')
                for p in pokemons:
                    if len(temp.text.split()) > 3 and temp.text.split()[1] == "sent" and p.name == history.text:
                        return p
        raise self.FatalError("Current pokemon not found")

    def waiting(self):
        for check in self.document.find_elements_by_css_selector('.controls em'):
            try:
                if check.text == "Waiting for opponent...":
                    return True
            except StaleElementReferenceException:
                pass
        return False

    def checkGameEnd(self):
        for check in self.document.find_elements_by_css_selector("button[name=instantReplay]"):
            return True
        return False

    def bestSwitch(self, pokemon, enemy):
        possibilities = []
        best = []
        temp = self.getAvailableSwitches()
        print(temp)
        for p in pokemon:
            for t in temp:
                if p.name in t or t in p.name:
                    possibilities.append(p)
                    break
        for p in possibilities:
            tmp = 0
            for type in p.types:
                tmp += calcEffictiveness(enemy, Move([0, '', type, 0, 0, 0]))
            for type in enemy.types:
                tmp -= 1.5 * calcEffictiveness(p, Move([0, '', type, 0, 0, 0]))
            best.append([p.name, tmp])
        return max(best, key=lambda x: x[1])[0]

    def chooseMove(self, moves, threshold):
        availableMoves = self.getAvailableMoves()
        possibleMoves = []
        try:
            self.document.find_element_by_css_selector('input[name=megaevo]').click()
        except:
            pass
        for move in availableMoves:
            possibleMoves.append(moveStats(move, moves))
        if len(possibleMoves) > 0:
            for move in possibleMoves:
                dmg = calcKo(self.enemyCurrentPokemon, self.myCurrentPokemon, move, self)
                move.calculatedDamage = dmg

            possibleMoves.sort(key=lambda x: x.calculatedDamage, reverse=True)
            if possibleMoves[0].calculatedDamage / self.enemyCurrentPokemon.hp < threshold:
                return False
            try:
                print("At least " + str(100 * (possibleMoves[0].calculatedDamage) / self.enemyCurrentPokemon.hp) + "% damage")
                print("Max " + str(100 * (1.17647 * (possibleMoves[0].calculatedDamage)) / self.enemyCurrentPokemon.hp) + "% damage")
            except ZeroDivisionError:
                pass
            for move2 in self.document.find_elements_by_css_selector("button[name=chooseMove]"):
                try:
                    if " ".join(move2.text.split()[0:-2]) == possibleMoves[0].name:
                        move2.click()
                        self.parseDone = False
                        return True
                except:
                    pass

    def chooseSwitch(self, myPokemon):
        best = self.bestSwitch(myPokemon, self.enemyCurrentPokemon)
        for pokemon in self.document.find_elements_by_css_selector("button[name=chooseSwitch]"):
            try:
                print(pokemon.text, end=" _ ")
                print(best)
                if pokemon.text in best or best in pokemon.text:
                    pokemon.click()
                    self.parseDone = False
            except Exception as e:
                print(e)

    def parseTurn(self, moves, pokemons, enemyPokemons):
        if self.parseDone:
            return 0
        print("Parsing")
        time.sleep(1)
        found = False
        first = 0
        i = -1
        if self.turn == 0:
            found = True
        self.turn = len(self.document.find_elements_by_css_selector('h2.battle-history')) - 1
        for turn in self.document.find_elements_by_css_selector('.battle-history'):
            i += 1
            if not found:
                if turn.text == "Turn " + str(self.turn):
                    found = True
                continue
            line = turn.text.split()
            if "Go!" in turn.text:
                for p in pokemons:
                    if p.name in line[1] or line[1][:-1] in p.name:
                        self.myCurrentPokemon = p
            elif "sent out" in turn.text:
                print(turn.text)
                for p in enemyPokemons:
                    print(p.name + " / " + line[-1])
                    if p.name in line[-1] or line[-1][:-1] in p.name:
                        self.enemyCurrentPokemon = p
            elif first == 0 and "The opposing" in turn.text and "used" in turn.text:
                first = 2
                move = turn.find_element_by_css_selector('strong').text
                self.enemyCurrentPokemon.setMove(moveStats(move, moves))
            elif first == 0 and "used" in turn.text:
                first = 1
            elif "rose!" in turn.text:
                target = self.myCurrentPokemon
                if "opposing" in turn.text:
                    target = self.enemyCurrentPokemon
                if "Special Attack" in turn.text:
                    target.statChanges[2] += 1
                elif "Attack" in turn.text:
                    target.statChanges[0] += 1
                elif "Special Defense" in turn.text:
                    target.statChanges[3] += 1
                elif "Defense" in turn.text:
                    target.statChanges[1] += 1
                elif "Speed" in turn.text:
                    target.statChanges[4] += 1
                target.updateStats()
            elif "fell!" in turn.text:
                target = self.myCurrentPokemon
                if "opposing" in turn.text:
                    target = self.enemyCurrentPokemon
                if "Special Attack" in turn.text:
                    target.statChanges[2] -= 1
                elif "Attack" in turn.text:
                    target.statChanges[0] -= 1
                elif "Special Defense" in turn.text:
                    target.statChanges[3] -= 1
                elif "Defense" in turn.text:
                    target.statChanges[1] -= 1
                elif "Speed" in turn.text:
                    target.statChanges[4] -= 1
                target.updateStats()

            elif (first == 1 or first == 4) and "health" in turn.text and "lost" in turn.text and "some" not in turn.text:
                fraction = 0
                try:
                    fraction = float(line[4][:-1]) / 100
                except ValueError:
                    pass
                self.enemyCurrentPokemon.takeDamage(fraction)
                first = 3
            elif (first == 2 or first == 3) and "health" in turn.text and "lost" in turn.text and "some" not in turn.text:
                fraction = 0
                try:
                    fraction = float(line[2][:-1]) / 100
                except ValueError:
                    pass
                self.myCurrentPokemon.takeDamage(fraction)
                first = 4
            elif "opposing" in turn.text and "was burned" in turn.text:
                self.enemyCurrentPokemon.status = STATUS_EFFECTS['burn']
            elif "was burned" in turn.text:
                self.myCurrentPokemon.status = STATUS_EFFECTS['burn']
            elif "opposing" in turn.text and "was paralysed" in turn.text:
                self.enemyCurrentPokemon.status = STATUS_EFFECTS['paralysis']
            elif "was paralysed" in turn.text:
                self.myCurrentPokemon.status = STATUS_EFFECTS['paralysis']
            elif "opposing" in turn.text and "was badly poisoned" in turn.text:
                self.enemyCurrentPokemon.status = STATUS_EFFECTS['bad_poison']
            elif "was badly poisoned" in turn.text:
                self.myCurrentPokemon.status = STATUS_EFFECTS['bad_poison']
            elif "opposing" in turn.text and "was poisoned" in turn.text:
                self.enemyCurrentPokemon.status = STATUS_EFFECTS['poison']
            elif "was poisoned" in turn.text:
                self.myCurrentPokemon.status = STATUS_EFFECTS['poison']


        print('End parsing')
        self.turn += 1
        self.parseDone = True

import requests
from pyquery import PyQuery
import pickle
pokemon = []

data = requests.get("https://pokemondb.net/pokedex/national")
src = PyQuery(data.text)

cards = src.find('.infocard-lg-img')
i = 0
for card in cards:
    url = card.find('a').attrib['href']
    data = PyQuery(requests.get("https://pokemondb.net" + url).text)
    count = 0
    for table in data.find('.tabset-basics .vitals-table'):
        count += 1
    if(count == 1):
        pokemon.append([])
        pokemon[i].append(data.find('h1')[0].text)
        types = []
        for type in data.find('.tabset-basics .vitals-table .type-icon'):
            types.append(type.text)
        pokemon[i].append(types)
        abilities = []
        for ability in data.find('.tabset-basics .vitals-table .text-muted a'):
            abilities.append(ability.text)
        pokemon[i].append(abilities)
        stats = []
        for stat in data.find('.resp-scroll .vitals-table tr'):
            stats.append(stat.find('td:nth-child(1)').text)
        pokemon[i].append(stats)
        moves = []
        for move in data.find(table.attrib['href'] + ' .tabset-moves-game tr'):
            print(move)
            moves.append(move.find('.cell-name').text)
        pokemon[i].append(moves[0:-1])
        i += 1
    else:
        for table in data.find('.tabset-basics .tabs-tab'):
            pokemon.append([])
            pokemon[i].append(table.text)
            types = []
            for type in data.find(table.attrib['href'] + ' .vitals-table .type-icon'):
                types.append(type.text)
            pokemon[i].append(types)
            abilities = []
            for ability in data.find(table.attrib['href'] + ' .vitals-table .text-muted a'):
                abilities.append(ability.text)
            pokemon[i].append(abilities)
            stats = []
            for stat in data.find(table.attrib['href'] + ' .resp-scroll .vitals-table tr'):
                stats.append(stat.find('td').text)
            pokemon[i].append(stats[0:-1])
            moves = []
            for test in data.find('.tabs-tab'):
                if test.text == "Let's Go Pikachu/Let's Go Eevee":
                    continue
                for move in data.find(test.attrib['href'] + ' .cell-name .ent-name'):
                    moves.append(move.text)
            pokemon[i].append(list(set(moves[0:-1])))
            i += 1

for p in pokemon:
    print(p)

with open('pokemon.txt', 'wb') as file:
    pickle.dump(pokemon, file)

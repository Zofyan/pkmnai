from selenium import webdriver
import time
import pickle
fastList = list()
pokemons = []
page = webdriver.Firefox()
page.get('https://www.smogon.com/dex/sm/pokemon/')
time.sleep(5)
j = 0
print('test')
for i in range(0, 30):
    lst = page.find_elements_by_css_selector('.PokemonAltRow')
    for entry in lst:
        temp = entry.find_element_by_css_selector('.PokemonAltRow-name').text
        print(temp)
        stop = False
        if temp in fastList or (temp + "-Mega") in fastList:
            continue
        fastList.append(temp)
        print("Add: ", end='')
        print(temp)
        types = []
        for type in entry.find_elements_by_css_selector('.PokemonAltRow-types a'):
            types.append(type.text)
        abilities = []
        for ab in entry.find_elements_by_css_selector('.PokemonAltRow-abilities'):
            for ability in ab.find_elements_by_css_selector('a'):
                abilities.append(ability.text)
        t = [
            len(pokemons) + 1,
            temp,
            types,
            abilities,
            [
                int(entry.find_element_by_css_selector('.PokemonAltRow-hp span').text),
                int(entry.find_element_by_css_selector('.PokemonAltRow-atk span').text),
                int(entry.find_element_by_css_selector('.PokemonAltRow-def span').text),
                int(entry.find_element_by_css_selector('.PokemonAltRow-spa span').text),
                int(entry.find_element_by_css_selector('.PokemonAltRow-spd span').text),
                int(entry.find_element_by_css_selector('.PokemonAltRow-spe span').text)
                ],
        ]
        print(t)
        pokemons.append(t)
    page.execute_script("window.scrollBy(0,1800)")
    time.sleep(1)
    if i == 20:
        break
with open('pokemon.txt', 'wb') as file:
    pickle.dump(pokemons, file)

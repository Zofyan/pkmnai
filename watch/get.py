import os, os.path
from selenium import webdriver
DIR = "replays/"
start = int(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) / 2)

page = webdriver.Firefox()
page.get("https://replay.pokemonshowdown.com/")
page.find_element_by_css_selector('form input[name=format]').send_keys("battlefactory")
page.find_element_by_css_selector('form button:nth-child(1)').click()
page.find_element_by_css_selector('a.nav-last').click()

battles = []

for t in page.find_elements_by_css_selector('.linklist a'):
    battles.append(t.attrib['href'])

for b in battles:
    page.get("https://replay.pokemonshowdown.com/" + str(b))

for i in range(start, start + 100):
    f = open("replays/replay" + str(i) + ".html", 'w')
    print("Input replay:")
    while True:
        try:
            line = input()
            f.write(line + "\n")
        except EOFError:
            break
    f = open("replays/info" + str(i) + ".html", 'w')
    print("Input info:")
    while True:)
        try:
            line = input(
            f.write(line + "\n")
        except EOFError:
            break

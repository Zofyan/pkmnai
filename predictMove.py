import joblib
import pickle
import random
import numpy
from helper.functions import *
from keras.models import load_model, Sequential
from keras.layers import Dense, Dropout

with open('moves.txt', 'rb') as file:
    moves = pickle.load(file)
with open('pokemon.txt', 'rb') as file:
    pokemons = pickle.load(file)


def genTarget(targets):
    result = numpy.zeros((1, 900))
    result[0][targets[0]] = 1
    result[0][targets[1]] = 1
    result[0][targets[2]] = 1
    result[0][targets[3]] = 1
    return result


load = False
if not load:
    model = Sequential()
    model.add(Dense(1000, input_dim=(9 + 2 * 900), activation="relu"))
    model.add(Dense(1000, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(600, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(600, activation="relu"))
    model.add(Dense(4000, activation="relu"))
    model.add(Dense(900, activation="sigmoid"))
    model.compile(loss='binary_crossentropy', optimizer="Adam", metrics=['accuracy'])
else:
    model = load_model('models/moves.krs')

with open('training/trainingData2.txt', 'rb') as file:
    trainingData = joblib.load(file)
with open('training/answerData2.txt', 'rb') as file:
    answerData = joblib.load(file)
    file.close()
i = 1


def test(sample):
    prediction = list(model.predict(numpy.array([trainingData[sample]]))[0])
    print("Prediction for " + findPokemonId(trainingData[sample][0], pokemons)[1])
    for x in range(0, 4):
        try:
            i = prediction.index(max(prediction))
            del prediction[i]
            print(moveStatsId(i, moves).name, end=', ')
        except Exception as e:
            print('-', end=', ')
    print()


for i in range(0, 10):
    test(random.randint(0, 99000))
    print()
print(trainingData.shape)
print(answerData.shape)
s = numpy.arange(0, len(trainingData), 1)
numpy.random.shuffle(s)
trainingData = trainingData[s]
answerData = answerData[s]
model.fit(trainingData, answerData, epochs=5, batch_size=128)
model.save('models/moves.krs')

from urllib.request import urlopen
import json
import random
import copy
import numpy
import os.path
import math
import sys

class Options:
        def __init__(self, eloAdvantage=32.8, eloDraw=350, JSONLink='https://tcec.chessdom.com/schedule.json', engines_file_name='engines.json', simulcount=10000):
            self.eloAdvantage = eloAdvantage
            self.eloDraw = eloDraw
            self.JSONLink = JSONLink
            self.engines_file_name = engines_file_name
            self.simulcount = simulcount

options = Options()

class Engine:
    def __init__(self, engine_name, engine_elo):
        self.engine_name = engine_name
        self.engine_elo = engine_elo
    
    def __str__(self):
        return (self.engine_name + ': ' + str(self.engine_elo))

class Game:
    def __init__(self, white_engine, black_engine, result=0, played=0):
        self.white_engine = white_engine
        self.black_engine = black_engine
        self.result = result
        self.played = played
    
    def simulate(self):
        goodness = 1000000000
        res = random.randint(0, goodness)

        whiteWin = self.whiteProbability()
        blackWin = self.blackProbability()

        if res <= goodness * whiteWin:
            self.result = 1
        elif res <= goodness * (whiteWin + blackWin):
            self.result = 0
        else:
            self.result = 0.5

        self.played = True
    
    def clearResult(self):
        self.played = False
    
    def function(self, delta):
        return 1 / (1 + 10 ** (delta / 400))
    
    def whiteProbability(self):
        return self.function(self.black_engine.engine_elo - self.white_engine.engine_elo - options.eloAdvantage + options.eloDraw)
    
    def blackProbability(self):
        return self.function(self.white_engine.engine_elo - self.black_engine.engine_elo + options.eloAdvantage + options.eloDraw)

    def __str__(self):
        res = str(self.white_engine) + '\n' + str(self.black_engine)
        if self.played:
            res += '\n' + str(self.result)
        
        return res

def getSchedule(link):
    url = link
    response = urlopen(url)
    string = response.read().decode('utf-8')
    return string

def simulate(games):
    for i in games:
        i.simulate()

def calculatePositions(games):
    scores = {}

    for i in games:
        if i.white_engine.engine_name not in scores:
            scores[i.white_engine.engine_name] = 0
        if i.black_engine.engine_name not in scores:
            scores[i.black_engine.engine_name] = 0

        if i.result == 1:
            scores[i.white_engine.engine_name] += 1
        elif i.result == 0:
            scores[i.black_engine.engine_name] += 1
        else:
            scores[i.white_engine.engine_name] += 0.5
            scores[i.black_engine.engine_name] += 0.5
    
    result = []

    for i in sorted(scores.items(), key=lambda kv: kv[1], reverse=True):
        result.append(i[0])

    return result

def makeSimulations(games, engines, cnt, playedCount):
    result = {}

    for i in engines:
        result[i] = numpy.zeros(len(engines))
    
    for i in range(cnt):
        for j in range(playedCount + 1, len(games)):
            games[j].simulate()

        positions = calculatePositions(games)
        
        for j in range(len(positions)):
            result[positions[j]][j] += 1
    
    for i in sorted(result, key=lambda x: result[x].argmax()):
        print("{:<30}".format(i) + ": ", end=' ')
        for j in result[i]:
            print("{:07.4f}".format(j / cnt * 100), end=' ')
        print('')

def setEnginesInfo(engine_names, filename):
    data = {}

    print('Введите рейтинги движков:')
    
    for i in engine_names:
        print(i + ": ", end='')
        rating = int(input())
        data[i] = rating
    
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def installRatingEngines(engine_names, filename):
    engines = {}

    # Сопоставления движка и его рейтинга
    with open(filename, 'r') as data_file:
        data = json.load(data_file)

    for i in data:
        engines[i] = Engine(i, data[i])

    return engines

fromFile = False

for i in range(len(sys.argv)):
    if sys.argv[i] == '-eA':
        options.eloAdvantage = int(sys.argv[i+1])
    elif sys.argv[i] == '-eD':
        options.eloDraw = int(sys.argv[i+1])
    elif sys.argv[i] == '-l':
        options.JSONLink = sys.argv[i+1]
    elif sys.argv[i] == '-r':
        fromFile = True
        options.engines_file_name = sys.argv[i+1]
    elif sys.argv[i] == '-s':
        options.simulcount = int(sys.argv[i+1])
    elif sys.argv[i] == '-h':
        print('-h - show help\n-eA - set elo advantage\n-eD - set elo draw\n-l - link to JSON schedule\n-r - local file with engine ratings\n-s - number of simulations')
        exit(0)

schedule = json.loads(getSchedule(options.JSONLink))
engines_names = set()

# Find endines in file
for i in schedule:
    engines_names.add(i['White'])
    engines_names.add(i['Black'])

# Connect engines with ratings from file
if not os.path.isfile(options.engines_file_name) or not fromFile:
    setEnginesInfo(engines_names, options.engines_file_name)
    print('Saved to', options.engines_file_name)

engines = installRatingEngines(engines_names, options.engines_file_name)

for i in engines:
    print(engines[i])

games = []

playedCount = 0

for i in schedule:
    if not 'Result' in i:
        games.append(Game(engines[i['White']], engines[i['Black']]))
    else:
        playedCount += 1

        if i['Result'] == '1-0':
            games.append(Game(engines[i['White']], engines[i['Black']], 1, 1))
        elif i['Result'] == '0-1':
            games.append(Game(engines[i['White']], engines[i['Black']], 0, 1))
        else:
            games.append(Game(engines[i['White']], engines[i['Black']], 0.5, 1))

print('Played: {}/{}'.format(playedCount, len(games)))
makeSimulations(games, engines, options.simulcount, playedCount)